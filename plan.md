# plan.md — Standards repo audit, re-org, and hardening

## Completed (2025-08-22)

### Initial Reorganization

✅ **Repository reorganization** - Created clean `/standards/{nist,owasp,supply-chain,cisa}/` structure
✅ **YAML front-matter** - Added to all standards pages with required metadata
✅ **CI/CD workflows** - Implemented markdownlint, lychee link checker, OpenSSF Scorecard
✅ **CLAIMS.md** - Created with anchored normative claims, enforced via `claims-anchors` job
✅ **SLSA v1.0** - Added retired status notice
✅ **SLSA v1.1** - Created current version page
✅ **in-toto** - Added supply chain attestation framework page
✅ **CycloneDX** - Created with ECMA-424 reference
✅ **CISA pages** - Added Secure by Design and KEV process
✅ **Core NIST standards** - SP 800-53r5, 800-171r3, 800-218 SSDF, AI RMF 1.0, GenAI Profile
✅ **OWASP standards** - Top 10 2021, API Top 10 2023

### Final Enhancements

✅ **Standards registry** - Machine-readable index with validation (`/standards/registry.json`)
✅ **Standards index page** - Human-readable directory (`/docs/standards/index.md`)
✅ **Dependabot** - Configured for GitHub Actions updates
✅ **Contributor templates** - PR and issue templates
✅ **OSCAL scaffolding** - Near-term work defined with actionable steps

### Governance & Monitoring (2025-08-22)

✅ **CODEOWNERS** - Defined ownership for standards, docs, and CI paths
✅ **Branch protection docs** - Exact settings documented in `/docs/governance/branch-protection.md`
✅ **OpenSSF Scorecard badge** - Added to README with proper v2 configuration
✅ **Release Drafter** - Automated changelog generation with categories
✅ **KEV watcher** - Daily monitoring of CISA KEV catalog with issue creation
✅ **Watchers documentation** - Explains KEV monitoring and opt-out for forks
✅ **OWASP Top 10 2025 radar** - Tracking document for upcoming release

## Maintenance

### Quarterly Reviews (Next: 2025-11-22)

* Review and update all standards pages
* Verify primary source URLs
* Update CLAIMS.md with new requirements
* Check for new NIST/OWASP/CISA publications

### Continuous Monitoring

* **KEV Catalog** - Daily automated check via GitHub Actions
* **Link validation** - Daily scheduled workflow
* **OpenSSF Scorecard** - Per-PR and push analysis
* **OWASP Top 10 2025** - Quarterly manual check (next: 2025-11-22)

## Objectives

* **Make the repo LLM-first** (clear structure, rich context, consistent metadata) without dumbing it down.
* **Fix and future-proof workflows** (linting, link checks, security hygiene).
* **Verify every normative claim** against primary sources; flag unknowns.
* **Identify and scaffold high-value standards you're missing** (NIST, OWASP, SLSA, SBOM, CISA, etc.), with citations.

