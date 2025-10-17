// Unit Testing Examples - Go
//
// This file demonstrates best practices for writing unit tests in Go,
// including table-driven tests, mocking, benchmarking, and test coverage.
//
// See: https://pkg.go.dev/testing

package testing_examples

import (
	"errors"
	"testing"
)

// ===== Example Code Under Test =====

// Calculator provides basic arithmetic operations
type Calculator struct{}

func (c *Calculator) Add(a, b int) int {
	return a + b
}

func (c *Calculator) Subtract(a, b int) int {
	return a - b
}

func (c *Calculator) Divide(a, b int) (float64, error) {
	if b == 0 {
		return 0, errors.New("cannot divide by zero")
	}
	return float64(a) / float64(b), nil
}

func (c *Calculator) Multiply(a, b int) int {
	return a * b
}

// User represents a user in the system
type User struct {
	ID       int
	Name     string
	Email    string
	IsActive bool
}

func (u *User) Deactivate() {
	u.IsActive = false
}

func (u *User) GetDisplayName() string {
	return u.Name + " (" + u.Email + ")"
}

// Database interface for mocking
type Database interface {
	Query(query string) (map[string]interface{}, error)
	Execute(query string) error
}

// UserRepository handles user data access
type UserRepository struct {
	db Database
}

func NewUserRepository(db Database) *UserRepository {
	return &UserRepository{db: db}
}

func (r *UserRepository) GetUserByID(id int) (*User, error) {
	result, err := r.db.Query("SELECT * FROM users WHERE id = ?")
	if err != nil {
		return nil, err
	}

	user := &User{
		ID:       result["id"].(int),
		Name:     result["name"].(string),
		Email:    result["email"].(string),
		IsActive: result["is_active"].(bool),
	}

	return user, nil
}

func (r *UserRepository) SaveUser(user *User) error {
	return r.db.Execute("INSERT INTO users VALUES (?)")
}

// ===== Basic Unit Tests =====

func TestCalculatorAdd(t *testing.T) {
	calc := &Calculator{}
	result := calc.Add(2, 3)

	if result != 5 {
		t.Errorf("Add(2, 3) = %d; want 5", result)
	}
}

func TestCalculatorSubtract(t *testing.T) {
	calc := &Calculator{}
	result := calc.Subtract(10, 3)

	if result != 7 {
		t.Errorf("Subtract(10, 3) = %d; want 7", result)
	}
}

func TestCalculatorMultiply(t *testing.T) {
	calc := &Calculator{}
	result := calc.Multiply(4, 5)

	if result != 20 {
		t.Errorf("Multiply(4, 5) = %d; want 20", result)
	}
}

func TestCalculatorDivide(t *testing.T) {
	calc := &Calculator{}
	result, err := calc.Divide(10, 2)

	if err != nil {
		t.Errorf("Divide(10, 2) returned error: %v", err)
	}

	if result != 5.0 {
		t.Errorf("Divide(10, 2) = %f; want 5.0", result)
	}
}

func TestCalculatorDivideByZero(t *testing.T) {
	calc := &Calculator{}
	_, err := calc.Divide(10, 0)

	if err == nil {
		t.Error("Divide(10, 0) should return an error")
	}

	expectedError := "cannot divide by zero"
	if err.Error() != expectedError {
		t.Errorf("Divide(10, 0) error = %q; want %q", err.Error(), expectedError)
	}
}

// ===== Table-Driven Tests (Go Best Practice) =====

func TestCalculatorAddTableDriven(t *testing.T) {
	calc := &Calculator{}

	tests := []struct {
		name     string
		a        int
		b        int
		expected int
	}{
		{"positive numbers", 2, 3, 5},
		{"zeros", 0, 0, 0},
		{"negative and positive", -1, 1, 0},
		{"large numbers", 100, 200, 300},
		{"negative numbers", -5, -3, -8},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Add(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
			}
		})
	}
}

