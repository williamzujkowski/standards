# Claude Flow Project Plan

Absolutely. Here's a **Claude-Flow–ready project plan** tailored to your actual stack (11ty, Tailwind, custom JS, Node, GitHub Pages) — **no Vale,

## 🧭 Project Plan: `CLAUDE.md` v3.1 + Skills Pilot for Humanized, Accurate Content

**Project Name:** CLAUDE Governance v3.1 (Site-Only Stack)
**Owner:** William Zujkowski
**Repo:** `williamzujkowski.github.io`
**Stack:** 11ty, Tailwind CSS, Node, custom JS, GitHub Pages
**Revision:** 1.1 (site-only)
**Date:** 2025-10-24

## 🎯 Objectives

1. **Preserve** enforcement + SPARC orchestration in `CLAUDE.md` (single source of truth).
2. **Humanize** writing: Linus-ish tone + Smart Brevity + anti-AI tells (no em dashes/semicolons, no hype).
3. **Guarantee accuracy**: explicit **No Exaggeration / No Hallucinations** policy, with in-repo checks (no external services).
4. **Pilot Skills** (`docs/SKILLS.md` + `skills/*`) that map to your repo tasks and run **locally** without external infra.
5. **Stay stack-pure**: only Node + simple scripts; CI via GitHub Actions if desired.

---

## 🧩 Scope

| Area        | In Scope                                                                   | Out of Scope                  |
| ----------- | -------------------------------------------------------------------------- | ----------------------------- |
| `CLAUDE.md` | Update to v3.1 with tone + accuracy guardrails                             | Removing enforcement sections |
| Blog style  | Anti-AI tells + Smart Brevity                                              | Marketing copy generators     |
| Skills      | `blog-style`, `research-citations`, `images-pipeline`, `enforcement-guard` | External APIs/services        |
| CI          | Optional GitHub Actions: link check & lint                                 | Third-party SaaS integrations |

---

## ⚙️ Deliverables

* `CLAUDE.md` **v3.1 (authoritative)** — includes:

  * Human voice rules (Linus-ish tone, Smart Brevity)
  * **Accuracy/No-Hallucinations** section with must/should rules
  * Anti-AI-tells (no em dashes/semicolons; anti-hype; fragments ok)
  * Enforcement: no root writes, MANIFEST update, timestamp rules, concurrency batching
* `docs/SKILLS.md` (pilot spec) — maps repo workflows to Claude **Agent Skills**
* `skills/blog-style/`

  * `skill.yaml`, `prompts/style.md`, `prompts/anti-ai-tells.md`
* `skills/research-citations/`

  * `skill.yaml`, `prompts/sourcing.md`, `scripts/local-claims-check.js`
* `skills/images-pipeline/`

  * `skill.yaml`, `scripts/update-images.sh`, `scripts/optimize-images.sh` (thin wrappers around existing scripts)
* `skills/enforcement-guard/`

  * `skill.yaml`, `scripts/verify-manifest.sh`, `scripts/check-duplicates.sh`
* `reports/claude-refactor-validation.md` (one-time output from CI/local run)
* `MANIFEST.json` updated (paths + timestamps)

> All scripts are **local**; Node/bash preferred. Python optional but not required.

---

## 🔒 Accuracy / No Exaggeration / No Hallucinations (Authoritative Policy)

Embed this section into `CLAUDE.md`:

* **No Fabrication:** If a claim cannot be verified from **primary docs** or reputable sources, **omit it** or mark as observation (“In my lab…”).
* **No Exaggeration:** Ban hype words (e.g., “revolutionary,” “game-changer”), vague adverbs (“significantly”) **unless** paired with data (e.g., “23%”).
* **Citations on First Mention:** Link **inline** to official docs, standards, or papers (DOI/arXiv). If none exist, call it an opinion.
* **Refusal to Guess:** If uncertain, write: *“Unknown. Not enough data.”* or *“We haven’t tested this.”*
* **Trade-offs Required:** Every recommendation must include risks/limits.
* **Temporal Clarity:** Use explicit dates (“2025-10-24”) when recency matters.
* **Sanity Check:** Before publish, run **Local Claims Check** (below).
* **Tone:** Skeptical, practical, concise. Strong opinions, **weakly held**.

### Local Claims Check (no external tools)

* **Rules:** Simple regex + heuristics to flag:

  * Banned tokens: em dash (—), semicolon (;), hype/buzzwords list, adverb list
  * Claims that look numeric without a link nearby
  * Sections missing “Trade-offs” or “Why it matters”
* **Command (Node):**

  ```bash
  node skills/research-citations/scripts/local-claims-check.js src/posts/<file>.md
  ```

