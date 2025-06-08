# Go Project Makefile - Following CODING_STANDARDS.md and TESTING_STANDARDS.md

.PHONY: help build test lint format security-check coverage clean install-tools

# Default target
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-tools: ## Install required development tools
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install golang.org/x/tools/cmd/goimports@latest
	go install github.com/securego/gosec/v2/cmd/gosec@latest
	go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
	go install honnef.co/go/tools/cmd/staticcheck@latest
	go install golang.org/x/vuln/cmd/govulncheck@latest

build: ## Build the application
	go build -v -o bin/app ./cmd/app

test: ## Run tests
	go test -v -race ./...

coverage: ## Run tests with coverage (target: 85%)
	@echo "Running tests with coverage..."
	@go test -coverprofile=coverage.out -covermode=atomic ./...
	@go tool cover -func=coverage.out | grep total | awk '{print $$3}' | sed 's/%//g' | \
		awk '{if ($$1 < 85) {print "❌ Coverage is below 85%: " $$1 "%"; exit 1} else {print "✅ Coverage: " $$1 "% (target: 85%)"}}'
	@echo "\nDetailed coverage report:"
	@go tool cover -func=coverage.out

coverage-html: coverage ## Generate HTML coverage report
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

lint: ## Run linters (golangci-lint)
	@echo "Running golangci-lint..."
	golangci-lint run --timeout=5m
	
	@echo "\nChecking formatting..."
	@if [ -n "$$(gofmt -l .)" ]; then \
		echo "❌ The following files need formatting:"; \
		gofmt -l .; \
		exit 1; \
	else \
		echo "✅ All files are properly formatted"; \
	fi
	
	@echo "\nChecking cyclomatic complexity..."
	gocyclo -over 10 .
	
	@echo "\nRunning staticcheck..."
	staticcheck ./...

format: ## Format code
	@echo "Formatting code..."
	gofmt -s -w .
	goimports -w .
	@echo "✅ Code formatted"

security-check: ## Run security checks
	@echo "Running security scan with gosec..."
	gosec -fmt=json -out=security-report.json ./... || true
	gosec ./...
	
	@echo "\nChecking for vulnerabilities..."
	govulncheck ./...

vet: ## Run go vet
	go vet ./...

mod-tidy: ## Tidy go modules
	go mod tidy
	go mod verify

clean: ## Clean build artifacts
	rm -rf bin/ coverage.* security-report.json

# Combined targets for CI/CD
ci: lint vet test coverage security-check ## Run all CI checks

pre-commit: format mod-tidy lint vet test ## Run pre-commit checks

# Development workflow
dev-test: ## Run tests in watch mode (requires entr)
	@if command -v entr > /dev/null; then \
		find . -name '*.go' | entr -c go test -v ./...; \
	else \
		echo "Install entr for watch mode: https://github.com/eradman/entr"; \
		exit 1; \
	fi

benchmark: ## Run benchmarks
	go test -bench=. -benchmem ./...

profile-cpu: ## Generate CPU profile
	go test -cpuprofile=cpu.prof -bench=. ./...
	go tool pprof -http=:8080 cpu.prof

profile-mem: ## Generate memory profile
	go test -memprofile=mem.prof -bench=. ./...
	go tool pprof -http=:8080 mem.prof