# Python Project Standard Setup

This document describes the standard setup for a new Python project.

## 1. Dependency Management and Configuration (`pyproject.toml`)

We use `pyproject.toml` to manage project metadata, dependencies, and tool configurations.

### Development Dependencies

The following tools are used for development:
- `ruff`: for linting and formatting
- `black`: for code formatting
- `pytest`: for testing

Add them to the `[project.optional-dependencies]` section:

```toml
[project.optional-dependencies]
dev = [
    "pre-commit",
    "ruff",
    "black",
    "pytest",
]
```

### Tool Configuration

Configure `black`, `ruff`, and `pytest` within `pyproject.toml`.

- **`black` and `ruff`**: Set `line-length` to 120 for consistency.
- **`pytest`**: Specify the test directory.

```toml
[tool.black]
line-length = 120

[tool.ruff]
line-length = 120

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## 2. Task Runner (`justfile`)

We use `just` as a command runner for common tasks like formatting, linting, and setting up the environment.

Create a `justfile` in the project root:

```justfile
# justfile

# Default task
default:
    @just --list

# Setup the local development environment
setup:
    uv venv
    uv pip install -e '.[dev]'

# Run the linter
lint:
    uv run ruff check .

# Fix linting issues automatically
fix:
    uv run ruff check . --fix
    uv run black .

# Run tests
test:
    uv run pytest
```

## 3. Pre-commit Hooks

To ensure code quality before committing, we use `pre-commit`.

Create a `.pre-commit-config.yaml` file in the project root:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
    -   id: ruff
        args: [--fix]
    -   id: ruff-format

-   repo: https://github.com/psf/black-pre-commit-mirror
    rev: 24.4.2
    hooks:
    -   id: black
```

### Pre-commit Installation and Usage

1.  Install `pre-commit`:
    ```bash
    pip install pre-commit
    ```

2.  Install the git hooks:
    ```bash
    pre-commit install
    ```

Now, the hooks will run automatically on `git commit`.