func TestCalculatorDivideTableDriven(t *testing.T) {
	calc := &Calculator{}

	tests := []struct {
		name        string
		a           int
		b           int
		expected    float64
		expectError bool
	}{
		{"normal division", 10, 2, 5.0, false},
		{"large numbers", 100, 10, 10.0, false},
		{"decimal result", 7, 2, 3.5, false},
		{"negative dividend", -10, 2, -5.0, false},
		{"divide by zero", 10, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := calc.Divide(tt.a, tt.b)

			if tt.expectError {
				if err == nil {
					t.Errorf("Divide(%d, %d) should return an error", tt.a, tt.b)
				}
			} else {
				if err != nil {
					t.Errorf("Divide(%d, %d) returned unexpected error: %v", tt.a, tt.b, err)
				}
				if result != tt.expected {
					t.Errorf("Divide(%d, %d) = %f; want %f", tt.a, tt.b, result, tt.expected)
				}
			}
		})
	}
}

// ===== Mock Database for Testing =====

type MockDatabase struct {
	QueryFunc   func(query string) (map[string]interface{}, error)
	ExecuteFunc func(query string) error
}

func (m *MockDatabase) Query(query string) (map[string]interface{}, error) {
	if m.QueryFunc != nil {
		return m.QueryFunc(query)
	}
	return nil, nil
}

func (m *MockDatabase) Execute(query string) error {
	if m.ExecuteFunc != nil {
		return m.ExecuteFunc(query)
	}
	return nil
}

// ===== Tests with Mocks =====

func TestUserRepositoryGetUserByID(t *testing.T) {
	mockDB := &MockDatabase{
		QueryFunc: func(query string) (map[string]interface{}, error) {
			return map[string]interface{}{
				"id":        1,
				"name":      "Alice",
				"email":     "alice@example.com",
				"is_active": true,
			}, nil
		},
	}

	repo := NewUserRepository(mockDB)
	user, err := repo.GetUserByID(1)

	if err != nil {
		t.Errorf("GetUserByID(1) returned error: %v", err)
	}

	if user.ID != 1 {
		t.Errorf("user.ID = %d; want 1", user.ID)
	}

	if user.Name != "Alice" {
		t.Errorf("user.Name = %q; want %q", user.Name, "Alice")
	}

	if user.Email != "alice@example.com" {
		t.Errorf("user.Email = %q; want %q", user.Email, "alice@example.com")
	}

	if !user.IsActive {
		t.Error("user.IsActive = false; want true")
	}
}

func TestUserRepositoryGetUserByIDError(t *testing.T) {
	mockDB := &MockDatabase{
		QueryFunc: func(query string) (map[string]interface{}, error) {
			return nil, errors.New("database connection failed")
		},
	}

	repo := NewUserRepository(mockDB)
	_, err := repo.GetUserByID(1)

	if err == nil {
		t.Error("GetUserByID(1) should return an error when database fails")
	}

	expectedError := "database connection failed"
	if err.Error() != expectedError {
		t.Errorf("error = %q; want %q", err.Error(), expectedError)
	}
}

func TestUserRepositorySaveUser(t *testing.T) {
	executeCalled := false

	mockDB := &MockDatabase{
		ExecuteFunc: func(query string) error {
			executeCalled = true
			return nil
		},
	}

	repo := NewUserRepository(mockDB)
	user := &User{ID: 1, Name: "Bob", Email: "bob@example.com", IsActive: true}

	err := repo.SaveUser(user)

	if err != nil {
		t.Errorf("SaveUser() returned error: %v", err)
	}

	if !executeCalled {
		t.Error("SaveUser() did not call database Execute()")
	}
}

// ===== User Tests =====

func TestUserDeactivate(t *testing.T) {
	user := &User{ID: 1, Name: "Alice", Email: "alice@example.com", IsActive: true}

	user.Deactivate()

	if user.IsActive {
		t.Error("user.IsActive = true; want false after Deactivate()")
	}
}

func TestUserGetDisplayName(t *testing.T) {
	user := &User{ID: 1, Name: "Alice", Email: "alice@example.com", IsActive: true}

	displayName := user.GetDisplayName()
	expected := "Alice (alice@example.com)"

	if displayName != expected {
		t.Errorf("GetDisplayName() = %q; want %q", displayName, expected)
	}
}

