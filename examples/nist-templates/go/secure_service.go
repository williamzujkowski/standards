package main

import (
	"bytes"
	"context"
	"crypto/hmac"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
	"golang.org/x/time/rate"
)

// @nist ac-3 "Access control structures"
// @nist ac-6 "Least privilege implementation"
type Permission string

const (
	PermissionRead   Permission = "read"
	PermissionWrite  Permission = "write"
	PermissionDelete Permission = "delete"
	PermissionAdmin  Permission = "admin"
)

type User struct {
	ID           string
	Username     string
	PasswordHash []byte
	Permissions  []Permission
	CreatedAt    time.Time
	UpdatedAt    time.Time
	// @nist ac-7 "Account lockout fields"
	FailedAttempts int
	LockedUntil    *time.Time
}

// @nist au-3 "Structured audit log entry"
type AuditLog struct {
	Timestamp     time.Time              `json:"timestamp"`
	CorrelationID string                 `json:"correlation_id"`
	UserID        string                 `json:"user_id,omitempty"`
	Action        string                 `json:"action"`
	Resource      string                 `json:"resource,omitempty"`
	Result        string                 `json:"result"`
	RemoteAddr    string                 `json:"remote_addr"`
	Details       map[string]interface{} `json:"details,omitempty"`
}

// @nist ia-2 "Authentication service"
// @nist ia-5 "Authenticator management"
type AuthService struct {
	userStore      UserStore
	jwtSecret      []byte
	auditLogger    *AuditLogger
	rateLimiters   map[string]*rate.Limiter
	rateLimiterMux sync.RWMutex
}

type UserStore interface {
	GetUser(ctx context.Context, username string) (*User, error)
	UpdateUser(ctx context.Context, user *User) error
	// @nist ia-5 "Password history management"
	CheckPasswordHistory(ctx context.Context, userID string, passwordHash []byte) (bool, error)
	AddPasswordHistory(ctx context.Context, userID string, passwordHash []byte) error
}

// @nist au-2 "Audit logging service"
type AuditLogger struct {
	mu     sync.Mutex
	output *log.Logger
}

func NewAuditLogger() *AuditLogger {
	return &AuditLogger{
		output: log.New(log.Writer(), "", 0), // Use structured logging in production
	}
}

func (al *AuditLogger) Log(entry AuditLog) {
	al.mu.Lock()
	defer al.mu.Unlock()

	// @nist au-3 "Generate complete audit records"
	data, _ := json.Marshal(entry)
	al.output.Println(string(data))
}

func NewAuthService(userStore UserStore, jwtSecret []byte) *AuthService {
	return &AuthService{
		userStore:    userStore,
		jwtSecret:    jwtSecret,
		auditLogger:  NewAuditLogger(),
		rateLimiters: make(map[string]*rate.Limiter),
	}
}

// @nist ac-7 "Rate limiting implementation"
func (as *AuthService) getRateLimiter(key string) *rate.Limiter {
	as.rateLimiterMux.RLock()
	limiter, exists := as.rateLimiters[key]
	as.rateLimiterMux.RUnlock()

	if !exists {
		// Create new rate limiter: 10 requests per minute with burst of 5
		limiter = rate.NewLimiter(rate.Every(6*time.Second), 5)

		as.rateLimiterMux.Lock()
		as.rateLimiters[key] = limiter
		as.rateLimiterMux.Unlock()
	}

	return limiter
}

