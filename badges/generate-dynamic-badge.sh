#!/bin/bash
# Generate dynamic badge based on actual metrics

# Get test coverage from your test output
COVERAGE=$(npm test -- --coverage --coverageReporters=text-summary | grep "Statements" | awk '{print $3}' | sed 's/%//')

# Determine color based on coverage
if (( $(echo "$COVERAGE >= 85" | bc -l) )); then
    COLOR="brightgreen"
elif (( $(echo "$COVERAGE >= 70" | bc -l) )); then
    COLOR="green"
elif (( $(echo "$COVERAGE >= 50" | bc -l) )); then
    COLOR="yellow"
else
    COLOR="red"
fi

# Generate badge URL
echo "https://img.shields.io/badge/coverage-${COVERAGE}%25-${COLOR}.svg"

# Update README with new badge
sed -i "s|https://img.shields.io/badge/coverage-[0-9]*%25-[a-z]*.svg|https://img.shields.io/badge/coverage-${COVERAGE}%25-${COLOR}.svg|g" README.md
