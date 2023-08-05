import json
from nativeconfig.exceptions import DeserializationError, ValidationError
from nativeconfig.options.base_option import BaseOption


class StringOption(BaseOption):
    """
    StringOption represents Python string in config.
    """
    def __init__(self, name, *, allow_empty=True, **kwargs):
        """
        Accepts all the arguments of BaseConfig except choices.

        @param allow_empty: Allow values of empty string.
        @type allow_empty: bool
        """
        self._allow_empty = allow_empty
        super().__init__(name, **kwargs)

    def deserialize_json(self, json_value):
        try:
            value = json.loads(json_value)
        except ValueError:
            raise DeserializationError("Invalid json for \"{}\": \"{}\"!".format(self._name, json_value), json_value, self._name)
        else:
            if value is not None:
                if not isinstance(value, str):
                    raise DeserializationError("JSON (\"{}\") is not a string!".format(json_value), json_value, self._name)
                else:
                    return str(value)
            else:
                return None

    def validate(self, python_value):
        super().validate(python_value)

        if not isinstance(python_value, str):
            raise ValidationError("Invalid string \"{}\" for \"{}\"!".format(python_value, self._name), python_value, self._name)

        if not self._allow_empty and len(python_value) == 0:
            raise ValidationError("Empty values are disallowed for \"{}\"!".format(self._name), python_value, self._name)