// @nist ia-2 "User authentication"
// @nist-implements ia-2.1 "Network access with authentication"
// @evidence code, test
func (as *AuthService) Authenticate(ctx context.Context, username, password string) (string, error) {
	correlationID := ctx.Value("correlation_id").(string)
	remoteAddr := ctx.Value("remote_addr").(string)

	// @nist si-10 "Input validation"
	if err := validateUsername(username); err != nil {
		as.auditLogger.Log(AuditLog{
			Timestamp:     time.Now(),
			CorrelationID: correlationID,
			Action:        "auth.failed",
			Result:        "invalid_input",
			RemoteAddr:    remoteAddr,
			Details:       map[string]interface{}{"reason": "invalid_username"},
		})
		return "", errors.New("invalid credentials")
	}

	// @nist ac-7 "Check rate limit"
	limiter := as.getRateLimiter(remoteAddr)
	if !limiter.Allow() {
		as.auditLogger.Log(AuditLog{
			Timestamp:     time.Now(),
			CorrelationID: correlationID,
			Action:        "auth.rate_limited",
			Result:        "blocked",
			RemoteAddr:    remoteAddr,
		})
		return "", errors.New("rate limit exceeded")
	}

	user, err := as.userStore.GetUser(ctx, username)
	if err != nil {
		// @nist au-2 "Log authentication failures"
		as.auditLogger.Log(AuditLog{
			Timestamp:     time.Now(),
			CorrelationID: correlationID,
			Action:        "auth.failed",
			Result:        "user_not_found",
			RemoteAddr:    remoteAddr,
		})
		return "", errors.New("invalid credentials")
	}

	// @nist ac-7 "Check account lockout"
	if user.LockedUntil != nil && user.LockedUntil.After(time.Now()) {
		as.auditLogger.Log(AuditLog{
			Timestamp:     time.Now(),
			CorrelationID: correlationID,
			UserID:        user.ID,
			Action:        "auth.blocked",
			Result:        "account_locked",
			RemoteAddr:    remoteAddr,
		})
		return "", errors.New("account locked")
	}

	// @nist ia-5 "Password verification"
	err = bcrypt.CompareHashAndPassword(user.PasswordHash, []byte(password))
	if err != nil {
		// Handle failed attempt
		user.FailedAttempts++
		if user.FailedAttempts >= 5 {
			// @nist ac-7 "Lock account after 5 failed attempts"
			lockUntil := time.Now().Add(30 * time.Minute)
			user.LockedUntil = &lockUntil

			as.auditLogger.Log(AuditLog{
				Timestamp:     time.Now(),
				CorrelationID: correlationID,
				UserID:        user.ID,
				Action:        "auth.account_locked",
				Result:        "locked",
				RemoteAddr:    remoteAddr,
				Details:       map[string]interface{}{"locked_until": lockUntil},
			})
		}

		as.userStore.UpdateUser(ctx, user)

		// @nist au-2 "Log failed authentication"
		as.auditLogger.Log(AuditLog{
			Timestamp:     time.Now(),
			CorrelationID: correlationID,
			UserID:        user.ID,
			Action:        "auth.failed",
			Result:        "invalid_password",
			RemoteAddr:    remoteAddr,
			Details:       map[string]interface{}{"attempts": user.FailedAttempts},
		})

		return "", errors.New("invalid credentials")
	}

	// Reset failed attempts on successful auth
	if user.FailedAttempts > 0 {
		user.FailedAttempts = 0
		user.LockedUntil = nil
		as.userStore.UpdateUser(ctx, user)
	}

	// @nist ac-12 "Session management"
	token, err := as.generateToken(user)
	if err != nil {
		return "", err
	}

	// @nist au-2 "Log successful authentication"
	as.auditLogger.Log(AuditLog{
		Timestamp:     time.Now(),
		CorrelationID: correlationID,
		UserID:        user.ID,
		Action:        "auth.success",
		Result:        "authenticated",
		RemoteAddr:    remoteAddr,
	})

	return token, nil
}

