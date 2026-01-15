import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

project_slug = "{{ cookiecutter.project_slug }}"

if not re.match(MODULE_REGEX, project_slug):
    print(f"ERROR: The project slug ({project_slug}) is not a valid Python module name.")
    print("Please do not use dashes (-) or start with numbers.")
    # Exit 1 to fail the generation
    sys.exit(1)
