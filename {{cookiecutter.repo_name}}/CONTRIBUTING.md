# Contributing Guide

Welcome! This repository serves as a standard template for production-grade Machine Learning projects.

This guide outlines the engineering standards, workflow patterns, and setup instructions required to work on this project effectively. It is designed to bridge the gap between "notebook experimentation" and "MLOps engineering."

---

## 1. Mental Model & Philosophy

We follow a **strict separation** between *Exploration* and *Engineering*.

* **Notebooks (`notebooks/`)**: For visualization, EDA, and prototyping `forward()` passes. **Do not** write training loops or complex business logic here.
* **Source Code (`src/`)**: All reusable logic (models, datasets, training loops) must be refactored here. The code in `src` is stateless, functional, and covered by tests.
* **Configuration (`conf/`)**: We do not hardcode hyperparameters. All run configurations are managed via **Hydra**.
* **Data (`dvc/`)**: Large files are never committed to Git. We use **DVC** to link code versions to data versions.

---

## 2. Environment Setup

This project uses the `src` layout, meaning the package must be installed to be imported.

### Prerequisites

* Python 3.10+
* [DVC](https://dvc.org/) (Data Version Control) installed globally or in your venv.

### Installation

1. **Clone and Install**:

    ```bash
    git clone https://github.com/{{cookiecutter.github_owner}}/{{cookiecutter.repo_name}}.git
    cd {{cookiecutter.repo_name}}
    uv sync
    ```

3. **Pull Data (If using DVC)**:

    ```bash
    dvc pull
    ```

    *Note: You need credentials for the DVC remote storage (e.g., S3/GDrive) if not working locally. If DVC is not configured, skip this.*

3. **Setup Pre-commit Hooks**:

    ```bash
    pre-commit install
    ```

    *This ensures `ruff` and `mypy` run automatically before every commit.*

---

## 3. Development Workflow

### A. The "Refactor" Loop

1. **Prototype**: Meaningful work starts in a Jupyter Notebook.
2. **Refactor**: Once a function works, move it to `src/models/` or `src/data/`.
3. **Test**: Add a unit test in `tests/` to verify the new function.
4. **Run**: Execute the pipeline via the CLI, not the notebook.

### B. Running Experiments (Hydra)

Do not change code to change hyperparameters. Use the CLI.

* **Standard Training**:

    ```bash
    python src/train.py experiment=baseline
    ```

* **Override Parameters**:

    ```bash
    python src/train.py model.lr=0.001 data.batch_size=64
    ```

* **Hyperparameter Sweep (Optuna)**:

    ```bash
    python src/train.py -m hydra/sweeper=optuna
    ```

### C. Tracking (MLFlow)

MLFlow runs locally by default. To view results:

```bash
mlflow ui
```

---

## 4. Coding Standards

We enforce strict quality gates. If these checks fail, CI will reject the PR.

**Style & Linting**

* **Linter**: We use ruff (replaces Flake8/Isort).

* **Formatter**: We use ruff format (replaces Black).

* **Type Checking**: We use mypy. All function signatures in src/ must have type hints.

Command to run checks locally:

```bash
ruff check .
ruff format .
mypy src
```

**Testing**

* **Unit Tests**: Logic in src must be tested.

* **Data Tests**: We use pytest to verify data shapes and integrity before training.

```bash
pytest tests/
```

---

---

## 5. Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) to automate versioning and changelogs.

**Format**: `type(scope): subject`

**Common types**:
* `feat`: A new feature
* `fix`: A bug fix
* `docs`: Documentation only changes
* `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
* `refactor`: A code change that neither fixes a bug nor adds a feature
* `perf`: A code change that improves performance
* `test`: Adding missing tests or correcting existing tests
* `build`: Changes that affect the build system or external dependencies
* `ci`: Changes to our CI configuration files and scripts
* `chore`: Other changes that don't modify src or test files
* `revert`: Reverts a previous commit

**Examples**:
* `feat(ci): add release workflow`
* `fix(template): correct path in dockerfile`
* `docs: update contributing guide`

> **Note**: This is enforced locally via `pre-commit` hooks. If you attempt to commit a message that doesn't follow this standard, the commit will be rejected.

---

## 6. Dependency Management

* **Adding a Package**: Add it to pyproject.toml under dependencies.

* **Locking**: If using a lock file, update it after changing pyproject.toml.

---

## 7. Definition of Done

A feature or experiment is considered "Done" when:

1. Logic is moved to `src`.

2. Tests pass (`pytest`).

3. Linter passes (`ruff`).

4. Types are valid (`mypy`).

5. (If applicable) The trained model and metrics are logged to MLFlow.