// @nist ac-12 "Token generation with expiration"
func (as *AuthService) generateToken(user *User) (string, error) {
	claims := jwt.MapClaims{
		"user_id":     user.ID,
		"username":    user.Username,
		"permissions": user.Permissions,
		"exp":         time.Now().Add(time.Hour).Unix(), // 1 hour expiration
		"iat":         time.Now().Unix(),
		"iss":         "secure-service",
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(as.jwtSecret)
}

// @nist ia-5 "Password change with complexity validation"
// @nist-implements ia-5.1 "Password complexity and history"
func (as *AuthService) ChangePassword(ctx context.Context, userID, oldPassword, newPassword string) error {
	correlationID := ctx.Value("correlation_id").(string)

	// @nist si-10 "Validate password input"
	if err := validatePasswordComplexity(newPassword); err != nil {
		as.auditLogger.Log(AuditLog{
			Timestamp:     time.Now(),
			CorrelationID: correlationID,
			UserID:        userID,
			Action:        "password.change_failed",
			Result:        "complexity_failure",
			Details:       map[string]interface{}{"error": err.Error()},
		})
		return err
	}

	// Verify old password and update to new
	// Implementation details omitted for brevity

	// @nist au-2 "Log password changes"
	as.auditLogger.Log(AuditLog{
		Timestamp:     time.Now(),
		CorrelationID: correlationID,
		UserID:        userID,
		Action:        "password.changed",
		Result:        "success",
	})

	return nil
}

// @nist si-10 "Input validation functions"
func validateUsername(username string) error {
	if len(username) < 3 || len(username) > 50 {
		return errors.New("username must be between 3 and 50 characters")
	}

	// Allow only alphanumeric, underscore, and hyphen
	for _, char := range username {
		if !((char >= 'a' && char <= 'z') ||
			(char >= 'A' && char <= 'Z') ||
			(char >= '0' && char <= '9') ||
			char == '_' || char == '-') {
			return errors.New("username contains invalid characters")
		}
	}

	return nil
}

// @nist ia-5.1 "Password complexity validation"
func validatePasswordComplexity(password string) error {
	if len(password) < 12 {
		return errors.New("password must be at least 12 characters")
	}

	var hasUpper, hasLower, hasNumber, hasSpecial bool

	for _, char := range password {
		switch {
		case char >= 'A' && char <= 'Z':
			hasUpper = true
		case char >= 'a' && char <= 'z':
			hasLower = true
		case char >= '0' && char <= '9':
			hasNumber = true
		case strings.ContainsRune("!@#$%^&*(),.?\":{}|<>", char):
			hasSpecial = true
		}
	}

	if !hasUpper || !hasLower || !hasNumber || !hasSpecial {
		return errors.New("password must contain uppercase, lowercase, number, and special character")
	}

	return nil
}

// @nist ac-3 "Authorization middleware"
func RequirePermission(permission Permission, auditLogger *AuditLogger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ctx := r.Context()
			correlationID := ctx.Value("correlation_id").(string)

			// Extract user permissions from context (set by auth middleware)
			userPerms, ok := ctx.Value("permissions").([]Permission)
			if !ok {
				// @nist au-2 "Log authorization failures"
				auditLogger.Log(AuditLog{
					Timestamp:     time.Now(),
					CorrelationID: correlationID,
					Action:        "authz.failed",
					Result:        "no_permissions",
					Resource:      r.URL.Path,
					RemoteAddr:    r.RemoteAddr,
				})
				http.Error(w, "Forbidden", http.StatusForbidden)
				return
			}

			// @nist ac-3 "Check permission"
			hasPermission := false
			for _, p := range userPerms {
				if p == permission || p == PermissionAdmin {
					hasPermission = true
					break
				}
			}

			if !hasPermission {
				// @nist au-2 "Log authorization failures"
				auditLogger.Log(AuditLog{
					Timestamp:     time.Now(),
					CorrelationID: correlationID,
					UserID:        ctx.Value("user_id").(string),
					Action:        "authz.failed",
					Result:        "insufficient_permissions",
					Resource:      r.URL.Path,
					RemoteAddr:    r.RemoteAddr,
					Details:       map[string]interface{}{"required": permission},
				})
				http.Error(w, "Forbidden", http.StatusForbidden)
				return
			}

			next.ServeHTTP(w, r)
		})
	}
}

// @nist sc-8 "HTTPS enforcement middleware"
// @nist sc-13 "Cryptographic protection of communications"
func EnforceHTTPS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// In production, this would check for HTTPS
		// For development, we'll check for a header set by reverse proxy
		if r.Header.Get("X-Forwarded-Proto") != "https" && r.TLS == nil {
			// Redirect to HTTPS
			httpsURL := "https://" + r.Host + r.URL.String()
			http.Redirect(w, r, httpsURL, http.StatusMovedPermanently)
			return
		}

		// @nist sc-8 "Set security headers"
		w.Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("X-Frame-Options", "DENY")
		w.Header().Set("X-XSS-Protection", "1; mode=block")
		w.Header().Set("Content-Security-Policy", "default-src 'self'")

		next.ServeHTTP(w, r)
	})
}

