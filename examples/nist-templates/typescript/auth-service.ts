/**
 * Authentication Service Template with NIST Controls
 * @nist ia-2 "User authentication service"
 * @nist ia-5 "Authenticator management"
 * @nist au-2 "Audit authentication events"
 */

import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { randomBytes } from 'crypto';

interface User {
  id: string;
  username: string;
  passwordHash: string;
  mfaSecret?: string;
  failedAttempts: number;
  lockedUntil?: Date;
}

interface AuthResult {
  success: boolean;
  token?: string;
  refreshToken?: string;
  error?: string;
}

export class AuthenticationService {
  private readonly saltRounds = 12; // @nist ia-5 "Strong password hashing"
  private readonly maxFailedAttempts = 5; // @nist ac-7 "Unsuccessful login attempts"
  private readonly lockoutDuration = 30 * 60 * 1000; // 30 minutes
  private readonly tokenExpiry = '1h'; // @nist ac-12 "Session termination"
  private readonly refreshTokenExpiry = '7d';

  constructor(
    private userRepository: any,
    private auditLogger: any,
    private jwtSecret: string
  ) {}

  /**
   * Authenticate user with username and password
   * @nist ia-2 "User authentication implementation"
   * @nist-implements ia-2.1 "Multi-factor authentication support"
   * @evidence code, test
   */
  async authenticate(username: string, password: string, mfaToken?: string): Promise<AuthResult> {
    // @nist si-10 "Input validation"
    if (!this.validateInput(username) || !this.validateInput(password)) {
      await this.auditLogger.log('auth.failed', {
        reason: 'invalid_input',
        username: this.sanitizeUsername(username)
      });
      return { success: false, error: 'Invalid credentials' };
    }

    const user = await this.userRepository.findByUsername(username);
    if (!user) {
      // @nist au-2 "Log authentication failures"
      await this.auditLogger.log('auth.failed', {
        reason: 'user_not_found',
        username: this.sanitizeUsername(username)
      });
      return { success: false, error: 'Invalid credentials' };
    }

    // @nist ac-7 "Check account lockout"
    if (this.isAccountLocked(user)) {
      await this.auditLogger.log('auth.blocked', {
        reason: 'account_locked',
        userId: user.id
      });
      return { success: false, error: 'Account locked' };
    }

    // @nist ia-5 "Verify password"
    const passwordValid = await bcrypt.compare(password, user.passwordHash);
    if (!passwordValid) {
      await this.handleFailedAttempt(user);
      return { success: false, error: 'Invalid credentials' };
    }

    // @nist ia-2.1 "Multi-factor authentication"
    if (user.mfaSecret && !this.verifyMfaToken(user.mfaSecret, mfaToken)) {
      await this.auditLogger.log('auth.mfa_failed', {
        userId: user.id
      });
      return { success: false, error: 'Invalid MFA token' };
    }

    // Reset failed attempts on successful auth
    await this.userRepository.resetFailedAttempts(user.id);

    // Generate tokens
    const token = this.generateToken(user);
    const refreshToken = this.generateRefreshToken(user);

    // @nist au-2 "Log successful authentication"
    await this.auditLogger.log('auth.success', {
      userId: user.id,
      method: user.mfaSecret ? 'mfa' : 'password'
    });

    return {
      success: true,
      token,
      refreshToken
    };
  }

