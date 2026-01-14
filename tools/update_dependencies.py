#!/usr/bin/env python3
import re
import json
import urllib.request
import sys
from pathlib import Path

# Path to the template's pyproject.toml
PYPROJECT_PATH = Path("{{cookiecutter.repo_name}}/pyproject.toml")

# Regex to find dependencies formatted as "package==version" or "package>=version"
# Captures: 1=package_name, 2=operator, 3=version
DEP_PATTERN = re.compile(r'"([a-zA-Z0-9_\-]+)(==|>=)([\d\.]+)"')

def get_latest_version(package_name):
    """Query PyPI for the latest version of a package."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception as e:
        print(f"  [!] Skipped {package_name}: {e}")
        return None

def update_dependencies():
    if not PYPROJECT_PATH.exists():
        print(f"Error: {PYPROJECT_PATH} not found.")
        sys.exit(1)

    print(f"Reading {PYPROJECT_PATH}...")
    content = PYPROJECT_PATH.read_text()
    
    new_content = content
    # Find all matches
    matches = DEP_PATTERN.findall(content)
    
    updates_made = False

    for package, operator, current_version in matches:
        # We generally only want to auto-update pinned versions (==)
        # minimal versions (>=) are less critical to update constantly unless requested.
        # But for this script, we'll try to update pinned ones mostly.
        if operator == "==":
            print(f"Checking {package} (current: {current_version})...")
            latest = get_latest_version(package)
            
            if latest and latest != current_version:
                # Basic check to avoid downgrades or unstable updates if logic needed
                # For now, simplistic string replacement
                print(f"  -> Updating to {latest}")
                # Replace specifically this entry to avoid replacing other occurrences
                # Construct the old string and new string
                old_str = f'"{package}{operator}{current_version}"'
                new_str = f'"{package}{operator}{latest}"'
                new_content = new_content.replace(old_str, new_str)
                updates_made = True
            else:
                print(f"  -> Up to date.")

    if updates_made:
        print(f"Writing changes to {PYPROJECT_PATH}...")
        PYPROJECT_PATH.write_text(new_content)
        print("Done.")
    else:
        print("No updates found.")

if __name__ == "__main__":
    update_dependencies()