> Tooling: Use **Claude Code CLI** as the execution engine; optionally orchestrate steps via **claude-flow** (alpha). If claude-flow flakes, fall back to the CLI steps below. (claude-flow’s workflow commands are still placeholders as of issue #578.) ([Anthropic][1])

---

## Repo shape (target)

```
/
├─ README.md
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ /standards/
│  ├─ nist/
│  │  ├─ sp800-53r5.md     # control catalog overview + crosswalk pointers
│  │  ├─ sp800-171r3.md    # CUI requirements
│  │  ├─ sp800-218-ssdf.md # secure SDLC
│  │  └─ ai-rmf-1.0.md     # risk mgmt for AI
│  ├─ owasp/
│  │  ├─ top10-2021.md
│  │  └─ api-top10-2023.md
│  ├─ supply-chain/
│  │  ├─ slsa-1.0.md
│  │  ├─ cyclonedx-sbom.md
│  │  └─ in-toto.md
│  ├─ cisa/
│  │  ├─ secure-by-design.md
│  │  └─ kev-process.md
│  └─ _templates/
│     └─ standard-template.md
├─ /docs/                  # narrative guides, playbooks, crosswalks
├─ /prompts/               # LLM prompts (repo-aware); see prompt file below
├─ /mcp/                   # optional MCP server configs/tools
├─ .github/
│  └─ workflows/           # lint + links + scorecard + (optional) CodeQL
└─ .claude/                # CLI config + reusable commands
```

**Front-matter** for every standards page:

```yaml
---
title: "NIST SP 800-53 Rev. 5 — Overview"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://doi.org/10.6028/NIST.SP.800-53r5"
  retrieved: "2025-08-21"
review:
  last_reviewed: "2025-08-21"
  next_review_due: "2026-02-21"
accuracy: "verified"
---
```

---

## Step-by-step (CLI-first, claude-flow optional)

### 0) Install/update Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code  # or native install per docs
claude update
```

(Install/quickstart refs.) ([Anthropic][2])

### 1) Prime the repo for LLMs

* Add `.claude/settings.json` to whitelist read-only commands; prefer **plan** permission mode for dry-runs.
* Create `.claude/commands/` one-shot tasks (e.g., `audit-standards.md`, `fix-workflows.md`).

### 2) Run the **Repo Audit** (use the prompt below with `claude -p`)

* Inventory files; normalize names; generate missing front-matter.
* Build `CLAIMS.md` (machine-extracted normative statements) with **empty** citation slots.
* Auto-populate citations from **primary sources only** (NIST, OWASP, CISA, SLSA, OpenSSF, CycloneDX); anything unverified → `UNKNOWN` and opened as an issue.

### 3) Add/upgrade core standards (authoritative sources)

* **NIST SP 800-53 Rev.5** (control catalog). ([NIST Publications][3], [NIST Computer Security Resource Center][4], [NIST CSRC][5])
* **NIST SP 800-171 Rev.3** (CUI). ([NIST Publications][6], [NIST Computer Security Resource Center][7])
* **NIST SP 800-218 (SSDF v1.1)**. ([NIST Publications][8], [NIST Computer Security Resource Center][9])
* **NIST AI RMF 1.0** (+ Generative AI Profile). ([NIST Publications][10], [NIST][11])
* **OWASP Top 10: 2021**; **OWASP API Top 10: 2023**. ([OWASP Foundation][12])
* **SLSA 1.0** (levels/tracks; provenance). ([SLSA][13])
* **CycloneDX SBOM** (ECMA-424). ([CycloneDX][14], [GitHub][15])
* **in-toto** (attestations). ([in-toto][16], [GitHub][17])
* **CISA Secure by Design** & **KEV process** (use KEV to drive patch SLAs).

### 4) Fix workflows (minimum viable, fast, and loud)

Create `.github/workflows/standards-ci.yml`:

```yaml
name: Standards CI
on:
  pull_request:
  push: { branches: [main] }
  schedule: [{ cron: "17 6 * * *" }]  # daily link check
permissions:
  contents: read
  security-events: write
jobs:
  markdownlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@vX   # pin latest
        with:
          globs: "**/*.md"
  links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@vX
        with:
          args: --verbose --no-progress --accept 403,429 --exclude-mail
        env:
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
  scorecard:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      security-events: write
    steps:
      - uses: ossf/scorecard-action@v2
        with:
          results_file: results.sarif
          results_format: sarif
          publish_results: true
```

Refs: markdownlint-cli2 action, lychee, Scorecard action. ([GitHub][18])
(Optional for code repos) add **CodeQL** with Actions queries. ([GitHub][19], [GitHub Docs][20])

### 5) MCP (optional, but powerful)

If you want Claude to fetch ground truth itself, add MCP servers (e.g., HTTP fetcher, your standards index, or your own **mcp-standards-server**). Configure via `claude mcp` per docs. ([Anthropic][21])

### 6) Deliverables

* Clean structure + metadata.
* `CLAIMS.md` with live citations or `UNKNOWN`.
* Up-to-date standards pages seeded from authoritative sources.
* Passing CI on lint + links + scorecard.
* Issues opened for anything unverified or stale.

---

## What “done” looks like

* No broken links; markdownlint clean; scorecard published and ≥8/10 on basics (pinned actions, branch protection, CodeQL if code exists). ([GitHub][22], [Open Source Security Foundation][23])
* Every standards page shows **source URL, retrieval date, and next review**.
* `CLAIMS.md` has **zero** `UNKNOWN` entries (or they’re ticketed with due dates).

---

[1]: https://docs.anthropic.com/en/docs/claude-code/common-workflows?utm_source=chatgpt.com "Common workflows"
[2]: https://docs.anthropic.com/en/docs/claude-code/quickstart "Quickstart - Anthropic"
[3]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf?utm_source=chatgpt.com "NIST.SP.800-53r5.pdf"
[4]: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final?utm_source=chatgpt.com "NIST SP 800-53 Rev. 5 \"Security and Privacy Controls for ..."
[5]: https://csrc.nist.rip/publications/detail/sp/800-53/rev-5/final?utm_source=chatgpt.com "SP 800-53 Rev. 5, Security and Privacy Controls for ... - CSRC"
[6]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf?utm_source=chatgpt.com "NIST.SP.800-171r3.pdf"
[7]: https://csrc.nist.gov/pubs/sp/800/171/r3/final?utm_source=chatgpt.com "SP 800-171 Rev. 3, Protecting Controlled Unclassified ..."
[8]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf?utm_source=chatgpt.com "Secure Software Development Framework (SSDF) Version 1.1"
[9]: https://csrc.nist.gov/pubs/sp/800/218/final?utm_source=chatgpt.com "Secure Software Development Framework (SSDF) Version 1.1 ..."
[10]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf?utm_source=chatgpt.com "[PDF] Artificial Intelligence Risk Management Framework (AI RMF 1.0)"
[11]: https://www.nist.gov/itl/ai-risk-management-framework?utm_source=chatgpt.com "AI Risk Management Framework | NIST"
[12]: https://owasp.org/Top10/?utm_source=chatgpt.com "OWASP Top 10:2021"
[13]: https://slsa.dev/spec/v1.0/?utm_source=chatgpt.com "SLSA specification"
[14]: https://cyclonedx.org/?utm_source=chatgpt.com "CycloneDX Bill of Materials Standard | CycloneDX"
[15]: https://github.com/CycloneDX?utm_source=chatgpt.com "CycloneDX BOM Standard"
[16]: https://in-toto.io/?utm_source=chatgpt.com "in-toto"
[17]: https://github.com/in-toto/attestation?utm_source=chatgpt.com "in-toto Attestation Framework"
[18]: https://github.com/DavidAnson/markdownlint-cli2-action?utm_source=chatgpt.com "DavidAnson/markdownlint-cli2-action"
[19]: https://github.com/github/codeql-action?utm_source=chatgpt.com "GitHub - github/codeql-action: Actions for running CodeQL analysis"
[20]: https://docs.github.com/en/enterprise-cloud%40latest/code-security/code-scanning/managing-your-code-scanning-configuration/actions-built-in-queries?utm_source=chatgpt.com "Actions queries for CodeQL analysis - GitHub Docs"
[21]: https://docs.anthropic.com/en/docs/claude-code/cli-reference "CLI reference - Anthropic"
[22]: https://github.com/ossf/scorecard?utm_source=chatgpt.com "ossf/scorecard - Security health metrics for Open Source"
[23]: https://openssf.org/projects/scorecard/?utm_source=chatgpt.com "OpenSSF Scorecard – Open Source Security Foundation"
