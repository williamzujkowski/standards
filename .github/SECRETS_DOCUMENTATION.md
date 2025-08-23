# GitHub Secrets Documentation

This document describes the GitHub Secrets required for various workflows in this repository.

## Required Secrets

### For NIST Compliance Badge (Optional)

To enable the NIST compliance badge that shows control coverage:

1. **GIST_SECRET**: A GitHub Personal Access Token with `gist` scope
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `gist` scope
   - Add as repository secret named `GIST_SECRET`

2. **GIST_ID**: The ID of a GitHub Gist to store badge data
   - Create a new secret gist at <https://gist.github.com>
   - Copy the ID from the URL (e.g., `https://gist.github.com/username/GIST_ID`)
   - Add as repository secret named `GIST_ID`

If these secrets are not configured, the badge creation step will be skipped automatically.

## Setting Repository Secrets

1. Go to repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add the secret name and value
4. Click "Add secret"

## Notes

- The workflows are designed to work without these secrets
- Badge creation only runs on pushes to the main branch
- All other NIST compliance checks will still run without these secrets
