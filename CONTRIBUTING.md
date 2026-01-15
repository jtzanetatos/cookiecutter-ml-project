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
conda env create -f environment.yaml
conda activate template
./tools/install_just.sh  # Optional
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

Recommended process:

1. Ensure `Cookiecutter Smoke Test` CI is green on `main`.
2. Update `CHANGELOG.md` (template-level) with user-facing changes.
3. Tag a release:

```bash
git tag -a vX.Y.Z -m "cookiecutter template vX.Y.Z"
git push origin vX.Y.Z
```

4. (Optional) Create a GitHub Release for the tag and paste the changelog notes.

Notes:

- Generated projects are versioned separately in their own repositories.
- Template tags communicate “what changed in the generator”, not in any particular generated repo.

## Versioning

This cookiecutter template can be versioned and tagged independently. Tag releases with `vX.Y.Z`.

