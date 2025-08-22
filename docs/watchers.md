# Live Source Watchers

This repository includes automated watchers that monitor authoritative security sources for updates.

## KEV Catalog Watcher

### What It Does

The KEV (Known Exploited Vulnerabilities) watcher monitors CISA's KEV catalog daily for new vulnerabilities that are being actively exploited in the wild.

- **Schedule**: Runs daily at 12:00 UTC
- **Source**: [CISA KEV Catalog](https://www.cisa.gov/resources-tools/resources/kev-catalog)
- **Data Location**: `data/kev_latest.json`
- **Script**: `scripts/check-kev-updates.js`
- **Workflow**: `.github/workflows/kev-watch.yml`

### How It Works

1. Fetches the latest KEV catalog JSON from CISA
2. Compares with cached version in `data/kev_latest.json`
3. If new entries are found:
   - Updates the cache file via automated commit
   - Creates or updates a GitHub issue with details
   - Labels the issue with `kev-update` and `security`

### Issue Format

When new vulnerabilities are detected, an issue is created with:

- Table of new CVEs with vendor, product, and date added
- Link to full CISA catalog
- Recommended actions for remediation

### Opt-Out for Forks

If you fork this repository and don't want KEV monitoring:

1. **Disable the workflow**:
   - Go to Actions tab → KEV Catalog Watcher → Disable workflow

2. **Or remove the workflow file**:

   ```bash
   rm .github/workflows/kev-watch.yml
   ```

3. **Or modify the schedule** in `.github/workflows/kev-watch.yml`:

   ```yaml
   schedule:
     - cron: '0 0 * * 0'  # Weekly instead of daily
   ```

## Future Watchers

### OWASP Top 10 Monitoring

A lightweight radar document tracks OWASP Top 10 updates:

- Location: `docs/radar/owasp-top10-2025.md`
- Manual review recommended quarterly
- Watch for 2025 release announcements

### Planned Additions

- NIST publication updates (SP 800 series)
- SLSA specification versions
- CycloneDX/SPDX SBOM format changes
- CISA Secure by Design updates

## Data Storage

All watcher data is stored in the `data/` directory:

- `kev_latest.json` - Latest KEV catalog cache
- Future: Additional source caches as watchers are added

## Security Considerations

- Watchers only fetch public data from official sources
- No credentials or API keys required
- Data is validated before caching
- Failed fetches don't corrupt existing cache

## Contributing

To add a new watcher:

1. Create script in `scripts/check-{source}-updates.js`
2. Add workflow in `.github/workflows/{source}-watch.yml`
3. Document here with source URL and schedule
4. Ensure graceful failure handling