func TestUserGetDisplayNameTableDriven(t *testing.T) {
	tests := []struct {
		name     string
		user     User
		expected string
	}{
		{
			"normal user",
			User{ID: 1, Name: "Alice", Email: "alice@example.com", IsActive: true},
			"Alice (alice@example.com)",
		},
		{
			"user with special characters",
			User{ID: 2, Name: "Bob O'Brien", Email: "bob+test@example.com", IsActive: true},
			"Bob O'Brien (bob+test@example.com)",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := tt.user.GetDisplayName()
			if result != tt.expected {
				t.Errorf("GetDisplayName() = %q; want %q", result, tt.expected)
			}
		})
	}
}

// ===== Subtests =====

func TestUser(t *testing.T) {
	t.Run("Deactivate", func(t *testing.T) {
		user := &User{ID: 1, Name: "Alice", Email: "alice@example.com", IsActive: true}
		user.Deactivate()

		if user.IsActive {
			t.Error("user.IsActive = true; want false")
		}
	})

	t.Run("GetDisplayName", func(t *testing.T) {
		user := &User{ID: 1, Name: "Alice", Email: "alice@example.com", IsActive: true}
		displayName := user.GetDisplayName()

		if displayName != "Alice (alice@example.com)" {
			t.Errorf("GetDisplayName() = %q; want %q", displayName, "Alice (alice@example.com)")
		}
	})
}

// ===== Benchmarks =====

func BenchmarkCalculatorAdd(b *testing.B) {
	calc := &Calculator{}

	for i := 0; i < b.N; i++ {
		calc.Add(2, 3)
	}
}

func BenchmarkCalculatorDivide(b *testing.B) {
	calc := &Calculator{}

	for i := 0; i < b.N; i++ {
		calc.Divide(10, 2)
	}
}

func BenchmarkUserGetDisplayName(b *testing.B) {
	user := &User{ID: 1, Name: "Alice", Email: "alice@example.com", IsActive: true}

	for i := 0; i < b.N; i++ {
		user.GetDisplayName()
	}
}

// ===== Test Helpers =====

func assertEqual(t *testing.T, got, want interface{}) {
	t.Helper()
	if got != want {
		t.Errorf("got %v; want %v", got, want)
	}
}

func assertNoError(t *testing.T, err error) {
	t.Helper()
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
}

func assertError(t *testing.T, err error, expectedMessage string) {
	t.Helper()
	if err == nil {
		t.Error("expected error, got nil")
		return
	}
	if err.Error() != expectedMessage {
		t.Errorf("error = %q; want %q", err.Error(), expectedMessage)
	}
}

// Example using test helpers
func TestCalculatorDivideWithHelpers(t *testing.T) {
	calc := &Calculator{}

	t.Run("normal division", func(t *testing.T) {
		result, err := calc.Divide(10, 2)
		assertNoError(t, err)
		assertEqual(t, result, 5.0)
	})

	t.Run("divide by zero", func(t *testing.T) {
		_, err := calc.Divide(10, 0)
		assertError(t, err, "cannot divide by zero")
	})
}

// ===== Testing Best Practices =====
//
// 1. Use table-driven tests for similar test cases
// 2. Use subtests (t.Run) to organize related tests
// 3. Use t.Helper() in test helper functions
// 4. Test both success and error paths
// 5. Use mocks/interfaces for dependencies
// 6. Write benchmarks for performance-critical code
// 7. Aim for high code coverage (use `go test -cover`)
// 8. Keep tests independent and isolated
// 9. Use descriptive test names
// 10. Run tests with race detector: `go test -race`
//
// Commands:
//   go test                          # Run all tests
//   go test -v                       # Verbose output
//   go test -cover                   # Show coverage
//   go test -coverprofile=cover.out  # Generate coverage report
//   go tool cover -html=cover.out    # View coverage in browser
//   go test -bench=.                 # Run benchmarks
//   go test -race                    # Run with race detector
//   go test -run TestName            # Run specific test
