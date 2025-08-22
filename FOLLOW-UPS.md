# Follow-Up Actions for Standards Repository

## Resolved Claims

All three NIST claims have been resolved with proper anchors:

1. Baseline selection → SP 800-53B §2 + FIPS 199
2. Tailoring → SP 800-53B §3
3. SSP documentation → PL-2 Control + SP 800-18r1 §2

## Standards Maintenance Tasks

| Task | Description | Owner | Due Date |
|------|-------------|-------|----------|
| ~~Update SLSA to v1.1~~ | ~~Create new standards/supply-chain/slsa-1.1.md with current specification~~ | ~~@williamzujkowski~~ | ~~2025-09-01~~ | COMPLETED |
| Verify NIST sections | Cross-reference all NIST SP 800-53 claims with actual PDF sections | @williamzujkowski | 2025-09-15 |
| ~~Add in-toto standard~~ | ~~Create standards/supply-chain/in-toto.md from https://in-toto.io/~~ | ~~@williamzujkowski~~ | ~~2025-09-30~~ | COMPLETED |

## Notes

- SLSA v1.0 confirmed as "Retired" status - document updated with prominent notice
- CycloneDX now properly references ECMA-424 (1st edition, June 2024) as primary source
- All new standards files created with proper YAML front matter and authoritative sources
