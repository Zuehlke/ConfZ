# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "ConfZ"
copyright = f"2023, Zühlke"
author = "Zühlke"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx"]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    "description": "ConfZ is a configuration management library for Python based on "
    "pydantic.",
    "github_user": "Zuehlke",
    "github_repo": "ConfZ",
    "github_button": True,
    "github_type": "star",
    "github_count": False,
    "extra_nav_links": {"Quick Start": "https://github.com/Zuehlke/ConfZ#readme"},
    "show_powered_by": False,
    "show_relbar_bottom": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["custom.css"]

# -- Options for extensions --------------------------------------------------

autodoc_class_signature = "separated"

autodoc_default_options = {"members": None, "show-inheritance": None}

autodoc_member_order = "bysource"

autodoc_type_aliases = {"ConfigSources": "confz.config_source.ConfigSources"}

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
