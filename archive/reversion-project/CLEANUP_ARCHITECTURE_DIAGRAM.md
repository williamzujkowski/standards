# Cleanup Strategy Architecture

**Date:** 2025-10-25
**Type:** System Architecture Design

## Safety Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SAFETY FIRST DESIGN                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────┐                                            │
│  │ Git Tag    │──────> cleanup-baseline-2025-10-25         │
│  │ (Rollback) │        (Instant restore if needed)         │
│  └────────────┘                                            │
│        │                                                    │
│        v                                                    │
│  ┌────────────┐        ┌──────────────┐                   │
│  │  Working   │───────>│  Validation  │                   │
│  │  Branch    │        │  Checkpoints │                   │
│  └────────────┘        └──────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Execution Flow

```
Phase 1: BACKUP (5 min)
┌──────────────────────────────────────┐
│ 1. Create git tag                    │
│ 2. Create working branch             │
│ 3. Capture audit baseline            │
│ 4. Validate exclusion policy         │
└──────────────┬───────────────────────┘
               │
               v
Phase 2: SAFE DELETIONS (10 min)
┌──────────────────────────────────────┐
│ 1. Verify no active links to .backup │
│ 2. Delete .backup/ (920KB, 38 files) │
│ 3. Delete backups/ (empty dir)       │
│ 4. Validate: Broken 18→1             │
└──────────────┬───────────────────────┘
               │
               v
Phase 3: HUB VIOLATIONS (5 min)
┌──────────────────────────────────────┐
│ 1. Run ensure-hub-links.py           │
│ 2. Link REVERSION_GUIDE.md           │
│ 3. Validate: Hub violations 1→0      │
└──────────────┬───────────────────────┘
               │
               v
CHECKPOINT VALIDATION
┌──────────────────────────────────────┐
│ ✓ Broken ≤1                          │
│ ✓ Hubs = 0                           │
│ ✓ Orphans ≤11                        │
└──────────────┬───────────────────────┘
               │
               v
Phase 4: ORPHAN RESOLUTION (30 min)
┌──────────────────────────────────────┐
│ Decision Tree:                       │
│ ├─ Current/useful? → Link to hub    │
│ ├─ Historical? → Archive             │
│ ├─ Duplicate? → Delete               │
│ └─ Uncertain? → Human review         │
│                                      │
│ Target: Orphans 11→≤5                │
└──────────────┬───────────────────────┘
               │
               v
Phase 5: FINAL VALIDATION (10 min)
┌──────────────────────────────────────┐
│ 1. generate-audit-reports.py        │
│ 2. validate-skills.py                │
│ 3. pre-commit --all-files            │
│                                      │
│ Gates (ALL MUST PASS):               │
│ ✓ Broken links ≤ 1                   │
│ ✓ Hub violations = 0                 │
│ ✓ Orphans ≤ 5                        │
└──────────────┬───────────────────────┘
               │
               v
Phase 6: DOCUMENTATION (15 min)
┌──────────────────────────────────────┐
│ 1. Update CLAUDE.md metrics          │
│ 2. Create decision record            │
│ 3. Update README if needed           │
└──────────────────────────────────────┘
```

## File Organization Strategy

```
BEFORE CLEANUP:
/home/william/git/standards/
├── .backup/                     [DELETE]
│   ├── skill-fixes-20251024/    920KB, 38 files, 33 days old
│   └── → 17 broken links here   ❌ Vestigial
├── backups/                     [DELETE]
│   └── (empty directory)        ❌ Unnecessary
├── archive/                     [KEEP]
│   ├── old-migrations/          ✅ Organized 2024-10-24
│   ├── old-reports/             ✅ Well-documented
│   ├── planning-docs/           ✅ Historical value
│   └── README.md + reports      1.6MB, 83 files
├── docs/
│   ├── guides/
│   │   └── REVERSION_GUIDE.md   ❌ Hub violation
│   ├── architecture/
│   │   └── *.md                 ❌ 1 orphan
│   ├── optimization/
│   │   └── *.md                 ❌ 1 orphan
│   ├── research/
│   │   └── *.md                 ❌ 1 orphan + 1 broken link
│   └── scripts/
│       └── *.md                 ❌ 1 orphan
├── scripts/
│   └── REVERSION_*.md           ❌ 2 orphans
├── tests/
│   └── reversion-*.md           ❌ 4 orphans
└── GEMINI.md                    ❌ 1 orphan (untracked)

AFTER CLEANUP:
/home/william/git/standards/
├── .backup/                     ✅ REMOVED (-920KB)
├── backups/                     ✅ REMOVED
├── archive/                     ✅ PRESERVED (1.6MB)
│   ├── old-migrations/
│   ├── old-reports/
│   ├── planning-docs/
│   └── reversion-project/       ✅ NEW (consolidated orphans)
├── docs/
│   ├── guides/
│   │   └── REVERSION_GUIDE.md   ✅ Linked to hub
│   ├── architecture/
│   │   └── *.md                 ✅ Linked to hub
│   ├── optimization/
│   │   └── *.md                 ✅ Linked to hub
│   └── research/
│       └── *.md                 ✅ Linked or archived
├── scripts/
│   └── README.md                ✅ Links to docs
├── tests/
│   └── README.md                ✅ Links to docs
└── GEMINI.md                    ✅ Linked or archived
```