* **Outcome:** Warnings with line numbers; block commit if “high-severity” issues exist (configurable).

---

## 🧠 SPARC Phases (Claude-Flow)

| Phase            | Mode                        | Output                                                                |
| ---------------- | --------------------------- | --------------------------------------------------------------------- |
| 1. Specification | `sparc run spec-pseudocode` | Draft updated `CLAUDE.md` outline + Skills map                        |
| 2. Pseudocode    | `sparc run spec-pseudocode` | Pseudocode for skills, hooks, and local checks                        |
| 3. Architecture  | `sparc run architect`       | Create `skills/*`, wire scripts (Node/bash), update MANIFEST          |
| 4. Refinement    | `sparc tdd`                 | Run local claims check, style enforcement, image pipeline smoke tests |
| 5. Completion    | `sparc run integration`     | CI (optional), build site, produce validation report, tag v3.1.0      |

---

## 🪜 Detailed Tasks

### Phase 1 — Specification

* [ ] Parse current `CLAUDE.md`; list sections to keep; add new **Accuracy** section.
* [ ] Define anti-AI-tells + Smart Brevity template.
* [ ] Define local claims check rules + banned token list.
* [ ] Produce Skills inventory & minimal YAML contract.

### Phase 2 — Pseudocode

* [ ] Draft `CLAUDE.md` v3.1 structure (enforcement preserved).
* [ ] Pseudocode for `local-claims-check.js`:

  * Parse Markdown → tokens
  * Check banned chars/tokens
  * Find numbers without nearby links
  * Verify headings include “Trade-offs” + “Why it matters”
  * Exit code 0/1 based on thresholds
* [ ] Pseudocode for `verify-manifest.sh` & `check-duplicates.sh`.

### Phase 3 — Architecture

* [ ] Create folders and stubs:

  ```
  docs/SKILLS.md
  skills/blog-style/{skill.yaml,prompts/style.md,prompts/anti-ai-tells.md}
  skills/research-citations/{skill.yaml,prompts/sourcing.md,scripts/local-claims-check.js}
  skills/images-pipeline/{skill.yaml,scripts/update-images.sh,scripts/optimize-images.sh}
  skills/enforcement-guard/{skill.yaml,scripts/verify-manifest.sh,scripts/check-duplicates.sh}
  ```

* [ ] Update `MANIFEST.json` (paths, `last_validated`).
* [ ] Ensure **write_paths** in each `skill.yaml` restrict to `src/posts` & `docs`.

### Phase 4 — Refinement

* [ ] Run local claims check on 2–3 existing posts; tune thresholds.
* [ ] Enforce anti-AI-tells via `blog-style` skill prompts + regex checks.
* [ ] Smoke-test image pipeline wrappers (just call your existing scripts if present; else no-op).
* [ ] Optionally add Node tooling:

  * `markdownlint-cli` for structure
  * `prettier` for md normalization
    (No external services; pure npm.)

### Phase 5 — Completion

* [ ] `npm run build` (11ty) succeeds.
* [ ] Produce `reports/claude-refactor-validation.md`:

  * Posts checked, warnings count, fixes applied
  * Accuracy policy compliance summary
* [ ] Commit + tag `v3.1.0`.

---

## 🧰 Minimal Skill Templates (local-only)

### `skills/blog-style/skill.yaml`

```yaml
name: blog-style
version: 1.0.0
description: Enforce human voice, Smart Brevity, and anti-AI-tells for posts.
entrypoints:
  - type: instruction
    path: prompts/style.md
  - type: instruction
    path: prompts/anti-ai-tells.md
constraints:
  write_paths:
    - "src/posts/"
    - "docs/"
```

### `skills/blog-style/prompts/style.md` (excerpt)

* Write like a seasoned IT/security engineer; skeptical, direct, concise.
* Smart Brevity structure: **TL;DR**, **Trade-offs**, **Why it matters**, **Go deeper**.
* Short paragraphs (1–3 sentences), bullets over walls of text.
* Use contractions and allow fragments if clear.

### `skills/blog-style/prompts/anti-ai-tells.md`

* **Ban:** em dashes (—), semicolons (;), hype words, mirrored symmetry.
* Avoid vague adverbs unless paired with data.
* Prefer numbers to adjectives; include one skeptical caveat.

### `skills/research-citations/skill.yaml`

```yaml
name: research-citations
version: 1.0.0
description: Local claims checks for accuracy without external services.
entrypoints:
  - type: instruction
    path: prompts/sourcing.md
capabilities:
  - read
  - suggest
hooks:
  after:
    - "node skills/research-citations/scripts/local-claims-check.js ${POST_PATH:-src/posts/*.md}"
constraints:
  write_paths:
    - "src/posts/"
    - "docs/"
```

