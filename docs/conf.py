# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "FileSwitch"
copyright = "2022, Marcel Johannesmann"
author = "Marcel Johannesmann"
release = "2022"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["tests", "_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "classic"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# A boolean that decides whether parentheses are appended to function and
# method role text (e.g. the content of :func:`input`) to signify that the name
# is callable. Default is True.
add_function_parentheses = False

# A boolean that decides whether module names are prepended to all object
# names (for object types where a “module” of some kind is defined),
# e.g. for py:function directives. Default is True.
add_module_names = False

# This value controls how to represent typehints. The setting takes the following values:
#   'signature' – Show typehints in the signature (default)
#   'description' – Show typehints as content of the function or method The typehints of overloaded functions or methods will still be represented in the signature.
#   'none' – Do not show typehints
#   'both' – Show typehints in the signature and as content of the function or method
# Overloaded functions or methods will not have typehints included in the description because it is impossible to accurately represent all possible overloads as a list of parameters.
autodoc_typehints = "description"
