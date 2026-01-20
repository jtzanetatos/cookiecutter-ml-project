# Contributing

This repository is a **cookiecutter template**. Changes here affect every project generated from it.

## Repository layout

- `cookiecutter.json` — template variables and render rules (including `_copy_without_render`)
- `{{cookiecutter.repo_name}}/` — the generated project skeleton (the “payload”)
- `tools/` — maintenance scripts (syncing from upstream template repo, smoke tests)
- `.github/` — maintenance automation for *this* template repo (issue/PR templates, CI smoke test)

## Development setup

Install tooling using the provided environment (recommended):

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dev dependencies
uv sync
```


## Making changes

### Option A (recommended): upstream template → sync into cookiecutter

1. Make changes in the upstream (plain) template repo.
2. Sync into this cookiecutter repo:

```bash
make sync SRC=/abs/path/to/ml-project-template
```

3. Run the smoke test:

```bash
make smoke SRC=/abs/path/to/ml-project-template OUT=../_generated
```

4. Commit changes and open a PR.

### Option B: edit directly in `{{cookiecutter.repo_name}}/`

Allowed, but you must ensure:

- cookiecutter placeholders are preserved (`{{cookiecutter.project_slug}}`, etc.)
- `_copy_without_render` is updated if you add Helm / Actions templates
- the smoke test still passes

## Commit Message Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) to automate versioning and changelogs.

**Format**: `type(scope): subject`

**Common types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to our CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files
- `revert`: Reverts a previous commit

**Examples**:
- `feat(ci): add release workflow`
- `fix(template): correct path in dockerfile`
- `docs: update contributing guide`

> **Note**: This is enforced locally via `pre-commit` hooks. If you attempt to commit a message that doesn't follow this standard, the commit will be rejected.

## Testing

### CI (required)

PRs must pass the cookiecutter smoke workflow.

### Local (recommended)

```bash
make smoke SRC=/abs/path/to/ml-project-template OUT=../_generated
```

## Style / hygiene

- Keep template changes minimal and predictable.
- Avoid introducing Jinja-like sequences `{{ ... }}` inside template payload files unless they are cookiecutter placeholders.
- If you add Helm templates or GitHub Actions workflow files under the payload, ensure they are covered by `_copy_without_render`.


## Template maintenance workflow

This repo is intended to be kept in sync with an upstream “plain template repo”.

### Sync upstream template → cookiecutter template directory

```bash
./tools/sync_template_into_cookiecutter.sh /abs/path/to/ml-project-template
```

### Sync + smoke test generation

```bash
./tools/sync_and_smoke_test.sh /abs/path/to/ml-project-template
```

### Update template dependencies

The repository contains a custom automation to keep template dependencies (Python packages, GitHub Actions) fresh, effectively acting as a "Dependabot" for the template content.

- **Automated**: Runs daily via the [Template Dependency Updates](.github/workflows/template-dependency-updates.yml) workflow.
- **Manual**: You can run the underlying script locally:

```bash
python tools/update_dependencies.py
```

## Notes on templating and copy-without-render

Some files contain template-like syntax that must **not** be rendered by Jinja (Helm charts, GitHub Actions expressions like `${{ ... }}`, etc.). Those must be listed in `cookiecutter.json` under `_copy_without_render`.

## Release process (template repo)

This repository is versioned independently as a **template**.

Release process is **fully automated** using GitHub Actions and Commitizen.

### How it works

1.  Merge your changes to `main`.
2.  The [Release](.github/workflows/release.yml) workflow triggers.
3.  It calculates the next version based on your commit messages (e.g., `feat` -> minor bump, `fix` -> patch bump).
4.  It creates a new tag, updates `CHANGELOG.md`, and creates a GitHub Release.

### Manual triggers

You do **not** need to manually tag releases. Just ensure your commit messages are correct.

4. (Optional) Create a GitHub Release for the tag and paste the changelog notes.

Notes:

- Generated projects are versioned separately in their own repositories.
- Template tags communicate “what changed in the generator”, not in any particular generated repo.

## Versioning

This cookiecutter template can be versioned and tagged independently. Tag releases with `vX.Y.Z`.