  /**
   * Change user password
   * @nist ia-5 "Password management"
   * @nist-implements ia-5.1 "Password complexity and history"
   */
  async changePassword(userId: string, oldPassword: string, newPassword: string): Promise<boolean> {
    const user = await this.userRepository.findById(userId);
    if (!user) {
      return false;
    }

    // Verify old password
    const oldPasswordValid = await bcrypt.compare(oldPassword, user.passwordHash);
    if (!oldPasswordValid) {
      // @nist au-2 "Log password change failures"
      await this.auditLogger.log('password.change_failed', {
        userId,
        reason: 'invalid_old_password'
      });
      return false;
    }

    // @nist ia-5.1 "Validate password complexity"
    if (!this.validatePasswordComplexity(newPassword)) {
      await this.auditLogger.log('password.change_failed', {
        userId,
        reason: 'complexity_requirements'
      });
      return false;
    }

    // @nist ia-5.1 "Check password history"
    const passwordReused = await this.checkPasswordHistory(userId, newPassword);
    if (passwordReused) {
      await this.auditLogger.log('password.change_failed', {
        userId,
        reason: 'password_reuse'
      });
      return false;
    }

    // Hash and store new password
    const newPasswordHash = await bcrypt.hash(newPassword, this.saltRounds);
    await this.userRepository.updatePassword(userId, newPasswordHash);
    await this.userRepository.addPasswordHistory(userId, newPasswordHash);

    // @nist au-2 "Log password changes"
    await this.auditLogger.log('password.changed', {
      userId
    });

    return true;
  }

  /**
   * Validate password complexity requirements
   * @nist ia-5.1 "Password complexity validation"
   */
  private validatePasswordComplexity(password: string): boolean {
    // Minimum 12 characters
    if (password.length < 12) return false;

    // Must contain uppercase, lowercase, number, and special character
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return hasUppercase && hasLowercase && hasNumber && hasSpecial;
  }

  /**
   * Generate JWT token
   * @nist ac-12 "Session management"
   */
  private generateToken(user: User): string {
    return jwt.sign(
      {
        userId: user.id,
        username: user.username
      },
      this.jwtSecret,
      {
        expiresIn: this.tokenExpiry,
        issuer: 'auth-service',
        audience: 'api'
      }
    );
  }

  /**
   * Handle failed authentication attempt
   * @nist ac-7 "Account lockout implementation"
   */
  private async handleFailedAttempt(user: User): Promise<void> {
    user.failedAttempts++;

    if (user.failedAttempts >= this.maxFailedAttempts) {
      user.lockedUntil = new Date(Date.now() + this.lockoutDuration);

      // @nist au-2 "Log account lockout"
      await this.auditLogger.log('auth.account_locked', {
        userId: user.id,
        lockedUntil: user.lockedUntil
      });
    }

    await this.userRepository.updateFailedAttempts(user.id, user.failedAttempts, user.lockedUntil);

    // @nist au-2 "Log failed authentication"
    await this.auditLogger.log('auth.failed', {
      userId: user.id,
      attempt: user.failedAttempts
    });
  }

  /**
   * Input validation to prevent injection attacks
   * @nist si-10 "Information input validation"
   */
  private validateInput(input: string): boolean {
    if (!input || input.length > 255) return false;

    // Check for common injection patterns
    const dangerousPatterns = [
      /[<>]/,           // HTML tags
      /javascript:/i,   // JavaScript protocol
      /on\w+=/i,       // Event handlers
      /[\x00-\x1F]/    // Control characters
    ];

    return !dangerousPatterns.some(pattern => pattern.test(input));
  }

  private sanitizeUsername(username: string): string {
    // Remove any potentially sensitive characters for logging
    return username.replace(/[^a-zA-Z0-9._-]/g, '');
  }

  private isAccountLocked(user: User): boolean {
    return user.lockedUntil ? user.lockedUntil > new Date() : false;
  }

  private generateRefreshToken(user: User): string {
    return jwt.sign(
      {
        userId: user.id,
        type: 'refresh',
        nonce: randomBytes(16).toString('hex')
      },
      this.jwtSecret,
      {
        expiresIn: this.refreshTokenExpiry
      }
    );
  }

  private verifyMfaToken(secret: string, token?: string): boolean {
    // MFA implementation would go here
    // This is a placeholder
    return !!token && token.length === 6;
  }

  private async checkPasswordHistory(userId: string, newPassword: string): Promise<boolean> {
    const history = await this.userRepository.getPasswordHistory(userId, 5);

    for (const oldHash of history) {
      if (await bcrypt.compare(newPassword, oldHash)) {
        return true;
      }
    }

    return false;
  }
}
