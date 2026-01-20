"""
MkDocs macros to inject dynamic variables into documentation.
Reads version from pyproject.toml automatically.
"""

import tomli
from pathlib import Path


def define_env(env):
    """
    Define custom variables and macros for MkDocs.
    This function is called by mkdocs-macros-plugin.
    """
    # Read version from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)

    # Make version available as {{ version }} in all markdown files
    env.variables["version"] = pyproject_data["tool"]["poetry"]["version"]

    # You can add more dynamic variables here as needed
    env.variables["project_name"] = pyproject_data["tool"]["poetry"]["name"]
    env.variables["description"] = pyproject_data["tool"]["poetry"]["description"]
