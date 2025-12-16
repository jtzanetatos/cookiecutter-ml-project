#!/usr/bin/env bash
set -euo pipefail

# sync_and_smoke_test.sh
#
# Usage:
#   ./tools/sync_and_smoke_test.sh /abs/path/to/ml-project-template [output_dir]
#
# Example:
#   ./tools/sync_and_smoke_test.sh ~/code/ml-project-template ../_generated
#
# If output_dir is omitted, generates into the parent of the cookiecutter repo.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CC_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

SRC_REPO="${1:-}"
if [[ -z "${SRC_REPO}" ]]; then
  echo "ERROR: Missing source template repo path."
  echo "Usage: $0 /abs/path/to/ml-project-template [output_dir]"
  exit 2
fi

OUT_DIR="${2:-$(cd -- "${CC_ROOT}/.." && pwd)}"
mkdir -p "${OUT_DIR}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "ERROR: Missing required tool: $1"; exit 2; }; }
need cookiecutter

echo "==> 1) Syncing template into cookiecutter repo"
"${CC_ROOT}/tools/sync_template_into_cookiecutter.sh" "${SRC_REPO}"

echo "==> 2) Smoke-generating a repo"
SMOKE_REPO_NAME="test-ml"
SMOKE_PROJECT_SLUG="test_ml_project"
SMOKE_OWNER="acme"
SMOKE_TITLE="Test ML Project"

cookiecutter "${CC_ROOT}" --no-input -o "${OUT_DIR}" \
  repo_name="${SMOKE_REPO_NAME}" \
  project_slug="${SMOKE_PROJECT_SLUG}" \
  owner="${SMOKE_OWNER}" \
  project_title="${SMOKE_TITLE}"

GEN_PATH="${OUT_DIR}/${SMOKE_REPO_NAME}"
if [[ ! -d "${GEN_PATH}" ]]; then
  echo "ERROR: Smoke repo not generated at: ${GEN_PATH}"
  exit 2
fi

echo "==> 3) Basic checks"
test -f "${GEN_PATH}/pyproject.toml"
test -d "${GEN_PATH}/src/${SMOKE_PROJECT_SLUG}"
test -d "${GEN_PATH}/config"
test -d "${GEN_PATH}/deployment"
test -d "${GEN_PATH}/tests"
test -d "${GEN_PATH}/tools"

echo "==> 4) Cleanup smoke repo: ${GEN_PATH}"
rm -rf "${GEN_PATH}"

echo "==> Done."