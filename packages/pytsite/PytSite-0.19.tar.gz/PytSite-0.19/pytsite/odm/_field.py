"""ODM Fields.
"""
from abc import ABC as _ABC
from datetime import datetime as _datetime
from bson.objectid import ObjectId as _bson_ObjectID
from bson.dbref import DBRef as _bson_DBRef
from copy import deepcopy as _deepcopy
from pytsite import lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Base field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param nonempty: bool
        """
        self._name = name
        self._default = kwargs.get('default')
        self._nonempty = kwargs.get('nonempty', False)
        self._modified = False
        self._value = _deepcopy(self._default)
        self.set_val(self._value)

    @property
    def nonempty(self) -> bool:
        return self._nonempty

    @property
    def name(self):
        """Get name of the field.
        """
        return self._name

    @property
    def is_modified(self) -> bool:
        """Is the field has been modified?
        """
        return self._modified

    def reset_modified(self):
        """Reset the 'modified' status of the field.
        """
        self._modified = False
        return self

    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        self._value = value
        if change_modified and not self._modified:
            self._modified = True

        return self

    def get_val(self, **kwargs):
        """Get value of the field.

        :rtype:
        """
        return self._value

    def get_storable_val(self):
        """Get value suitable to store in the database.
        """
        return self._value

    def clr_val(self, reset_modified: bool=True, **kwargs):
        """Clears a value of the field.
        """
        self._value = self._default

    def add_val(self, value, change_modified: bool=True, **kwargs):
        """Add a value to the field.
        """
        self._value += value

    def sub_val(self, value, change_modified: bool=True, **kwargs):
        """Remove a value from the field.
        """
        self._value -= value

    def inc_val(self, change_modified: bool=True, **kwargs):
        """Increment a value of the field.
        """
        self._value += 1

    def dec_val(self, change_modified: bool=True, **kwargs):
        """Increment a value of the field.
        """
        self._value -= 1

    def on_delete(self):
        """Hook method to provide for the entity notification mechanism about its deletion.
        """
        pass

    def __str__(self) -> str:
        """Stringify field's value.
        """
        return str(self._value)

    def __bool__(self) -> bool:
        return bool(self._value)


class ObjectId(Abstract):
    """ObjectId field.
    """
    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        if value is not None and not isinstance(value, _bson_ObjectID):
            raise TypeError("ObjectId expected")

        return super().set_val(value, change_modified, **kwargs)


class List(Abstract):
    """List field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_types = kwargs.get('allowed_types', (int, str, float, list, dict, tuple))
        self._min_len = kwargs.get('min_len', 0)
        self._max_len = kwargs.get('max_len', 0)

        if 'default' not in kwargs:
            kwargs['default'] = []

        super().__init__(name, **kwargs)

    def get_val(self, **kwargs) -> list:
        """Get value of the field.
        """
        return super().get_val(**kwargs)

    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Set value of the field.

        :type value: list | tuple
        """
        if type(value) not in (list, tuple):
            raise TypeError('List or tuple expected.')

        # Checking validness of types of the items
        if self._allowed_types:
            for v in value:
                if type(v) not in self._allowed_types:
                    raise TypeError("Value of the field '{}' cannot contain members of type {}."
                                    .format(self.name, type(v)))

        # Checking lengths
        if self._min_len and len(value) < self._min_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))
        if self._max_len and len(value) > self._max_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))

        return super().set_val(value, change_modified, **kwargs)

    def add_val(self, value, change_modified: bool=True, **kwargs):
        """Add a value to the field.
        """
        if type(value) not in self._allowed_types:
            raise TypeError("Adding values of type {} is not allowed.".format(type(value)))

        if len(self.get_val()):
            pass

        self._value.append(value)

        if change_modified:
            self._modified = True

        return self


class UniqueList(List):
    """Unique List.
    """
    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Set value of the field.
        :type value: list | tuple
        """
        clean_val = []
        for v in value:
            if v and v not in clean_val:
                clean_val.append(v)

        return super().set_val(clean_val, change_modified, **kwargs)

    def add_val(self, value, change_modified: bool=True, **kwargs):
        """Add a value to the field.
        """
        if value not in self.get_val():
            super().add_val(value, change_modified, **kwargs)

        return self


