# Archive Directory

This directory contains historical documentation and reports that are no longer actively used but preserved for reference.

## Directory Structure

### `old-migrations/`

**Created:** 2025-10-24
**Purpose:** Archive of completed migration documentation from standards to Anthropic Agent Skills format

**Contents:**

- Phase 1-3 planning documents (gate checklists, daily plans, progress trackers)
- Architecture design and requirements documents
- Skill mapping and transformation plans
- Migration implementation plans and executive summaries
- Research findings and risk mitigation strategies

**Why Archived:**

- Migration to skills format is complete (67 SKILL.md files created)
- Phase-based approach successfully executed
- Documentation was valuable during migration but now superseded by:
  - Active skills in `/skills` directory
  - Current guides in `/docs/guides`
  - Live implementation in repository

**Reference Value:**

- Historical context for repository evolution
- Migration methodology that could be reused
- Lessons learned for future transformations

### `old-reports/`

**Created:** 2025-10-24
**Purpose:** Archive of historical audit, validation, and phase completion reports

**Contents:** (~47 reports)

- Phase 1-5 completion and execution summaries
- Quality review and testing reports
- Performance analysis and benchmarking
- Token metrics and compatibility reports
- Workflow failure analysis
- Vestigial content analysis (meta!)
- Documentation accuracy audits

**Why Archived:**

- Superseded by current audit reports in `/reports/generated/`
- Historical snapshots of repository quality at different phases
- No longer actionable (issues resolved or obsolete)

**What Remains Active:**

- `/reports/generated/structure-audit.md` - Current link/orphan status
- `/reports/generated/linkcheck.txt` - Latest broken link scan
- `/reports/generated/hub-matrix.tsv` - Current hub compliance
- `/reports/generated/accuracy-audit.md` - Recent accuracy review
- `/reports/generated/quality-review.md` - Latest quality assessment

### `planning-docs/`

**Created:** 2025-10-24
**Purpose:** Archive of root-level planning documents

**Contents:**

- `update_repo.md` - Initial repository update plan
- `project_plan.md` - LLM optimization project plan (4-week timeline)
- `skills_alignment.md` - Skills alignment guide and migration prompt

**Why Archived:**

- Work described in these plans is substantially complete
- Planning phase transitioned to implementation phase
- Root directory should contain only active configuration (CLAUDE.md, README.md)

**Superseded By:**

- Current `/CLAUDE.md` - Active configuration and standards router
- `/docs/guides/KICKSTART_PROMPT.md` - Current kickstart workflow
- `/docs/guides/USING_PRODUCT_MATRIX.md` - Product matrix documentation
- Active `/skills` directory structure

## Deletion Policy

**Files in archive/ are:**

- ✅ Safe to reference
- ✅ Kept in git history
- ⚠️ Not actively maintained
- ❌ Not linked from active documentation

**Retention Period:**

- Migration docs: Keep until repository is stable for 6+ months
- Old reports: Keep for 3-6 months, then consider pruning
- Planning docs: Keep indefinitely as historical context

## Restoration Guidance

If you need to restore archived content:

```bash
# View what was in migration docs
ls archive/old-migrations/migration/

# Restore specific file to docs/
git mv archive/old-migrations/migration/research-findings.md docs/migration/

# Restore entire migration directory
git mv archive/old-migrations/migration docs/
```

## Archive Metadata

| Item | Files | Size | Archived | Reason |
|------|-------|------|----------|--------|
| Migration docs | 30 | 728KB | 2025-10-24 | Migration complete |
| Old reports | 47 | ~9MB | 2025-10-24 | Superseded by current audits |
| Planning docs | 3 | ~40KB | 2025-10-24 | Implementation complete |
| CLAUDE_backup.md | 1 | ~15KB | 2025-10-24 | Duplicate (deleted) |

**Total Archived:** 80 files, ~10MB
**Cleanup Benefit:** Simplified repository navigation, clearer active vs. historical content

## Questions?

If you're unsure whether archived content is still relevant, check:

1. Is this referenced in current docs? (Use `grep -r "filename" docs/`)
2. Is the work described still in progress? (Check project issues/PRs)
3. Does `/reports/generated/` have a newer version?

When in doubt, content can be restored from archive or git history.
