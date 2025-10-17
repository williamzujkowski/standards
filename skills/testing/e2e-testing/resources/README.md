# E2E Testing Resources

Additional documentation and best practices guides.

## Files

- `e2e-best-practices.md` - Comprehensive anti-flakiness guide with patterns and anti-patterns

## Topics Covered

### Best Practices Guide

- Selector strategies (priority order)
- Wait patterns (auto-waiting, explicit waits)
- Test isolation (independent tests, fresh state)
- Data management (API setup, fixtures, cleanup)
- Network handling (mocking, stability)
- Common anti-patterns (timing, animations, race conditions)
- Debugging techniques (visual debugging, traces, logging)
- Performance optimization (parallel execution, sharding, auth reuse)

## Quick Reference

### Flaky Test Checklist

- [ ] Use `data-testid` for stable selectors
- [ ] Rely on framework auto-waiting
- [ ] Never use hard-coded timeouts
- [ ] Keep tests independent
- [ ] Mock external dependencies
- [ ] Clean up test data
- [ ] Wait for animations to complete
- [ ] Enable retries for CI
