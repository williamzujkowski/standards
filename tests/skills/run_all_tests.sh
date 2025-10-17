#!/bin/bash
# Run all skills tests and generate reports
# Usage: ./run_all_tests.sh [--coverage] [--reports]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Options
COVERAGE=false
REPORTS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --coverage)
      COVERAGE=true
      shift
      ;;
    --reports)
      REPORTS=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Skills Test Suite Runner${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Create reports directory
mkdir -p reports/generated

# Run pytest tests
echo -e "${GREEN}Running pytest test suite...${NC}"

if [ "$COVERAGE" = true ]; then
  pytest tests/skills/ -v --cov=docs/skills --cov-report=term --cov-report=html --tb=short
  echo -e "${GREEN}Coverage report generated: htmlcov/index.html${NC}"
else
  pytest tests/skills/ -v --tb=short
fi

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -ne 0 ]; then
  echo -e "${RED}Some tests failed!${NC}"
  exit $TEST_EXIT_CODE
fi

echo ""
echo -e "${GREEN}✓ All pytest tests passed!${NC}"
echo ""

# Generate reports if requested
if [ "$REPORTS" = true ]; then
  echo -e "${BLUE}Generating analysis reports...${NC}"
  echo ""

  echo -e "${YELLOW}1. Token Optimization Analysis...${NC}"
  python3 tests/skills/test_token_optimization.py || true

  echo ""
  echo -e "${YELLOW}2. Backward Compatibility Analysis...${NC}"
  python3 tests/skills/test_backward_compatibility.py || true

  echo ""
  echo -e "${YELLOW}3. Resource Bundling Analysis...${NC}"
  python3 tests/skills/test_resource_bundling.py || true

  echo ""
  echo -e "${YELLOW}4. Skill Discovery Analysis...${NC}"
  python3 tests/skills/test_skill_discovery.py || true

  echo ""
  echo -e "${YELLOW}5. Skill Validation...${NC}"
  python3 tests/skills/test_skill_validation.py || true

  echo ""
  echo -e "${GREEN}✓ Reports generated in reports/generated/${NC}"
  echo ""
  echo "Available reports:"
  ls -lh reports/generated/*.{md,json} 2>/dev/null || echo "No reports found yet (skills may not be created)"
fi

echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}Test Suite Complete!${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "Summary:"
echo "  ✓ Pytest tests: PASSED"
if [ "$COVERAGE" = true ]; then
  echo "  ✓ Coverage report: htmlcov/index.html"
fi
if [ "$REPORTS" = true ]; then
  echo "  ✓ Analysis reports: reports/generated/"
fi
echo ""
echo "Next steps:"
echo "  1. Review test results"
echo "  2. Check coverage report (if generated)"
echo "  3. Review analysis reports (if generated)"
echo "  4. Address any issues or warnings"
echo ""