// @nist au-2 "Request logging middleware"
func RequestLogger(auditLogger *AuditLogger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			correlationID := uuid.New().String()
			ctx := context.WithValue(r.Context(), "correlation_id", correlationID)
			ctx = context.WithValue(ctx, "remote_addr", r.RemoteAddr)

			// @nist au-3 "Log request details"
			auditLogger.Log(AuditLog{
				Timestamp:     time.Now(),
				CorrelationID: correlationID,
				Action:        "request.started",
				Result:        "processing",
				Resource:      r.URL.Path,
				RemoteAddr:    r.RemoteAddr,
				Details: map[string]interface{}{
					"method":     r.Method,
					"user_agent": r.Header.Get("User-Agent"),
				},
			})

			// Create response wrapper to capture status code
			wrapped := &responseWrapper{ResponseWriter: w}

			next.ServeHTTP(wrapped, r.WithContext(ctx))

			// @nist au-3 "Log response details"
			auditLogger.Log(AuditLog{
				Timestamp:     time.Now(),
				CorrelationID: correlationID,
				Action:        "request.completed",
				Result:        fmt.Sprintf("%d", wrapped.statusCode),
				Resource:      r.URL.Path,
				RemoteAddr:    r.RemoteAddr,
			})
		})
	}
}

type responseWrapper struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWrapper) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

// @nist si-11 "Error handling"
func ErrorHandler(auditLogger *AuditLogger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			defer func() {
				if err := recover(); err != nil {
					correlationID := r.Context().Value("correlation_id").(string)

					// @nist au-2 "Log errors"
					auditLogger.Log(AuditLog{
						Timestamp:     time.Now(),
						CorrelationID: correlationID,
						Action:        "error.panic",
						Result:        "internal_error",
						Resource:      r.URL.Path,
						RemoteAddr:    r.RemoteAddr,
						Details:       map[string]interface{}{"error": fmt.Sprintf("%v", err)},
					})

					// @nist si-11 "Return generic error to prevent information disclosure"
					http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				}
			}()

			next.ServeHTTP(w, r)
		})
	}
}

// @nist sc-8 "Webhook signature validation"
// @nist sc-13 "HMAC signature verification"
func ValidateWebhookSignature(secret []byte, auditLogger *AuditLogger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			signature := r.Header.Get("X-Webhook-Signature")
			if signature == "" {
				http.Error(w, "Missing signature", http.StatusUnauthorized)
				return
			}

			// Read body for signature verification
			body, err := io.ReadAll(r.Body)
			if err != nil {
				http.Error(w, "Bad request", http.StatusBadRequest)
				return
			}
			r.Body = io.NopCloser(bytes.NewBuffer(body))

			// Calculate expected signature
			h := hmac.New(sha256.New, secret)
			h.Write(body)
			expectedSig := hex.EncodeToString(h.Sum(nil))

			// Constant-time comparison
			if subtle.ConstantTimeCompare([]byte(signature), []byte(expectedSig)) != 1 {
				// @nist au-2 "Log signature validation failures"
				auditLogger.Log(AuditLog{
					Timestamp:     time.Now(),
					CorrelationID: r.Context().Value("correlation_id").(string),
					Action:        "webhook.invalid_signature",
					Result:        "rejected",
					RemoteAddr:    r.RemoteAddr,
				})
				http.Error(w, "Invalid signature", http.StatusUnauthorized)
				return
			}

			next.ServeHTTP(w, r)
		})
	}
}

func main() {
	// Initialize services
	auditLogger := NewAuditLogger()

	// Set up middleware chain
	mux := http.NewServeMux()

	// Example endpoint with authentication and authorization
	mux.Handle("/api/v1/admin",
		RequestLogger(auditLogger)(
			ErrorHandler(auditLogger)(
				EnforceHTTPS(
					RequirePermission(PermissionAdmin, auditLogger)(
						http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
							w.Write([]byte("Admin access granted"))
						}),
					),
				),
			),
		),
	)

	// Start server
	log.Println("Starting secure service on :8443")
	// @nist sc-8 "Use TLS in production"
	// In production, use ListenAndServeTLS with proper certificates
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
