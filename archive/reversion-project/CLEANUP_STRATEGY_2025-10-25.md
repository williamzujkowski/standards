# Safe Cleanup Strategy - Executive Summary

**Date:** 2025-10-25
**Architect:** System Architecture Designer
**Status:** READY FOR EXECUTION

## Current State

**Audit Results:**

- Broken links: **18** (17 in .backup/, 1 in docs/research/)
- Hub violations: **1** (docs/guides/REVERSION_GUIDE.md)
- Orphans: **11** (various documentation files)
- Archive size: 1.6MB (83 files, well-organized, KEEP)
- .backup size: 920KB (38 files, 33 days old, SAFE TO DELETE)

## Safety-First Approach

### Pre-Flight Checklist

- [x] Audit baseline captured
- [ ] Git tag created: `cleanup-baseline-2025-10-25`
- [ ] Working branch: `cleanup/safe-removal-2025-10-25`
- [ ] Rollback procedure documented

### Execution Phases

**Phase 1: Backup (5 min)**

```bash
git tag -a cleanup-baseline-2025-10-25 -m "Pre-cleanup: 18 broken, 1 hub violation, 11 orphans"
git checkout -b cleanup/safe-removal-2025-10-25
python3 scripts/generate-audit-reports.py > /tmp/baseline.log 2>&1
```

**Phase 2: Safe Deletions (10 min)**

```bash
# Verify no active links to .backup
grep -r "\.backup/" . --exclude-dir=.backup --exclude-dir=.git

# Remove .backup (920KB, fixes 17 broken links)
rm -rf .backup/

# Remove empty backups/ directory
rmdir backups/

# Expected: Broken links: 18 → 1 (94% reduction)
```

**Phase 3: Fix Hub Violation (5 min)**

```bash
# Auto-link REVERSION_GUIDE.md to hub
python3 scripts/ensure-hub-links.py

# Expected: Hub violations: 1 → 0 (100% compliance)
```

**Checkpoint Validation**

```bash
python3 scripts/generate-audit-reports.py
# Verify: Broken ≤1, Hubs = 0, Orphans ≤11
```

**Phase 4: Address Orphans (30 min)**

Strategy by category:

- **Root files** (GEMINI.md): Review → Link to README or archive
- **Docs files** (4 files): Auto-link via ensure-hub-links.py
- **Script docs** (2 files): Link to scripts/README.md or archive
- **Test docs** (4 files): Link to tests/README.md or archive

```bash
# Attempt auto-linking first
python3 scripts/ensure-hub-links.py

# For remaining orphans, manual decision:
# 1. Useful? → Link to hub
# 2. Historical? → Move to archive/reversion-project/
# 3. Duplicate? → Delete (verify first)
```

**Phase 5: Final Validation (10 min)**

```bash
python3 scripts/generate-audit-reports.py
python3 scripts/validate-skills.py
pre-commit run --all-files

# Must pass gates:
# Broken links ≤ 1
# Hub violations = 0
# Orphans ≤ 5
```

**Phase 6: Documentation (15 min)**

- Update CLAUDE.md with new audit metrics
- Create cleanup decision record
- Update README if needed

## Success Criteria (ALL MUST PASS)

- [ ] Broken links ≤ 1 (currently 18)
- [ ] Hub violations = 0 (currently 1)
- [ ] Orphans ≤ 5 (currently 11)
- [ ] All validation scripts pass
- [ ] Git tag created for instant rollback
- [ ] No references to deleted .backup/
- [ ] Documentation updated

## Risk Assessment

| Action | Risk | Mitigation |
|--------|------|------------|
| Delete .backup/ | **ZERO** | Excluded from prod, in git history |
| Delete backups/ | **ZERO** | Empty directory |
| Fix hub violations | **ZERO** | Additive links only |
| Resolve orphans | **LOW** | Manual review + validation |

**Overall Risk: LOW**

## Rollback Procedures

### Full Rollback

```bash
git checkout master
git reset --hard cleanup-baseline-2025-10-25
```

### Selective Restore

```bash
git checkout cleanup-baseline-2025-10-25 -- .backup/
git checkout cleanup-baseline-2025-10-25 -- path/to/file
```

## Expected Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Broken links | 18 | ≤1 | 94% reduction |
| Hub violations | 1 | 0 | 100% fixed |
| Orphans | 11 | ≤5 | 55% reduction |
| Disk freed | 0 | ~920KB | Cleaner repo |
| Gate compliance | ❌ | ✅ | Production ready |

## Decision Tree for Orphans

```
For each orphan file:
├─ Is content current/actively used?
│  └─ YES → Link to appropriate hub (docs/, scripts/, tests/)
├─ Is content historical/completed project?
│  └─ YES → Move to archive/reversion-project/ with README
├─ Is content duplicate of active file?
│  └─ YES → Delete (verify no references first)
└─ Uncertain?
   └─ STOP → Request human review
```

## Verification Commands

```bash
# Check for .backup references (should be empty)
grep -r "\.backup/" . --exclude-dir=.backup --exclude-dir=.git

# Check gates
cat reports/generated/structure-audit.md | grep -E "Broken|Hub|Orphan"

# Verify .backup is in audit exclusions
grep "\.backup" config/audit-rules.yaml

# Count orphans
grep -A 100 "Orphaned Files" reports/generated/structure-audit.md | grep "^-" | wc -l
```

## Time Estimate

- Phase 1 (Backup): 5 min
- Phase 2 (Deletions): 10 min
- Phase 3 (Hubs): 5 min
- Checkpoint: 5 min
- Phase 4 (Orphans): 30 min
- Phase 5 (Validation): 10 min
- Phase 6 (Docs): 15 min

**Total: ~80 minutes** for safe, validated execution

## Notes

- **Archive preserved**: 1.6MB of historical docs kept (already organized)
- **No production impact**: All deletions in excluded directories
- **Fully reversible**: Git tag + git history = instant rollback
- **Evidence-based**: Only remove what's proven unnecessary
- **Validation checkpoints**: After every phase

## Full Strategy Document

Complete implementation details stored in:

- **Memory**: `hive/cleanup/strategy` (11KB)
- **This file**: Executive summary for quick reference

---

**Ready for execution.** All phases documented, risks mitigated, rollback ready.
