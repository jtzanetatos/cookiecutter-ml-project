# Streamlit Dashboard

This is an optional Streamlit app used for demos and lightweight exploration.

Guidelines:

- UI only; do not implement core logic here.
- Import inference helpers from `src/<{{cookiecutter.project_slug}}>/inference/`.
- Validate user inputs using `src/<{{cookiecutter.project_slug}}>/schemas/`.
- Resolve models from MLflow via aliases (`prod`, `staging`, etc.).

Run:

```bash
streamlit run deployment/dashboards/streamlit/app.py
```
