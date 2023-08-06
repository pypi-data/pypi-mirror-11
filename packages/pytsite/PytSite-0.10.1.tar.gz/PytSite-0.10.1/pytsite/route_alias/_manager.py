"""Route Paths Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from pytsite import util as _util, odm as _odm, lang as _lang
from . import _model


def create(alias: str, target: str, language: str=None) -> _model.RouteAlias:
    """Create a route alias instance.
    """
    if not language:
        language = _lang.get_current_lang()

    entity = _odm.dispense('route_alias')
    entity.f_set('language', language).f_set('alias', alias).f_set('target', target)

    return entity


def sanitize_alias_string(string: str, language: str=None) -> str:
    """Sanitize a path string.
    """
    string = _util.transform_str_1(string)

    if not language:
        language = _lang.get_current_lang()

    if not string:
        raise Exception('Alias cannot be empty.')

    if not string.startswith('/'):
        string = '/' + string

    itr = 0
    while True:
        if not _odm.find('route_alias').where('alias', '=', string).where('language', '=', language).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub('-\d+$', '-' + str(itr), string)


def find() -> _odm.Finder:
    """Get route alias finder.
    """
    return _odm.find('route_alias').where('language', '=', _lang.get_current_lang())


def find_one_by_target(target: str, language: str=None) -> _model.RouteAlias:
    """Find route alias by target.
    """
    if not language:
        language = _lang.get_current_lang()

    return _odm.find('route_alias').where('target', '=', target).where('language', '=', language).first()