### `skills/research-citations/prompts/sourcing.md` (excerpt)

* Prefer primary docs and standards.
* Inline link on first mention; mark opinions clearly.
* If uncertain, say so. Do not guess.

### `skills/research-citations/scripts/local-claims-check.js` (outline)

```js
#!/usr/bin/env node
// 1) Read file(s)
// 2) Flag banned tokens: '—', ';'
// 3) Flag hype words (list in this file)
// 4) Find numbers lacking a link within N chars
// 5) Ensure sections include "Trade-offs" and "Why it matters"
// 6) Print warnings with line numbers; exit 1 on high severity
```

### `skills/images-pipeline/skill.yaml`

```yaml
name: images-pipeline
version: 1.0.0
description: Local image metadata + optimization wrappers (no external deps).
entrypoints: []
constraints:
  write_paths:
    - "src/assets/images/blog/"
    - "src/posts/"
```

### `skills/images-pipeline/scripts/update-images.sh`

```bash
#!/usr/bin/env bash
# Thin wrapper. If your existing scripts exist, call them; else no-op.
[ -x scripts/blog-images/update-blog-images.py ] && \
  python3 scripts/blog-images/update-blog-images.py || true
```

### `skills/images-pipeline/scripts/optimize-images.sh`

```bash
#!/usr/bin/env bash
# Optional: run imagemin via npm if available, else no-op
[ -f package.json ] && npx --yes imagemin-cli ./src/assets/images/blog/* --out-dir=./src/assets/images/blog || true
```

### `skills/enforcement-guard/skill.yaml`

```yaml
name: enforcement-guard
version: 1.0.0
description: Protects against root writes and duplicate files.
hooks:
  before:
    - "bash skills/enforcement-guard/scripts/verify-manifest.sh"
  after:
    - "bash skills/enforcement-guard/scripts/check-duplicates.sh"
constraints:
  write_paths:
    - "src/"
    - "docs/"
    - "skills/"
    - "reports/"
```

### `skills/enforcement-guard/scripts/verify-manifest.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
# Ensure MANIFEST.json changed in the same commit when files added/removed
# (Implement a simple diff check or a git status grep)
exit 0
```

### `skills/enforcement-guard/scripts/check-duplicates.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
# Grep for duplicate slugs/filenames in src/posts
exit 0
```

---

## 🧪 Optional GitHub Actions (local-friendly)

Add a simple CI to run **local** checks only (no external API):

* `node skills/research-citations/scripts/local-claims-check.js`
* `npx markdownlint **/*.md`
* `npm run build` (11ty)
* (Optional) `npx linkinator ./_site --timeout=5000` (works offline on built site)

---

## 🧮 Success Criteria

| Metric                                         | Target         |
| ---------------------------------------------- | -------------- |
| `CLAUDE.md` v3.1 committed & enforced          | ✅              |
| Anti-AI-tells violations                       | **0** blocking |
| Numbers-without-link warnings                  | **0**          |
| Posts with **Trade-offs** + **Why it matters** | **100%**       |
| Build succeeds locally & in CI                 | ✅              |
| Skills run in suggest mode                     | ✅              |

---

## 🧰 Claude-Flow Command Handoff

```bash
# Pipeline orchestration
npx claude-flow sparc pipeline "Implement CLAUDE.md v3.1 + Skills pilot (site-only)"

# 1) Spec
npx claude-flow sparc run spec-pseudocode "Outline accuracy policy + tone rules + skills"

# 2) Pseudocode
npx claude-flow sparc run spec-pseudocode "Draft local-claims-check.js, verify-manifest.sh"

# 3) Architecture
npx claude-flow sparc run architect "Create skills folders, stubs, and update MANIFEST.json"

# 4) Refinement
npx claude-flow sparc tdd "Run claims check + anti-AI-tells on sample posts; fix"

# 5) Completion
npx claude-flow sparc run integration "Build site, produce validation report, tag v3.1.0"
```

---

## ✅ Definition of Done

1. `CLAUDE.md` v3.1 includes the **Accuracy / No Hallucinations** regime and anti-AI-tells.
2. `docs/SKILLS.md` + four `skills/*` folders exist with minimal local-only scripts.
3. Local claims check passes on representative posts.
4. Site builds locally (11ty) and (optionally) in CI.
5. `MANIFEST.json` updated; `reports/claude-refactor-validation.md` generated.
6. Tag `v3.1.0` pushed.
