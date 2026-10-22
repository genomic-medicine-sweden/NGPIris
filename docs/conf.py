# Configuration file for the Sphinx documentation builder.
#
# ruff: noqa: ERA001
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from pathlib import Path
from tomllib import load

with Path("../pyproject.toml").open("rb") as f:
    pyproject = load(f)
    project_name: str = pyproject["project"]["name"]
    authors: list[str] = [
        author["name"] for author in pyproject["project"]["authors"]
    ]
    project_version: str = pyproject["project"]["version"]

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = project_name
author = ", ".join(authors)
version = project_version

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
    "botocore": (
        "https://docs.aws.amazon.com/botocore/latest/reference/",
        None,
    ),
    "boto3": (
        "https://docs.aws.amazon.com/boto3/latest/",
        None,
    ),
    "bitmath": ("https://bitmath.readthedocs.io/en/latest/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

toc_object_entries_show_parents = "hide"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"
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
