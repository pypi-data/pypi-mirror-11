"""Content Widgets.
"""
from pytsite import taxonomy as _taxonomy, auth as _auth, widget as _widget, html as _html, lang as _lang, \
    router as _router
from . import _model, _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ContentModelSelect(_widget.select.Select):
    """Content Model Select Widget.
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self._items = []
        u = _auth.get_current_user()
        for k, v in _functions.get_models().items():
            if u.has_permission('pytsite.odm_ui.browse.' + k) or u.has_permission('pytsite.odm_ui.browse_own.' + k):
                self._items.append((k, _lang.t(v[1])))


class TagCloud(_taxonomy.widget.Cloud):
    """Tags Cloud Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__('tag', **kwargs)


class EntityTagCloud(_taxonomy.widget.Cloud):
    """Tags Cloud of the Entity Widget.
    """
    def __init__(self, entity: _model.Content, **kwargs):
        """Init.
        """
        super().__init__('tag', **kwargs)
        self._entity = entity

    @property
    def terms(self) -> list:
        return self._entity.tags


class SearchInput(_widget.Base):
    def __init__(self, model: str, **kwargs):
        super().__init__(**kwargs)
        self._model = model

    def render(self) -> _html.Element:
        value = _router.request.values_dict.get('search', '')
        form = _html.Form(cls='wrapper form-inline', method='GET')
        form.append(_html.Input(type='text', cls='form-control', name='search',  required=True,
                                placeholder=_lang.t('pytsite.content@search_input_placeholder'),
                                value=value))
        form.set_attr('action', _router.ep_url('pytsite.content.ep.index', {
            'model': self._model,
        }))

        btn = _html.Button(type='submit', cls='btn btn-default')
        form.append(btn.append(_html.I(cls='fa fa-search')))
        return self._group_wrap(form, False)
