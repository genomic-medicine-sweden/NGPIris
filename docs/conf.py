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

# Don't show "None" return types, but show all others
typehints_document_rtype_none = False

typehints_defaults = "comma"
typehints_use_signature = True


# -- Options for autodoc -------------------------------------------------

# autodoc_typehints = "both"
autodoc_preserve_defaults = True
autodoc_member_order = "bysource"
autoclass_content = "init"
autodoc_mock_imports = [
    "botocore",
    "bitmath",
    "rapidfuzz",
]

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
