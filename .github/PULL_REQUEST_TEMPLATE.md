# Summary

Describe the change to the cookiecutter template.

# Motivation / Context

Why is this change needed? Link related issues if applicable.

# What changed

- [ ] Template content under `{{cookiecutter.repo_name}}/`
- [ ] Cookiecutter mechanics (`cookiecutter.json`, render rules, scripts)
- [ ] Documentation (README/CONTRIBUTING/CHANGELOG)
- [ ] CI (smoke test or other)

# Testing

- [ ] CI smoke workflow passed
- [ ] Ran local smoke generation (optional)

Local command (optional):

```bash
./tools/sync_and_smoke_test.sh /abs/path/to/ml-project-template
```

# Checklist

- [ ] No unrendered `{{cookiecutter...}}` remains in generated output
- [ ] Updated `_copy_without_render` if new Helm / workflow files were added
- [ ] Updated README if user-facing behavior changed
