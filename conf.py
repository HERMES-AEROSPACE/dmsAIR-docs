"""Sphinx configuration for dmsAIR documentation.

Mirrors the PLATO docs layout (Sphinx + sphinx_rtd_theme) so the two HERMES
Aerospace documentation sites share a consistent look & feel.
"""
from __future__ import annotations
import datetime

# -- Project information -----------------------------------------------------
project   = "dmsAIR"
copyright = f"{datetime.date.today().year}, Clement Civrais"
author    = "Clement Civrais"
release   = "0.1"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

templates_path   = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

master_doc = "index"

# -- HTML output -------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_title = "dmsAIR"
html_static_path = ["_static"]
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
    "style_nav_header_background": "#1f3b5a",  # HERMES deep-blue accent
}

# Cross-references to external docs (Python stdlib, NumPy). Harmless if unused.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy":  ("https://numpy.org/doc/stable/", None),
}

# Copy-button for code blocks (copies content only, strips prompt chars)
copybutton_prompt_text      = r">>> |\.\.\. |\$ |# "
copybutton_prompt_is_regexp = True