## Decision Tree for Orphans

```
┌─────────────────────────────┐
│   Orphaned File Detected    │
└──────────────┬──────────────┘
               │
               v
       ┌───────────────┐
       │ Is content    │
       │ current and   │ YES
       │ actively used?├─────────> Link to appropriate hub
       └───────┬───────┘           (docs/, scripts/, tests/)
               │ NO
               v
       ┌───────────────┐
       │ Is content    │
       │ historical or │ YES
       │ completed?    ├─────────> Move to archive/reversion-project/
       └───────┬───────┘           with README.md
               │ NO
               v
       ┌───────────────┐
       │ Is content a  │
       │ duplicate of  │ YES
       │ active file?  ├─────────> Delete after verification
       └───────┬───────┘           (check references first)
               │ NO
               v
       ┌───────────────┐
       │   Uncertain?  │
       │    STOP!      │──────────> Request human review
       └───────────────┘            Do NOT guess or delete
```

## Risk Mitigation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RISK MITIGATION LAYERS                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Git History                                       │
│  ┌────────────────────────────────────────────────────┐   │
│  │ All content in commit history (since 2024-10-24)   │   │
│  │ Can restore any file via: git checkout <sha> --    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  Layer 2: Git Tag (cleanup-baseline-2025-10-25)            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Instant rollback: git reset --hard <tag>           │   │
│  │ Selective restore: git checkout <tag> -- <path>    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  Layer 3: Working Branch                                   │
│  ┌────────────────────────────────────────────────────┐   │
│  │ All changes isolated from master                   │   │
│  │ Can abandon branch if issues arise                 │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  Layer 4: Validation Checkpoints                           │
│  ┌────────────────────────────────────────────────────┐   │
│  │ After each phase: Run audit scripts                │   │
│  │ Verify gates before proceeding                     │   │
│  │ STOP if unexpected results                         │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  Layer 5: Archive Preservation                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Nothing permanently deleted                        │   │
│  │ Historical content moved to archive/               │   │
│  │ Can restore from archive if needed                 │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Gate Compliance Architecture

```
BEFORE CLEANUP:
┌────────────────────────────┐
│   Gate Status: ❌ FAILING  │
├────────────────────────────┤
│ Broken links: 18 (❌ >0)   │
│ Hub violations: 1 (❌ >0)  │
│ Orphans: 11 (❌ >5)        │
└────────────────────────────┘

AFTER CLEANUP:
┌────────────────────────────┐
│   Gate Status: ✅ PASSING  │
├────────────────────────────┤
│ Broken links: ≤1 (✅ ≤1)   │
│ Hub violations: 0 (✅ =0)  │
│ Orphans: ≤5 (✅ ≤5)        │
└────────────────────────────┘

CI/CD Pipeline:
┌─────────────────────────────────────┐
│ lint-and-validate.yml               │
├─────────────────────────────────────┤
│ 1. generate-audit-reports.py       │
│ 2. Check structure-audit.json      │
│ 3. FAIL if gates violated           │
│ 4. Upload artifacts:                │
│    - linkcheck.txt                  │
│    - structure-audit.md/json        │
│    - hub-matrix.tsv                 │
└─────────────────────────────────────┘
```

## Execution Principles

```
┌─────────────────────────────────────────────────────────────┐
│                  ARCHITECTURAL PRINCIPLES                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ZERO BREAKAGE                                           │
│     No broken links, references, or functionality           │
│                                                             │
│  2. PRESERVE VALUE                                          │
│     Keep everything with current utility                    │
│     Archive everything with historical value                │
│                                                             │
│  3. EVIDENCE-BASED                                          │
│     Only remove what can be proven unnecessary              │
│     Document every decision with rationale                  │
│                                                             │
│  4. REVERSIBLE                                              │
│     Every action can be undone                              │
│     Git tag + branch + archive = full safety net            │
│                                                             │
│  5. VALIDATED                                               │
│     Run checks after every phase                            │
│     All gates must pass before merge                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Time Allocation

```
Total Time: ~80 minutes
┌────────────────────────────────────┐
│ Phase 1: Backup (5 min)        6%  │ ▓▓
│ Phase 2: Deletions (10 min)   12% │ ▓▓▓▓
│ Phase 3: Hubs (5 min)          6%  │ ▓▓
│ Checkpoint (5 min)             6%  │ ▓▓
│ Phase 4: Orphans (30 min)     38% │ ▓▓▓▓▓▓▓▓▓▓▓▓
│ Phase 5: Validation (10 min)  12% │ ▓▓▓▓
│ Phase 6: Docs (15 min)        19% │ ▓▓▓▓▓▓
└────────────────────────────────────┘
```

## Success Metrics

```
                BEFORE  →  AFTER  →  IMPROVEMENT
Broken Links:     18    →   ≤1    →    94% ↓
Hub Violations:    1    →    0    →   100% ✓
Orphans:          11    →   ≤5    →    55% ↓
Disk Space:     920KB   →    0    →  Freed ✓
Gate Status:      ❌    →    ✅    →  Pass ✓
```

---

**Architecture designed for safety, validation, and zero breakage.**
