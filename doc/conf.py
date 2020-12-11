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

project = 'Limited Interaction'
copyright = '2020, Félix Chénier'
author = 'Félix Chénier'

# The full version, including alpha/beta/rc tags
with open('../limitedinteraction/VERSION', 'r') as fid:
    release = fid.read()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
#	'recommonmark',   # See workaround down there.
	'sphinx.ext.autodoc',  # Document objects using docstrings in API
	'sphinx.ext.autosummary',  # Generate summary table pages (for autodoc)
	'sphinx.ext.napoleon',  # Parse numpy-style docstrings (for autodoc)
	'sphinx_autodoc_typehints',  # Type hints in doc instead of signature (for autodoc)
    'matplotlib.sphinxext.plot_directive',
	'autodocsumm',  # Add a summary table at the top of each API page
    'nbsphinx',
    'm2r2'  # mdinclude in index.rst
]

autodoc_default_options = {
    'autosummary': True,
    'autodoc_typehints': 'description',
    'autosummary-imported-members': False,
}

nbsphinx_execute = 'never'


# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Matplotlib settings
plot_html_show_source_link = False
plot_html_show_formats = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.ipynb_checkpoints']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinx_rtd_theme'
html_theme = 'sphinx_material'

# Material theme options (see theme.conf for more information)
html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'Limited Interaction',

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://felixchenier.uqam.ca/limitedinteraction',

    # Set the color and the accent color
    'color_primary': 'black',
    'color_accent': 'blue',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/felixchenier/limitedinteraction/',
    'repo_name': 'limitedinteraction',
    'repo_type': 'github',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 1,
    # If False, expand all TOC entries
    'globaltoc_collapse': True,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': True,

    # Hide master navigation bar
    'master_doc': False,

}

html_sidebars = {
    "**": ["globaltoc.html", "localtoc.html", "searchbox.html"]
}

html_show_sourcelink = False
html_copy_source = False
html_logo = 'logo.png'
html_css_files = ['css/custom.css']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Workaround https://github.com/readthedocs/recommonmark/issues/177
from recommonmark.parser import CommonMarkParser
class CustomCommonMarkParser(CommonMarkParser):
    def visit_document(self, node):
        pass

# def setup(app):
#    app.add_source_suffix('.md', 'markdown')
#    app.add_source_parser(CustomCommonMarkParser)
