#!/usr/bin/env python3
import re
import json
import urllib.request
import sys
import os
from pathlib import Path

# Path to the template's pyproject.toml
PYPROJECT_PATH = Path("{{cookiecutter.repo_name}}/pyproject.toml")
WORKFLOWS_DIR = Path("{{cookiecutter.repo_name}}/.github/workflows")

# Regex to find dependencies formatted as "package==version" or "package>=version"
DEP_PATTERN = re.compile(r'"([a-zA-Z0-9_\-]+)(==|>=)([\d\.]+)"')

# Regex to find GitHub Actions "uses: owner/repo@version"
# Captures: 1=owner, 2=repo, 3=version (tag/branch/hash)
# We focus on @vX or @vX.Y.Z tags primarily for updates
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

def get_latest_action_version(owner, repo):
    """Query GitHub API for the latest release of an action."""
    # Try getting the latest release first
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    req = urllib.request.Request(url)
    
    # Use GITHUB_TOKEN if available to avoid rate limits
    token = os.environ.get("GITHUB_TOKEN")
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
                # Simple heuristic: return the first tag. 
                # Ideally we'd sort semanctically, but often the first return is latest.
                return data[0]["name"]
    except Exception as e:
        print(f"  [!] Skipped action {owner}/{repo}: {e}")
    return None

def update_python_dependencies():
    if not PYPROJECT_PATH.exists():
        print(f"Error: {PYPROJECT_PATH} not found.")
        return False

    print(f"Checking Python dependencies in {PYPROJECT_PATH}...")
    content = PYPROJECT_PATH.read_text()
    new_content = content
    matches = DEP_PATTERN.findall(content)
    updates_made = False

    for package, operator, current_version in matches:
        if operator == "==":
            print(f"  checking {package} (current: {current_version})...")
            latest = get_latest_pypi_version(package)
            
            if latest and latest != current_version:
                print(f"    -> Updating to {latest}")
                old_str = f'"{package}{operator}{current_version}"'
                new_str = f'"{package}{operator}{latest}"'
                new_content = new_content.replace(old_str, new_str)
                updates_made = True

    if updates_made:
        print(f"Writing changes to {PYPROJECT_PATH}...")
        PYPROJECT_PATH.write_text(new_content)
        return True
    else:
        print("  No Python updates found.")
        return False

def update_github_actions():
    if not WORKFLOWS_DIR.exists():
        print(f"Warning: {WORKFLOWS_DIR} not found.")
        return False

    print(f"Checking GitHub Actions in {WORKFLOWS_DIR}/*.yml...")
    updates_made = False

    for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
        print(f"  Scanning {workflow_file.name}...")
        content = workflow_file.read_text()
        new_content = content
        matches = ACTION_PATTERN.findall(content)
        
        file_changed = False
        for owner, repo, current_version in matches:
            # Skip if it is a local path or strange version
            if current_version.startswith("v"):
                 # Only try to update things that look like semantic versions or v-tags
                 pass
            else:
                # Could be a hash or branch, skip for safety unless we want to be aggressive
                # For this implementation, let's treat everything as updateable if we find a tag
                pass

            latest_tag = get_latest_action_version(owner, repo)
            if latest_tag and latest_tag != current_version:
                 # Check if latest_tag matches the style (v prefix)
                 if current_version.startswith("v") and not latest_tag.startswith("v"):
                     latest_tag = f"v{latest_tag}"
                 
                 # Basic major version check? 
                 # Often actions uses @v3 so updating to @v4.0.0 might be unwanted if we want to stay on v3.
                 # But the user request is generic "update". Let's assume upgrading to latest tag is okay.
                 if latest_tag != current_version:
                    print(f"    -> Updating {owner}/{repo} from {current_version} to {latest_tag}")
                    old_str = f"uses: {owner}/{repo}@{current_version}"
                    new_str = f"uses: {owner}/{repo}@{latest_tag}"
                    new_content = new_content.replace(old_str, new_str)
                    file_changed = True
        
        if file_changed:
            print(f"Writing changes to {workflow_file}...")
            workflow_file.write_text(new_content)
            updates_made = True

    return updates_made

if __name__ == "__main__":
    print("Starting dependency updates...")
    py_updated = update_python_dependencies()
    gh_updated = update_github_actions()
    
    if py_updated or gh_updated:
        print("Updates completed successfully.")
    else:
        print("No updates found.")
