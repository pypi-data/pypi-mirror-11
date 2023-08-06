"""Console Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite import lang as _lang
_lang.register_package(__name__)


# Public API
from ._functions import register_command, get_command, run_command, usage, run, print_info, \
    print_error, print_success, print_warning
from ._error import Error
from . import _command as command
