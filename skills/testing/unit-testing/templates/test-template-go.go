// Go unit test template with table-driven tests
package mypackage

import (
    "testing"
    "errors"
)

// Table-driven test example
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"zero", 0, 0, 0},
        {"mixed", -5, 10, 5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// Error handling test
func TestDivide(t *testing.T) {
    t.Run("successful division", func(t *testing.T) {
        result, err := Divide(10, 2)
        if err != nil {
            t.Fatalf("unexpected error: %v", err)
        }
        if result != 5 {
            t.Errorf("got %d, want 5", result)
        }
    })

    t.Run("division by zero", func(t *testing.T) {
        _, err := Divide(10, 0)
        if err == nil {
            t.Error("expected error for division by zero")
        }
        if !errors.Is(err, ErrDivisionByZero) {
            t.Errorf("expected ErrDivisionByZero, got %v", err)
        }
    })
}

// Benchmark test
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(1, 2)
    }
}

// Parallel test execution
func TestParallel(t *testing.T) {
    t.Run("test1", func(t *testing.T) {
        t.Parallel()
        // Test code
    })

    t.Run("test2", func(t *testing.T) {
        t.Parallel()
        // Test code
    })
}
