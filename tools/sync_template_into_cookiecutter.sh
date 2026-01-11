#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./tools/sync_template_into_cookiecutter.sh /abs/path/to/ml-project-template

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CC_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
TEMPLATE_DIR="${CC_ROOT}/{{cookiecutter.repo_name}}"

SRC_REPO="${1:-}"
if [[ -z "${SRC_REPO}" ]]; then
  echo "ERROR: Missing source template repo path."
  echo "Usage: $0 /abs/path/to/ml-project-template"
  exit 2
fi
if [[ ! -d "${SRC_REPO}" ]]; then
  echo "ERROR: Source repo path does not exist: ${SRC_REPO}"
  exit 2
fi
if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "ERROR: Cookiecutter template dir not found: ${TEMPLATE_DIR}"
  exit 2
fi

SRC_REPO="$(cd -- "${SRC_REPO}" && pwd)"
if [[ "${SRC_REPO}" == "${CC_ROOT}" ]] || [[ "${SRC_REPO}" == "${TEMPLATE_DIR}" ]]; then
  echo "ERROR: SRC_REPO points to the cookiecutter repo itself. Refusing."
  exit 2
fi

echo "==> Cookiecutter repo: ${CC_ROOT}"
echo "==> Source template repo: ${SRC_REPO}"
echo "==> Cookiecutter template dir: ${TEMPLATE_DIR}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "ERROR: Missing required tool: $1"; exit 2; }; }
need rsync
need perl
need find
need grep

HAVE_RG=0
if command -v rg >/dev/null 2>&1; then HAVE_RG=1; fi

echo "==> rsync template -> cookiecutter template dir"
rsync -av --delete \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.ruff_cache' \
  --exclude '.mypy_cache' \
  --exclude '.pytest_cache' \
  --exclude '.coverage' \
  --exclude 'uv.lock' \
  --exclude 'cookiecutter.json' \
  --exclude 'hooks' \
  --exclude '{{cookiecutter.repo_name}}' \
  "${SRC_REPO}/" \
  "${TEMPLATE_DIR}/"

if [[ -d "${TEMPLATE_DIR}/src/project_slug" ]]; then
  echo "==> Renaming src/project_slug -> src/{{cookiecutter.project_slug}}"
  rm -rf "${TEMPLATE_DIR}/src/{{cookiecutter.project_slug}}" || true
  mv "${TEMPLATE_DIR}/src/project_slug" "${TEMPLATE_DIR}/src/{{cookiecutter.project_slug}}"
fi

list_files_with_pattern() {
  local pattern="$1"
  if [[ "${HAVE_RG}" -eq 1 ]]; then
    (cd "${TEMPLATE_DIR}" && rg -l "${pattern}" .) || true
  else
    (cd "${TEMPLATE_DIR}" && grep -RIlE "${pattern}" .) || true
  fi
}

echo "==> Applying cookiecutter placeholders in files"

# 1. Handle <project_slug> -> placeholder (to avoid collision with bare project_slug)
files="$(list_files_with_pattern '<project_slug>')"
if [[ -n "${files}" ]]; then
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    perl -pi -e 's/<project_slug>/__COOKIE_PS_BRACKET__/g' "${TEMPLATE_DIR}/${f}"
  done <<< "${files}"
fi

# 2. Handle bare project_slug -> {{cookiecutter.project_slug}}
files="$(list_files_with_pattern '\bproject_slug\b')"
if [[ -n "${files}" ]]; then
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    perl -pi -e 's/\bproject_slug\b/{{cookiecutter.project_slug}}/g' "${TEMPLATE_DIR}/${f}"
  done <<< "${files}"
fi

# 3. Restore placeholder -> {{cookiecutter.project_slug}}
files="$(list_files_with_pattern '__COOKIE_PS_BRACKET__')"
if [[ -n "${files}" ]]; then
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    perl -pi -e 's/__COOKIE_PS_BRACKET__/{{cookiecutter.project_slug}}/g' "${TEMPLATE_DIR}/${f}"
  done <<< "${files}"
fi

files="$(list_files_with_pattern '<PROJECT_TITLE>')"
if [[ -n "${files}" ]]; then
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    perl -pi -e 's/<PROJECT_TITLE>/{{cookiecutter.project_title}}/g' "${TEMPLATE_DIR}/${f}"
  done <<< "${files}"
fi

files="$(list_files_with_pattern '<OWNER>/<REPO>')"
if [[ -n "${files}" ]]; then
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    perl -pi -e 's#<OWNER>/<REPO>#{{cookiecutter.owner}}/{{cookiecutter.repo_name}}#g' "${TEMPLATE_DIR}/${f}"
  done <<< "${files}"
fi

echo "==> Sanity checks"
set +e
(cd "${TEMPLATE_DIR}" && (
  (rg -n '\bproject_slug\b|<project_slug>|<PROJECT_TITLE>|<OWNER>/<REPO>' . 2>/dev/null) \
  || (grep -RInE '\bproject_slug\b|<project_slug>|<PROJECT_TITLE>|<OWNER>/<REPO>' .)
)) || true
set -e

echo "==> Done."