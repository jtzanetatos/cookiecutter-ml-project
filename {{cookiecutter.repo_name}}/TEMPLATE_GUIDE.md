# ML Project Template – Guide

This document explains **how to use and extend this template correctly**.
It is intended for engineers creating *new projects from the template*, not for end users of a specific ML model.

This template enforces **production-grade ML engineering practices** while remaining flexible for research and experimentation.

---

## Template Philosophy

This template is built around the following principles:

- **Single source of truth for configuration** (Hydra)
- **Clear separation of concerns**
- **Reproducibility over convenience**
- **CI/CD owns promotion and deployment**
- **Same model → multiple deployment targets**
- **No magic, no hidden state**

---

## High-Level Stack

- **Hydra** — configuration management
- **MLflow** — experiment tracking & model registry (alias-based lifecycle)
- **DVC** — optional data versioning & pipeline orchestration
- **FastAPI** — flexible inference API
- **Triton Inference Server** — high-performance inference
- **Docker / Kubernetes** — runtime environments
- **Woodpecker CI** — linting, testing, promotion
- **Loguru / stdlib logging**
- **Jupyter** — exploration only

---

## Repository Structure (Canonical)

```text
.
├── config/                 # Hydra configs (single source of truth)
├── data/                   # Data layout (DVC-tracked)
├── deployment/             # All serving & deployment artifacts
│   ├── api/                # FastAPI service
│   ├── docker/             # Dockerfiles & compose
│   ├── dashboards/         # Streamlit / NiceGUI (optional)
│   ├── k8s/                # Kubernetes / Helm (service-level)
│   └── triton/             # Triton model repository + export helpers
├── docs/                   # ADRs, design docs, figures
├── notebooks/              # EDA & experimentation only
├── src/
│   └── <{{cookiecutter.project_slug}}>/     # Production Python package
│       ├── cli/            # Training entrypoints (Hydra)
│       ├── data/           # Datasets, datamodules, transforms
│       ├── models/         # PyTorch & Lightning models
│       ├── training/       # Training loops & callbacks
│       ├── inference/      # Pure inference logic (no web code)
│       ├── evaluation/     # Offline evaluation
│       ├── schemas/        # Pydantic models
│       ├── integrations/   # MLflow / DVC glue
│       ├── logging/        # Logging setup
│       └── utils/          # Small pure utilities
├── tests/                  # Unit & integration tests
├── tools/                  # Repo hygiene & CI tools
├── .github/                # Issue / PR templates
├── dvc.yaml                # Optional DVC pipeline stub
├── pyproject.toml          # Dependency & version source of truth
├── CHANGELOG.md
├── README.md               # Project-specific documentation
└── TEMPLATE_GUIDE.md       # You are here
```

---

## Configuration Model (Hydra)

- All configuration lives under `config/`
- No `params.yaml`
- No duplicated config inside `src/`
- Tool-specific configs live in subgroups:
  - `config/data/`
  - `config/model/`
  - `config/trainer/`
  - `config/logging/`
  - `config/mlflow/`
  - `config/experiment/`

Training is always launched via:

```bash
python -m <{{cookiecutter.project_slug}}>.cli.train
```

Overrides happen via Hydra CLI or experiment configs.

---

## Notebook → Source Code Workflow

1. Explore ideas in `notebooks/`
2. Validate assumptions
3. Promote stable logic into `src/<{{cookiecutter.project_slug}}>/`
4. Add tests
5. Never let notebooks own production logic

Notebooks are **disposable**, source code is **authoritative**.

---

## Data & DVC

- `data/README.md` documents dataset semantics
- DVC is **optional but supported**
- `dvc.yaml` uses deterministic Hydra run dirs
- No dynamic DVC metadata in configs

Data is never committed directly.

---

## Model Tracking & Lifecycle (MLflow)

- One experiment per project
- One registered model per project
- Lifecycle handled via **aliases**:
  - `dev`
  - `staging`
  - `prod`
  - `archived`

CI is responsible for:

- exporting artifacts
- validating deployability
- updating aliases

Humans do not manually promote models.

---

## Deployment Paths

- **FastAPI** → flexible inference & business logic
- **Dashboards** → demos & QA (optional)
- **Triton** → high-performance inference
- **Kubernetes** → service-level deployment (namespace-agnostic)

All deployments pull models from **MLflow Registry**, not from git.

---

## CI/CD Model

- PRs → lint + tests
- Tags → model export + promotion
- Manual → fallback promotion

CI enforces:

- hygiene
- reproducibility
- lifecycle correctness

---

## Cookiecutter Notes

When converting this repo to a cookiecutter template:

- Replace `<{{cookiecutter.project_slug}}>` everywhere
- Preserve directory structure
- Keep all README / INSTRUCTIONS files
- Keep `TEMPLATE_GUIDE.md` unchanged
- Allow optional features (DVC, dashboards, Triton) via cookiecutter flags

---

## License

GPL-licensed template.
Derived projects must comply with the license terms.

---

## Final Notes

This template is intentionally strict.

If something feels inconvenient, it is usually protecting you from:

- irreproducible experiments
- ad-hoc deployment
- config drift
- silent production failures
