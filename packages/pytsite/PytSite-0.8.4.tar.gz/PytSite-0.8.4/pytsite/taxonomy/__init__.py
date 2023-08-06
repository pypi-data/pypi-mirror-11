"""Taxonomy Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import assetman
    from pytsite import tpl
    from pytsite import lang
    from pytsite import router
    from pytsite import admin

    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.add('pytsite.taxonomy@css/common.css')

    tpl.register_global('taxonomy', sys.modules[__package__])
    router.add_rule('/pytsite/taxonomy/search/<string:model>/<string:query>', 'pytsite.taxonomy.eps.search_terms')
    admin.sidebar.add_section('taxonomy', __name__ + '@taxonomy', 500, ('*',))

__init()


# Public API
from . import _functions, _model as model, _widget as widget
from ._functions import register_model, is_model_registered, find, dispense
