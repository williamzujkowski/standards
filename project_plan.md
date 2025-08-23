# Project Plan the Agent Should Execute

## Phase 0 — Discovery (2–3 commits)

* Crawl and emit `standards-inventory.json` with stable IDs and codes (CS/TS/SEC/FE/WD/CN/DOP/DE/LEG/NIST-IG).
* Cross-check that inventory aligns with README categories and linked docs (UNIFIED\_STANDARDS, NIST guides, etc.). ([GitHub][1])

## Phase 1 — Product Matrix & Loading API (3–4 commits)

* Add `config/product-matrix.yaml` with curated, opinionated defaults (web-service, API, CLI, frontend-web, data-pipeline, ML-service, infra-module, doc-site, compliance-artifacts).
* Implement `@load` resolution examples in `CLAUDE.md` that pull from the matrix (support wildcards like `SEC:*` to expand to the current SEC bundle). ([GitHub][1])
* Add `docs/guides/USING_PRODUCT_MATRIX.md` (new) with three worked examples.

## Phase 2 — Kickstart & Router Alignment (2–3 commits)

* Update `docs/guides/KICKSTART_PROMPT.md` to explicitly say: “After the Tech Stack Analysis, call the Router with the resolved bundle from `config/product-matrix.yaml`,” and show the exact `@load` incantations. Keep your YAML/CLI output sections intact from the current kickstart format you pasted.
* In `CLAUDE.md`, add “Routing Contracts”: input schema, how product types map to standards, and how NIST is pulled when SEC is present.

## Phase 3 — NIST r5 Tightening (2–4 commits)

* Verify presence and functionality of `scripts/setup-nist-hooks.sh`; if absent or stale, add/update to align with README promises (automated control tagging, CI/CD checks). ([GitHub][1])
* Add `examples/nist-templates/quickstart/` with a minimal example demonstrating `@nist` annotations, the VS Code hint loop, and CI invocation.
* Add `prompts/nist-compliance/VALIDATION_RUN.md` with copy-paste instructions for local+CI proof.

## Phase 4 — Docs, QA, and CI (2–3 commits)

* `reports/generated/structure-audit.md` & `linkcheck.txt` added to PR.
* Ensure pre-commit, markdownlint, yamllint pass. If needed, minimally extend rules to cover new paths.
* Add/confirm GH Action: `lint-and-validate.yml` running pre-commit, linkcheck, and NIST validation quickstart.

## Phase 5 — PR & Handover (1 commit)

* Open a single PR bundling all changes with a reviewer checklist:

  * Inventory present and accurate
  * Product matrix loads resolve correctly
  * Kickstart ↔ Router handshake verified
  * NIST quickstart passes locally + CI
  * No broken links; linters green

---

## Strong Opinions / Guardrails (so it doesn’t drift)

* **One matrix to rule them all.** Don’t scatter mappings across prompts; **`config/product-matrix.yaml` is the source of truth** for product-type → standards bundles.
* **Router owns loading.** `CLAUDE.md` (your “CloudMD”) should be the only place that translates `@load` shorthands into concrete includes. ([GitHub][1])
* **NIST piggybacks security.** If a bundle contains `SEC:*`, auto-include `NIST-IG:base` and link to the NIST quickstart so people don’t “forget compliance” during SEC work. ([GitHub][1])
* **Everything generates artifacts.** If it isn’t in `reports/generated/`, it didn’t happen.

---

## Ready-to-Use Snippets the Agent Will Create

**`config/product-matrix.yaml` (new)**

```yaml
version: 1
defaults:
  include_nist_on_security: true
products:
  web-service: [CS:language, TS:framework, SEC:auth, SEC:secrets, FE/WD:api, DOP:ci-cd, OBS:monitoring, LEG:privacy, NIST-IG:base]
  api: [CS:language, TS:framework, SEC:auth, SEC:input-validation, DOP:ci-cd, OBS:monitoring, LEG:privacy, NIST-IG:base]
  frontend-web: [FE/WD:design-system, FE/WD:accessibility, CS:typescript, TS:vitest, SEC:auth-ui, DOP:ci-cd, OBS:web-vitals]
  data-pipeline: [DE:orchestration, DE:data-quality, SEC:secrets, SEC:data-classification, DOP:ci-cd, OBS:logging, LEG:data-retention, NIST-IG:base]
  ml-service: [DE:feature-store, TS:model-tests, SEC:model-risk, SEC:secrets, DOP:ci-cd, OBS:monitoring, LEG:privacy, NIST-IG:base]
  infra-module: [CN:container, DOP:iac, SEC:secrets, SEC:sbom, TS:integration, OBS:telemetry, NIST-IG:base]
  documentation-site: [KNOWLEDGE:info-arch, FE/WD:accessibility, DOP:ci-cd, OBS:links]
  compliance-artifacts: [COMPLIANCE:controls, NIST-IG:base, SEC:risk-mgmt, DOP:ci-cd]
```

**Kickstart addendum for `docs/guides/KICKSTART_PROMPT.md`**

```md
### Using the Standards Router (CLAUDE.md)
After Tech Stack Analysis, select a product type and resolve its bundle from `config/product-matrix.yaml`, then call the router:

@load [CS:python + TS:pytest + SEC:*]  # Example shorthand supported by the router
```

(References match the README’s `@load` convention and kickstart intent.) ([GitHub][1])

---

## Why this fits your repo (in short)

* You already advertise Kickstart, Router, and NIST tooling in README; this plan hooks them together with a single `product-matrix.yaml` so agents can auto-load standards consistently. ([GitHub][1])
* It keeps reports in `reports/generated/` per your file-organization guidance. ([GitHub][1])
* It fulfills the promise of `scripts/setup-nist-hooks.sh` and the `prompts/nist-compliance/` folder by providing a trivial, provable quickstart. ([GitHub][1])

If you want, I can also spit out the GitHub Actions workflow and a skeleton `examples/nist-templates/quickstart/` set (Makefile + sample code with `@nist` annotations) in the next pass.

[1]: https://github.com/williamzujkowski/standards "GitHub - williamzujkowski/standards"
