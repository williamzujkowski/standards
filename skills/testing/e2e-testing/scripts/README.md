# E2E Testing Scripts

Automation scripts for running tests in different environments.

## Files

- `run-e2e-tests.sh` - Comprehensive CI/CD test execution script

## Usage

### Basic Usage

```bash
# Run tests
./run-e2e-tests.sh

# With custom settings
TEST_FRAMEWORK=playwright BROWSER=chromium ENVIRONMENT=staging ./run-e2e-tests.sh
```

### Environment Variables

- `TEST_FRAMEWORK` - `playwright` or `cypress` (default: playwright)
- `BROWSER` - Browser to use: `chromium`, `firefox`, `webkit`, `all` (default: chromium)
- `ENVIRONMENT` - Environment: `development`, `staging`, `production` (default: staging)
- `PARALLEL` - Run tests in parallel: `true` or `false` (default: false)
- `HEADLESS` - Headless mode: `true` or `false` (default: true)
- `RETRIES` - Number of retries (default: 2)
- `WORKERS` - Number of parallel workers (default: 1)
- `VIDEO` - Video recording: `on`, `off`, `on-failure` (default: on-failure)
- `REPORT` - Report format: `html`, `json`, `junit` (default: html)

### CI/CD Integration

```yaml
# GitHub Actions
- name: Run E2E tests
  run: |
    chmod +x scripts/run-e2e-tests.sh
    ./scripts/run-e2e-tests.sh
  env:
    TEST_FRAMEWORK: playwright
    BROWSER: chromium
    ENVIRONMENT: staging
    CI: true
```
