# -*- coding: utf-8 -*-

import sys

from django.core.exceptions import ValidationError
from django.db.models import TextField, SubfieldBase

from .compat import add_metaclass
from .fields import RadioGridFormField


class RadioGridField(TextField):
    __metaclass__ = SubfieldBase

    def __init__(self, *args, **kwargs):
        self.rows = kwargs.pop('rows')
        self.values = kwargs.pop('values')
        self.require_all_fields = kwargs.pop('require_all_fields', True)
        self.verbose_name = kwargs.get('verbose_name', '')
        super(RadioGridField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(RadioGridField, self).deconstruct()
        kwargs['rows'] = self.rows
        kwargs['values'] = self.values
        kwargs['require_all_fields'] = self.require_all_fields
        return name, path, args, kwargs

    def to_python(self, value):
        if value:
            return value if isinstance(value, list) else value.split(',')
        return value

    def get_prep_value(self, value):
        return '' if value is None else ','.join(value)

    def formfield(self, **kwargs):
        defaults = {
            'rows': self.rows,
            'values': self.values,
            'require_all_fields': self.require_all_fields,
            'label': self.verbose_name,
        }
        defaults.update(kwargs)
        return RadioGridFormField(**defaults)

    def value_to_string(self, obj):
        return self.get_prep_value(self._get_val_from_obj(obj))

    def validate(self, value, model_instance):
        allowed_values = [str(key) for key, _ in self.values]
        for v in value:
            if str(v) not in allowed_values:
                raise ValidationError(self.error_messages['invalid_choice'] % {"value": value})

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(RadioGridField, self).contribute_to_class(cls, name, virtual_only)

        def get_list(obj):
            values = dict(self.values)
            display = []
            if getattr(obj, name):
                for value in getattr(obj, name):
                    item = values.get(value, None)
                    if item is None:
                        try:
                            item = values.get(int(value), value)
                        except (ValueError, TypeError):
                            item = value
                    display.append(item)
            return display

        def get_display(obj):
            return ', '.join(get_list(obj))

        setattr(cls, 'get_%s_list' % self.name, get_list)
        setattr(cls, 'get_%s_display' % self.name, get_display)


if sys.version_info[0] > 2:
    RadioGridField = add_metaclass(SubfieldBase)(RadioGridField)
