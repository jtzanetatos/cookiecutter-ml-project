#!/usr/bin/env python3
import re
import json
import urllib.request
import os
import subprocess
import tempfile
from pathlib import Path

# Path to the template's pyproject.toml
PYPROJECT_PATH = Path("{{cookiecutter.repo_name}}/pyproject.toml")
WORKFLOWS_DIR = Path("{{cookiecutter.repo_name}}/.github/workflows")
PRECOMMIT_CONFIG = Path(".pre-commit-config.yaml") # This is for the template repo itself, usually root

# Regex to find dependencies formatted as "package==version" or "package>=version"
# Handles single/double quotes, spaces, and PEP 440 versions (digits, dots, chars, +, -)
DEP_PATTERN = re.compile(r'["\']([a-zA-Z0-9_\-]+)\s*(==|>=)\s*([a-zA-Z0-9\.\-\+]+)["\']')

# Regex to find GitHub Actions "uses: owner/repo@version"
ACTION_PATTERN = re.compile(r'uses:\s+([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)@([a-zA-Z0-9_\-\.]+)')

def get_latest_pypi_version(package_name):
    """Query PyPI for the latest version of a package."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception as e:
        print(f"  [!] Skipped {package_name}: {e}")
        return None

def get_latest_action_version(owner, repo, token=None):
    """Query GitHub API for the latest release of an action."""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    req = urllib.request.Request(url)
    
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data["tag_name"]
    except Exception:
        # Fallback: list tags if no releases
        return _get_latest_tag_fallback(owner, repo, token)

def _get_latest_tag_fallback(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
        
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data and isinstance(data, list):
                # Return the first tag (heuristic for latest)
                return data[0]["name"]
    except Exception as e:
        print(f"  [!] Skipped action {owner}/{repo}: {e}")
    return None

def validate_with_uv(new_pyproject_content):
    """
    Validates that the new pyproject.toml content allows for a successful 'uv lock'.
    
    Strategy:
    1. Temporarily write the new content to the template.
    2. Render the template using cookiecutter to a temp dir.
    3. Run 'uv lock' in the generated project.
    4. Revert the template file change.
    """
    print("    [?] Validating dependency resolution with uv...")
    original_content = PYPROJECT_PATH.read_text()
    
    # 1. Apply candidate change
    PYPROJECT_PATH.write_text(new_pyproject_content)
    
    valid = False
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                # 2. Render template (use minimal inputs)
                subprocess.run(
                    [
                        "uv", "run", "cookiecutter", ".", 
                        "--no-input", 
                        f"--output-dir={tmp_dir}", 
                        "project_slug=validation_proj",
                        "ml_framework=pytorch" 
                    ],
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                project_path = Path(tmp_dir) / "validation_proj"
                
                # 3. Run uv lock
                result = subprocess.run(
                    ["uv", "lock"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("    [OK] Validation successful.")
                    valid = True
                else:
                    print(f"    [!] Validation FAILED:\n{result.stderr}")
                    
            except subprocess.CalledProcessError as e:
                print(f"    [!] Validation crashed (subprocess): {e}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
            except Exception as e:
                print(f"    [!] Validation crashed: {e}")
                
    finally:
        # 4. Revert immediately (we only write permanently if/when the caller decides)
        # The caller (update_python_dependencies) calls write_text AGAIN if valid.
        # So it is safe to always revert here to restore clean state.
        PYPROJECT_PATH.write_text(original_content)
    
    return valid

def update_python_dependencies():
    if not PYPROJECT_PATH.exists():
        print(f"Error: {PYPROJECT_PATH} not found.")
        return False

    print(f"Checking Python dependencies in {PYPROJECT_PATH}...")
    content = PYPROJECT_PATH.read_text()
    new_content = content
    # Look for exact string matches from regex to safely replace
    updates_candidate_content = content
    has_candidates = False

    for match in DEP_PATTERN.finditer(content):
        package = match.group(1)
        operator = match.group(2)
        current_version = match.group(3)
        full_match = match.group(0) 
        
        if operator == "==":
            latest = get_latest_pypi_version(package)
            if latest and latest != current_version:
                 print(f"  checking {package}: {current_version} -> {latest}")
                 # Apply update to candidate content
                 new_block = full_match.replace(current_version, latest)
                 updates_candidate_content = updates_candidate_content.replace(full_match, new_block)
                 has_candidates = True

    if has_candidates:
        # Validate the BATCH of updates (all at once)
        if validate_with_uv(updates_candidate_content):
            print(f"Writing validated changes to {PYPROJECT_PATH}...")
            PYPROJECT_PATH.write_text(updates_candidate_content)
            return True
        else:
            print("  [!] Skipping updates due to validation failure.")
            return False
    
    print("  No Python updates found.")
    return False

def update_workflow_files(directory):
    """Scans workflow files in a given directory for action updates."""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Warning: {dir_path} not found.")
        return False

    print(f"Checking GitHub Actions in {dir_path}/*.yml...")
    updates_made = False
    
    token = os.environ.get("GITHUB_TOKEN")

    for workflow_file in dir_path.glob("*.yml"):
        print(f"  Scanning {workflow_file.name}...")
        content = workflow_file.read_text()
        new_content = content
        
        file_changed = False
        for match in ACTION_PATTERN.finditer(content):
            owner = match.group(1)
            repo = match.group(2)
            current_version = match.group(3)
            full_match = match.group(0)
            
            # Skip if not a version tag
            if not (current_version.startswith("v") or "." in current_version):
                continue

            latest_tag = get_latest_action_version(owner, repo, token)
            if latest_tag and latest_tag != current_version:
                 # Standardize 'v' prefix
                 if current_version.startswith("v") and not latest_tag.startswith("v"):
                     latest_tag = f"v{latest_tag}"
                 
                 if latest_tag != current_version:
                    print(f"    -> Updating {owner}/{repo}: {current_version} -> {latest_tag}")
                    new_block = full_match.replace(current_version, latest_tag)
                    new_content = new_content.replace(full_match, new_block)
                    file_changed = True
        
        if file_changed:
            print(f"Writing changes to {workflow_file}...")
            workflow_file.write_text(new_content)
            updates_made = True

    return updates_made

def update_pre_commit():
    """Run pre-commit autoupdate for the repository's own configuration."""
    root_config = Path(".pre-commit-config.yaml")
    
    if root_config.exists():
        print(f"Updating root pre-commit hooks in {root_config}...")
        try:
            # Check if pre-commit is installed
            subprocess.run(["pre-commit", "--version"], check=True, capture_output=True)
            subprocess.run(["pre-commit", "autoupdate"], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  [!] Failed to run pre-commit autoupdate (is it installed?)")
    
    return False

if __name__ == "__main__":
    print("Starting dependency updates...")
    py_updated = update_python_dependencies()
    
    # Update both template workflows and the repo's own workflows
    gh_updated_template = update_workflow_files(WORKFLOWS_DIR)
    gh_updated_root = update_workflow_files(".github/workflows")
    
    pc_updated = update_pre_commit()
    
    if py_updated or gh_updated_template or gh_updated_root or pc_updated:
        print("Updates completed successfully.")
    else:
        print("No updates found.")
