# Cookiecutter ML Project Template

![Release](https://img.shields.io/github/v/tag/jtzanetatos/cookiecutter-ml-project?label=release)
![License](https://img.shields.io/badge/License-AGPL_v3-blue.svg)
![CI](https://img.shields.io/github/actions/workflow/status/jtzanetatos/cookiecutter-ml-project/cookiecutter-smoke.yml?label=smoke%20test)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Cookiecutter](https://img.shields.io/badge/cookiecutter-template-orange)

Cookiecutter template for creating production-oriented Python ML repositories with:

- Hydra configuration (`config/`)
- DVC scaffolding (`data/`, `dvc.yaml`)
- MLflow tracking + registry conventions
- Optional Triton model repository layout
- Docker + optional Kubernetes/Helm skeleton
- GitHub Actions workflows (tests/lint/type-check/etc.)
- `uv`-first dependency management (lockfile-based)

This repository is the **cookiecutter wrapper** around an ML template repo. It exists to generate new project repositories quickly and consistently.

---

## License Selection Guide

This template offers three license options. Choose carefully based on your goals:

| License | Type | Best For |
| :--- | :--- | :--- |
| **GPL-3.0** | Copyleft | Open source projects where you want to ensure all forks remain open source. |
| **AGPL-3.0** | Strong Copyleft | Web services / APIs. Prevents the "SaaS loophole" by requiring source code sharing even for network deployments. |
| **CC-BY-NC-4.0** | Non-Commercial | Research/Personal projects. source available, but prevents others from making money off your work. |

### Decision Flowchart

```mermaid
graph TD
    A["Start"] --> B{"Is source code sharing required?"}
    B -- Yes --> C{"Network Service?"}
    C -- Yes --> D["AGPL-3.0 (Strong Copyleft)"]
    C -- No --> E["GPL-3.0 (Copyleft)"]
    B -- No --> F{"Commercial use allowed?"}
    F -- No --> G["CC-BY-NC-4.0 (Non-Commercial)"]
    F -- Yes --> H["Consider MIT/Apache (Not in this template)"]
```

---

## Quick start

### 1) Environment Setup

This template provides a `environment.yaml` to ensure a deterministic environment with all necessary tools (cookiecutter, uv, etc.).

1. Clone this repository:
   ```bash
   git clone https://github.com/jtzanetatos/cookiecutter-ml-project.git
   cd cookiecutter-ml-project
   ```

2. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yaml
   conda activate template
   ```

3. (Optional) Install `just` command runner:
   ```bash
   ./tools/install_just.sh
   ```

### 2) Generate a new repository (interactive)

From wherever you want the new repo to be created:

```bash
cookiecutter gh:<owner>/cookiecutter-ml-project
```

Cookiecutter will prompt for values like:

- `repo_name`
- `project_title`
- `project_slug`
- `owner`

### 3) Generate non-interactively

```bash
cookiecutter gh:<owner>/<repo> --no-input \
  repo_name=my-ml-repo \
  project_slug=my_ml_repo \
  owner=acme \
  project_title="My ML Repo"
```

### 4) Choose output directory

Create the repo somewhere else:

```bash
cookiecutter gh:<owner>/<repo> -o /path/to/projects
```

---

## What gets generated

The generated project repository includes:

- `src/<project_slug>/` — production package
- `config/` — Hydra configuration groups
- `data/` — DVC-friendly structure
- `deployment/` — Docker, API skeleton, optional k8s/helm, Triton model repo layout
- `tests/` — unit/integration scaffolding
- `tools/` — repo hygiene scripts
- CI workflows preconfigured for `uv` and `uv.lock`

---

## Dependency management with uv

Generated repos are `uv`-first.

### Recommended workflow (generated repos)

Create and sync the environment:

```bash
uv sync --group dev
```

Run tests:

```bash
uv run pytest -m "not gpu and not slow"
```

Format + lint:

```bash
uv run ruff check . --fix
uv run ruff format .
```

Type check:

```bash
uv run mypy src
```

### Lockfile policy

Generated repos commit `uv.lock`. CI uses `uv sync` (locked install) for deterministic environments.

---

## GPU dependencies (opt-in)

GPU dependencies are defined as an optional extra in generated repos, but are **not installed by default**.

Example (generated repo):

```bash
uv pip install -e ".[gpu]" \
  --index https://download.pytorch.org/whl/cu130 \
  --index https://pypi.org/simple
```

CI never installs GPU extras.

---

## Docs build support (optional)

Generated repos can build docs if they include MkDocs or Sphinx config.

Docs tooling is expected to live in separate dependency groups so repos without docs don’t pay the dependency cost.

---

## Contributing & Maintenance

This repo is just a cookiecutter wrapper.

- **To update the template content** (sync from upstream, release, versioning, automated dependency updates), please see [CONTRIBUTING.md](CONTRIBUTING.md).
- **Maintenance scripts** are located in `tools/`.

---

## License

This cookiecutter template is licensed under AGPL-3.0 unless stated otherwise.

>License note
>This repository is licensed under AGPLv3.
>
>Projects generated using this template are not required to be licensed under AGPLv3.
>Users are free to choose any license for their generated projects.
>
>The AGPLv3 license applies to the template itself and any modifications or redistributions of the template.
