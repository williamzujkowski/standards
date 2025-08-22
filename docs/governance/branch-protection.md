# Branch Protection Settings

This document outlines the exact branch protection settings to enable for the `main` branch.

## Required Settings

Navigate to: **Settings → Branches → Add rule** (or edit existing rule for `main`)

Reference: [Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

### 1. Branch name pattern

- Pattern: `main`

### 2. Protect matching branches

#### **Require a pull request before merging**

- ✅ Enable
- **Required approvals**: `1` (minimum)
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ✅ **Require review from CODEOWNERS**

#### **Require status checks to pass before merging**

- ✅ Enable
- ✅ **Require branches to be up to date before merging**
- **Required status checks:**
  - `Markdown Linting`
  - `Link Validation`
  - `OpenSSF Scorecard`
  - `Verify Claim Anchors`
  - `Validate Standards Registry`

#### **Require conversation resolution before merging**

- ✅ Enable (ensures all PR comments are resolved)

#### **Require signed commits** (optional but recommended)

- ✅ Enable if your team uses commit signing

#### **Include administrators**

- ✅ Enable (applies rules even to admins)

### 3. Rules for administrators

#### **Allow force pushes**

- ❌ **Disable** (never allow force pushes to main)

#### **Allow deletions**

- ❌ **Disable** (prevent accidental branch deletion)

## Additional Recommendations

### Suggested Settings

1. **Require linear history** - Prevents merge commits, keeps history clean
2. **Require deployments to succeed** - If using deployment workflows
3. **Lock branch** - For archived/frozen branches (not for active `main`)

### Security Best Practices

- Regularly review CODEOWNERS file
- Audit branch protection bypass permissions
- Enable security alerts for the repository
- Use rulesets for more granular control (GitHub Enterprise)

## Verification

After configuring, verify settings by:

1. Creating a test PR without required checks
2. Attempting to push directly to main (should fail)
3. Checking that status checks are enforced

## References

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [About CODEOWNERS](https://docs.github.com/articles/about-code-owners)
