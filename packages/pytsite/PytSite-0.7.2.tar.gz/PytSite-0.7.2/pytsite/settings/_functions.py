"""Settings Plugin Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import admin as _admin, auth as _auth
from pytsite.core import router as _router, form as _form, odm as _odm, widget as _widget, lang as _lang

__settings = {}


def define(uid: str, form_cls: type, menu_title: str, menu_icon: str, menu_weight: int=0,
           perm_name: str='*', perm_description: str=None):
    """Define setting.
    """
    if uid in __settings:
        raise KeyError("Setting '{}' already defined.".format(uid))

    if not isinstance(form_cls, type) or not issubclass(form_cls, _form.Base):
        raise TypeError("Subclass of base form expected.")

    __settings[uid] = {
        'title': menu_title,
        'form_cls': form_cls,
        'weight': menu_weight,
        'perm_name': perm_name,
        'perm_description': perm_description,
    }

    if perm_name != '*' and perm_description:
        _auth.define_permission(perm_name, perm_description, 'admin')

    url = _router.endpoint_url('pytsite.settings.eps.form', {'uid': uid})
    _admin.sidebar.add_menu('settings', uid, menu_title, url, menu_icon, permissions=perm_name)


def get_definition(uid: str) -> dict:
    """Get setting definition.
    """
    if uid not in __settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    return __settings[uid]


def get_form(uid) -> _form.Base:
    """Get form for setting.
    """
    frm_class = get_definition(uid)['form_cls']
    frm = frm_class('settings-' + uid)
    """:type : _form.Base """

    frm.action = _router.endpoint_url('pytsite.settings.eps.form_submit', {'uid': uid})
    frm.validation_ep = 'pytsite.settings.eps.form_validate'

    frm.add_widget(_widget.input.Hidden(
        uid='__setting_uid',
        value=uid
    ), 'form')

    actions = _widget.static.Wrapper(uid='actions')
    actions.add_child(_widget.button.Submit(
        weight=10,
        value=_lang.t('settings@save'),
        icon='fa fa-save',
        color='primary'
    ))
    actions.add_child(_widget.button.Link(
        weight=10,
        value=_lang.t('settings@cancel'),
        icon='fa fa-ban',
        href=_router.endpoint_url('pytsite.admin.eps.dashboard')
    ))
    frm.add_widget(actions, 'footer')

    return frm


def get_setting(uid) -> dict:
    """Get setting value.
    """
    if uid not in __settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    entity = _odm.find('setting').where('uid', '=', uid).first()
    if not entity:
        return {}

    return entity.f_get('value')


def set_setting(uid, value: dict):
    """Set setting value.
    """
    entity = _odm.find('setting').where('uid', '=', uid).first()
    if not entity:
        entity = _odm.dispense('setting').f_set('uid', uid)

    entity.f_set('value', value).save()