class Dict(Abstract):
    """Dictionary field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default: dict
        :param keys: tuple
        :param nonempty_keys: tuple
        """
        self._keys = kwargs.get('keys', ())
        self._nonempty_keys = kwargs.get('nonempty_keys', ())
        if kwargs.get('default') is None:
            kwargs['default'] = {}

        super().__init__(name, **kwargs)

    def set_val(self, value: dict, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        if not isinstance(value, dict):
            raise TypeError("Value of the field '{}' must be a dictionary.".format(self._name))

        if self._keys:
            for k in self._keys:
                if k not in value:
                    raise ValueError("Value of the field '{}' must contain key '{}'.".format(self._name, k))

        if self._nonempty_keys:
            for k in self._nonempty_keys:
                if k not in value or value[k] is None:
                    raise ValueError("Value of the field '{}' must contain nonempty key '{}'.".format(self._name, k))

        return super().set_val(value, change_modified, **kwargs)


class Ref(Abstract):
    """Ref Field.
    """
    def __init__(self, name: str, model: str, **kwargs):
        """Init.
        """
        super().__init__(name, **kwargs)
        self._model = model

    @property
    def model(self) -> str:
        return self._model

    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        from ._model import Model

        if isinstance(value, list) or isinstance(value, tuple):
            value = value[0] if len(value) else None

        if isinstance(value, _bson_DBRef) or value is None:
            pass
        elif isinstance(value, Model):
            if self._model != '*' and value.model != self._model:
                raise ValueError("Instance of ODM model '{}' expected.".format(self._model))
            value = value.ref
        else:
            raise TypeError("Field '{}': entity or DBRef expected, but '{}' given.".format(self._name, repr(value)))

        return super().set_val(value, change_modified, **kwargs)

    def get_val(self, **kwargs):
        """Get value of the field.
        """
        value = self._value
        if isinstance(self._value, _bson_DBRef):
            from ._functions import get_by_ref
            referenced_entity = get_by_ref(value)
            if not referenced_entity:
                self.set_val(None)  # Updating field's value about missing entity
            return referenced_entity


class RefsList(List):
    """List of DBRefs field.
    """
    def __init__(self, name: str, model: str, **kwargs):
        """Init.
        """
        self._model = model
        super().__init__(name, allowed_types=(_bson_DBRef,), **kwargs)

    @property
    def model(self) -> str:
        return self._model

    def set_val(self, value: list, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        if not isinstance(value, list) and not isinstance(value, tuple):
            raise ValueError('List expected.')

        # Cleaning up value
        clean_value = []
        from ._model import Model
        for item in value:
            if isinstance(item, Model):
                if self._model != '*' and item.model != self._model:
                    raise ValueError("Instance of ODM model '{}' expected.".format(self._model))
                clean_value.append(item.ref)
            elif isinstance(item, _bson_DBRef):
                clean_value.append(item)
            else:
                raise TypeError("Field '{}': list of DBRefs or entities expected.".format(self.name))

        return super().set_val(clean_value, change_modified, **kwargs)

    def get_val(self, **kwargs) -> list:
        """Get value of the field.
        """
        r = []
        v = self._value
        """:type: list"""

        for ref in v:
            from ._functions import get_by_ref
            entity = get_by_ref(ref)
            if entity:
                r.append(entity)

        sort_by = kwargs.get('sort_by')
        if sort_by:
            r = sorted(r, key=lambda item: item.f_get(sort_by), reverse=kwargs.get('sort_reverse', False))

        return r

    def add_val(self, value, change_modified: bool=True, **kwargs):
        """Add a value to the field.
        """
        from ._model import Model
        if not isinstance(value, _bson_DBRef) and not isinstance(value, Model):
            raise TypeError("DBRef of entity expected.")

        if isinstance(value, _bson_DBRef):
            self._value.append(value)
        elif isinstance(value, Model):
            self._value.append(value.ref)

        if change_modified:
            self._modified = True

        return self


class RefsUniqueList(RefsList):
    """Unique list of DBRefs field.
    """
    def set_val(self, value: list, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        super().set_val(value, change_modified, **kwargs)
        clean_val = []
        ids = []
        for v in self.get_val():
            if v.id not in ids:
                clean_val.append(v)
                ids.append(v.id)

        return super().set_val(clean_val, change_modified, **kwargs)

    def add_val(self, value, change_modified: bool=True, **kwargs):
        """Add value to the field.
        """
        # Simply adding value
        super().add_val(value, change_modified, **kwargs)

        # Then filtering out duplicates
        self.set_val(self.get_val(**kwargs), change_modified, **kwargs)

        return self


class DateTime(Abstract):
    """Datetime field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        :param default: _datetime
        """
        if kwargs.get('default') is None:
            kwargs['default'] = _datetime(1970, 1, 1)

        super().__init__(name, **kwargs)

    def set_val(self, value: _datetime, change_modified: bool=True, **kwargs):
        """Set field's value.
        """
        if not isinstance(value, _datetime):
            raise TypeError("DateTime expected, while '{}' got".format(value))

        return super().set_val(value, change_modified, **kwargs)

    def get_val(self, fmt: str=None, **kwargs):
        """Get field's value.
        """
        value = super().get_val()
        """:type : _datetime"""

        if fmt:
            if fmt == 'ago':
                value = _lang.time_ago(value)
            elif fmt == 'pretty_date':
                value = _lang.pretty_date(value)
            elif fmt == 'pretty_date_time':
                value = _lang.pretty_date_time(value)
            else:
                value = value.strftime(fmt)

        return value


class String(Abstract):
    """String field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._max_length = kwargs.get('max_length', 0)

        if kwargs.get('default') is None:
            kwargs['default'] = ''

        super().__init__(name, **kwargs)

    @property
    def max_length(self) -> int:
        return self._max_length

    @max_length.setter
    def max_length(self, val: int):
        self._max_length = int(val)

    def set_val(self, value: str, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        value = '' if value is None else str(value).strip()

        if self._max_length:
            value = value[:self._max_length]

        return super().set_val(value, change_modified, **kwargs)


class Integer(Abstract):
    """Integer field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        if kwargs.get('default') is None:
            kwargs['default'] = 0

        super().__init__(name, **kwargs)

    def get_val(self, **kwargs) -> int:
        return super().get_val(**kwargs)

    def set_val(self, value: int, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        if not isinstance(value, int):
            value = int(value)

        return super().set_val(int(value), change_modified, **kwargs)

    def add_val(self, value: int, change_modified: bool=True, **kwargs):
        """Add a value to the value of the field.
        """
        if not isinstance(value, int):
            raise ValueError('Integer expected.')
        return self.set_val(self.get_val(**kwargs) + value, change_modified, **kwargs)

    def inc_val(self, change_modified: bool=True, **kwargs):
        """Increment field's value.
        """
        return self.set_val(self.get_val(**kwargs) + 1, change_modified, **kwargs)

    def dec_val(self, change_modified: bool=True, **kwargs):
        """Increment field's value.
        """
        return self.set_val(self.get_val(**kwargs) - 1, change_modified, **kwargs)


class Float(Abstract):
    """Float field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        if kwargs.get('default') is None:
            kwargs['default'] = 0.0

        super().__init__(name, **kwargs)

    def set_val(self, value: float, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        if not isinstance(value, float):
            value = float(value)

        return super().set_val(value, change_modified, **kwargs)

    def add_val(self, value: float, change_modified: bool=True, **kwargs):
        """Add a value to the value of the field.
        """
        if not isinstance(value, float):
            raise ValueError('Float expected.')
        return self.set_val(self.get_val(**kwargs) + value, change_modified, **kwargs)


class Bool(Abstract):
    """Integer field.
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        if kwargs.get('default') is None:
            kwargs['default'] = False

        super().__init__(name, **kwargs)

    def set_val(self, value: bool, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        return super().set_val(bool(value), change_modified, **kwargs)


class StringList(List):
    """List of Strings.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(str,), **kwargs)


class IntegerList(List):
    """List of Integers.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(int,), **kwargs)


class FloatList(List):
    """List of Floats.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(float,), **kwargs)


class ListList(List):
    """List of Lists.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(list, tuple), **kwargs)


class Virtual(Abstract):
    pass
