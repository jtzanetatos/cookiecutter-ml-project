# API Documentation

This directory describes the public interfaces for this project.

## HTTP API (if applicable)

### Base URL

[TODO: e.g. /api/v1]

### Endpoints

- `GET /health`  
  Description: [TODO]

- `POST /predict`  
  Request schema: [TODO: link to Pydantic model]  
  Response schema: [TODO]

---

## Python Library API

### Modules

- `{{cookiecutter.project_slug}}.inference` – [TODO: describe]
- `{{cookiecutter.project_slug}}.data` – [TODO]

---

## CLI Commands

- `python -m src.{{cookiecutter.project_slug}}.core.train`  
  Description: training entrypoint using Hydra.

- `python -m src.{{cookiecutter.project_slug}}.core.evaluate`  
  Description: evaluation workflow.

---

Add detailed API documents as separate files if needed.
