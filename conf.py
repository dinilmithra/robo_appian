# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys

sys.path.insert(0, os.path.abspath(".."))  # Adjust this path as needed
# If your project structure is more complex, you might need to add multiple paths
# sys.path.insert(0, os.path.abspath('../../src'))

project = "robo-appian"
copyright = "2025, Dinil Mithra"
author = "Dinil Mithra"
release = "v0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []
extensions = [
    "sphinx.ext.autodoc",  # Highly recommended for Python projects
    "sphinx.ext.napoleon",  # If you use Google or NumPy style docstrings
    "sphinx.ext.viewcode",  # To link to source code
    "sphinx_rtd_theme",  # Add this line
]

html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
