# Makefile (cookiecutter repo)
#
# Usage examples:
#   make sync SRC=/abs/path/to/ml-project-template
#   make smoke SRC=/abs/path/to/ml-project-template
#   make smoke SRC=/abs/path/to/ml-project-template OUT=../_generated
#
# Notes:
# - SRC must point to the upstream (plain) template repo that is the source of truth.
# - OUT defaults to the parent directory of this cookiecutter repo.

SHELL := /usr/bin/env bash

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
SRC ?=
OUT ?= $(abspath $(ROOT)/..)

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make sync  SRC=/abs/path/to/ml-project-template"
	@echo "  make smoke SRC=/abs/path/to/ml-project-template [OUT=/path/to/output]"
	@echo ""
	@echo "Vars:"
	@echo "  SRC  Upstream template repo path (required)"
	@echo "  OUT  Output directory for smoke generation (default: parent of cookiecutter repo)"

.PHONY: sync
sync:
	@if [[ -z "$(SRC)" ]]; then echo "ERROR: SRC is required"; exit 2; fi
	@./tools/sync_template_into_cookiecutter.sh "$(SRC)"

.PHONY: smoke
smoke:
	@if [[ -z "$(SRC)" ]]; then echo "ERROR: SRC is required"; exit 2; fi
	@./tools/sync_and_smoke_test.sh "$(SRC)" "$(OUT)"
