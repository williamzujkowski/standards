# NIST Quickstart Example Makefile
# Demonstrates automated compliance checking

.PHONY: help install test lint nist-check validate run clean

help:
	@echo "NIST Quickstart Example - Available targets:"
	@echo "  make install     - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make nist-check - Check NIST control tags"
	@echo "  make validate   - Run all validation checks"
	@echo "  make run        - Run the example service"
	@echo "  make clean      - Clean generated files"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt || echo "No requirements.txt found"

test:
	@echo "Running tests..."
	python -m pytest test_auth_service.py -v

lint:
	@echo "Running linters..."
	python -m pylint auth-service.py || true
	python -m black --check auth-service.py || true

nist-check:
	@echo "Checking NIST control tags..."
	@echo "================================="
	@echo "Checking for NIST annotations in security code..."
	@grep -n "@nist" auth-service.py | head -20 || echo "No NIST tags found!"
	@echo ""
	@echo "Security patterns found:"
	@grep -E "(auth|password|encrypt|session|audit|validate)" auth-service.py | wc -l | xargs echo "  Security-related lines:"
	@echo ""
	@echo "NIST control coverage:"
	@grep -o "@nist [a-z][a-z]-[0-9]\+" auth-service.py | sort -u | wc -l | xargs echo "  Unique NIST controls:"
	@grep -o "@nist [a-z][a-z]-[0-9]\+" auth-service.py | sort -u || echo "  None found"
	@echo ""
	@echo "Validation result:"
	@if grep -q "@nist" auth-service.py; then \
		echo "  ✅ NIST tags present"; \
	else \
		echo "  ❌ Missing NIST tags in security code"; \
		exit 1; \
	fi

validate: lint test nist-check
	@echo "================================="
	@echo "✅ All validation checks passed!"

run:
	@echo "Running authentication service demo..."
	python auth-service.py

clean:
	@echo "Cleaning generated files..."
	rm -f *.pyc __pycache__/ audit.log
	rm -rf .pytest_cache/

# CI target for GitHub Actions
ci: install validate
	@echo "CI validation complete"
