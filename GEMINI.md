# GEMINI.md

## Project Overview

This repository contains a comprehensive set of software development standards and tools designed to kickstart new projects with industry best practices and NIST guidelines. It emphasizes a "skills-based" approach, allowing users to load only the necessary standards for their specific project, which significantly reduces the amount of information a developer or an AI assistant needs to process.

The project is heavily geared towards automation and integration with AI assistants, providing scripts and templates to generate project structures, configuration files, CI/CD pipelines, and more.

The core technologies used in this project are Python for scripting and automation, and Markdown for documentation. The standards themselves are technology-agnostic, but the examples and templates provided cover a wide range of technologies including Python, React, and various cloud services.

## Building and Running

The project itself is not a library or application that you "run" in a traditional sense. Instead, it's a collection of standards, scripts, and templates.

### Documentation

The documentation is built using MkDocs. To build and serve the documentation locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Serve documentation locally (with live reload)
mkdocs serve
```

### Scripts

The `scripts/` directory contains numerous Python and shell scripts for various tasks. The most important one is the `skill-loader.py` script, which is used to load and recommend "skills" for a project.

```bash
# Get skill recommendations for your project
python3 scripts/skill-loader.py recommend ./

# Load recommended skills
python3 scripts/skill-loader.py load product:api
```

## Development Conventions

The project has a very strong set of development conventions, enforced by a comprehensive set of pre-commit hooks.

*   **Code Formatting:** `black` for Python, `prettier` for JSON, and `markdownlint` for Markdown.
*   **Linting:** `ruff` for Python, `eslint` for JavaScript/TypeScript, and `shellcheck` for shell scripts.
*   **Security:** `gitleaks` for secret detection.
*   **Testing:** `pytest` is used for testing the Python scripts.
*   **Pre-commit Hooks:** A wide range of pre-commit hooks are defined in `.pre-commit-config.yaml` to enforce formatting, linting, and security checks before committing code.

## AI Assistant Integration

This repository is designed to be used with AI assistants. The `CLAUDE.md` file provides a detailed guide for how an AI assistant named Claude should interact with the repository. The key takeaways for any AI assistant are:

*   **Skills System:** The repository uses a "skills-based" approach. Instead of reading all the documentation, the AI assistant should use the `scripts/skill-loader.py` script to load the relevant "skills" for a given task.
*   **File Organization:** There are strict rules for file organization. AI assistants should not save files to the root folder. Instead, they should use the appropriate subdirectories, such as `/src` for source code, `/tests` for tests, and `/docs` for documentation.
*   **Concurrent Execution:** The `CLAUDE.md` file emphasizes that all operations should be concurrent and parallel in a single message. This means batching file operations, shell commands, and other tasks together.
*   **Documentation Integrity:** There is a strong emphasis on documentation integrity. All claims must be verifiable and linked to primary evidence.
