# Adapted off of
# https://github.com/felix-hilden/tekore/blob/f08c7a9692457b1caf7e2563338edc8cf0e69836/tekore/_model/serialise.py
# Under the MIT license by Felix Hilden
# I did this since this is an extremely elegant solution for creating objects based off of
# JSON responses (which I needed for this project)
import json
import re
from dataclasses import dataclass, asdict, fields
from pprint import pprint
from typing import Union, TypeVar, List
from warnings import warn


class JSONEncoder(json.JSONEncoder):
    """JSON Encoder for response models."""

    def default(self, o):
        """Convert into serializable data types."""
        if isinstance(o, Model):
            return asdict(o)
        else:
            return super().default(o)


def member_repr(dataclass_type) -> str:
    """Construct representation of fields of type Model."""
    v_fields = sorted(fields(dataclass_type), key=lambda f: f.name)
    joined = ', '.join(f.name for f in v_fields)
    return dataclass_type.__name__ + '(' + joined + ')'


def cut_by_comma(line: str, end: str, max_len: int) -> str:
    """Cut line to the appropriate comma."""
    cut = line[:max_len - len(end)]
    mend = ','.join(cut.split(',')[:-1])
    return mend + end


def field_repr(field, value) -> str:
    """Construct field representations."""
    if isinstance(value, Model):
        text = member_repr(type(value))
    elif isinstance(value, list):
        outer_type = field.type
        if outer_type.__origin__ is Union:
            outer_type = outer_type.__args__[0]

        inner_type = outer_type.__args__[0]

        if issubclass(inner_type, Model):
            f_str = member_repr(inner_type)
        else:
            f_str = inner_type.__name__

        text = f'[{len(value)} x {f_str}]'
    elif isinstance(value, dict):
        v_fields = sorted(value.keys())
        f_str = ', '.join([f"'{f}'" for f in v_fields])
        text = f'{{{f_str}}}'
    elif isinstance(value, str):
        text = f"'{value}'"
    else:
        text = repr(value)

    return text


def trim_line(line: str, value, max_len: int = 75) -> str:
    """Trim line based on field type."""
    if len(line) > max_len:
        if isinstance(value, Model):
            line = cut_by_comma(line, ', ...)', max_len)
        elif isinstance(value, list) and '(' in line:
            line = cut_by_comma(line, ', ...)]', max_len)
        elif isinstance(value, dict):
            line = cut_by_comma(line, ', ...}', max_len)
        elif isinstance(value, str):
            line = line[:max_len - 4] + '...\''

    return line


class Serializable:
    """Serialization and convenience methods for response models."""

    def json(self) -> str:
        """
        JSON representation of a model.
        Returns
        -------
        str
            JSON representation
        """
        return JSONEncoder().encode(self)

    def asbuiltin(self) -> Union[dict, list]:
        """
        Builtin representation of a model as dictionaries and lists.
        Returns
        -------
        Union[dict, list]
            builtin representation
        """
        return json.loads(self.json())

    def pprint(
            self,
            depth: int = None,
            compact: bool = True,
            **pprint_kwargs
    ) -> None:
        """
        Pretty print the builtin representation of a model.
        Parameters
        ----------
        depth
            number of levels printed, all levels printed by default
        compact
            combine items on the same line if they fit
        pprint_kwargs
            additional keyword arguments for ``pprint.pprint``
        """
        pprint(self.asbuiltin(), depth=depth, compact=compact, **pprint_kwargs)


# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def convert_field_name(name: str) -> list[str]:
    # The original field name is always in index 0
    return [name, name.lower(), camel_to_snake(name)]


def is_known_field(cls_fields: list[list[str]], known_kwargs: dict, unknown_kwargs: dict, name, val):
    name_options = convert_field_name(name)
    for field in cls_fields:
        for option in name_options:
            if option in field:
                known_kwargs[field[0]] = val
                return
    unknown_kwargs[name] = val


@dataclass(repr=False)
class Model(Serializable):
    """Dataclass that provides a readable ``repr`` of its fields."""

    def __repr__(self):
        name = type(self).__name__
        lines = [f'{name} with fields:']

        for field in sorted(fields(self), key=lambda f: f.name):
            value = getattr(self, field.name)
            text = field_repr(field, value)
            line = trim_line(f'  {field.name} = {text}', value)
            lines.append(line)

        return '\n'.join(lines)

    @classmethod
    def from_kwargs(cls, **kwargs):
        """Create the Model and patch unknown kwargs in."""
        # Adapted from Stack Overflow: https://stackoverflow.com/a/55101438/7089239
        cls_fields = [convert_field_name(field.name) for field in fields(cls)]

        # split into known and unknown kwargs
        known_kwargs, unknown_kwargs = {}, {}
        for name, val in kwargs.items():
            is_known_field(cls_fields, known_kwargs, unknown_kwargs, name, val)

        model = cls(**known_kwargs)

        for name, val in unknown_kwargs.items():
            setattr(model, name, val)
        return model


T = TypeVar('T')


class ModelList(List[T], Serializable):
    """List that provides a readable ``repr`` of its items."""

    def __repr__(self):
        name = type(self).__name__
        lines = [f'{name} with items: [']

        for model in self:
            # Hack: can leave field out because nested lists don't exist
            text = field_repr(None, model)
            line = trim_line(f'  {text}', model)
            lines.append(line)

        return '\n'.join(lines + [']'])


class UnknownModelAttributeWarning(RuntimeWarning):
    """The response model contains an unknown attribute."""
