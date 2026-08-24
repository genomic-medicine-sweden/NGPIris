# Configuration file for the Sphinx documentation builder.
#
# ruff: noqa: ERA001
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "NGPIris"
# copyright = "2026, Author"
author = "Erik Brink"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_click",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "botocore": ("https://docs.aws.amazon.com/botocore/latest/", None),
    "bitmath": ("https://bitmath.readthedocs.io/en/latest/", None),
    "rapidfuzz": ("https://rapidfuzz.github.io/RapidFuzz/Usage/", None),
}


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

toc_object_entries_show_parents = "hide"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_logo = html_favicon = "_static/gms.png"

# -- Options for autodoc_typehints ---------------------------------------------

typehints_document_rtype_none = True
typehints_defaults = "comma"
typehints_use_signature = True
typehints_use_rtype = False


# -- Options for autodoc -------------------------------------------------

# autodoc_typehints = "both"
autodoc_preserve_defaults = True
autodoc_member_order = "bysource"
autoclass_content = "init"

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
