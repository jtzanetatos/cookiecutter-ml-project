# Contributing

This repository is a **cookiecutter template**. Changes here affect every project generated from it.

## Repository layout

- `cookiecutter.json` — template variables and render rules (including `_copy_without_render`)
- `{{cookiecutter.repo_name}}/` — the generated project skeleton (the “payload”)
- `tools/` — maintenance scripts (syncing from upstream template repo, smoke tests)
- `.github/` — maintenance automation for *this* template repo (issue/PR templates, CI smoke test)

## Development setup

Install tooling (recommended via `uv`):

```bash
uv tool install cookiecutter
python -m pip install --upgrade pre-commit
pre-commit install
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

## Releasing the template

See README “Release process”.
