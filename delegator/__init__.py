__version__ = '0.1.0'

"""
    delegator
    ~~~~~~~~~

    Similar to `def_delegator` in Ruby, allows to forward/delegate attributes
    and methods to some attribute on the object. Supports setting and deleting.

    User-interface consists of:

        - `delegate` class decorator
        - `delegator` class decorator
        - `Delegator` metaclass

    All methods are interchangeable. `delegate` requires passing arguments
    directly, wheares `delegator` and `Delegator` read configuration from
    `delegate` attribute on the target class. For examples see `tests.py`.
"""
from typing import Any, Union, Type, Sequence


class Delegated(object):
    """
    Your typical, run-of-the-mill attribute accessor.
    Forwards access to attribute <attr_name> from owner to <del_name>
    attribute on the owner.
    """
    def __init__(self, name: str, attr: str) -> None:
        self.attr_name = attr
        self.del_name = name

    def __get__(self, instance: str, owner: object) -> Any:
        if instance is None:
            return self
        else:
            return getattr(self.delegate(instance), self.attr_name)

    def __set__(self, instance: str, value: Any) -> None:
        setattr(self.delegate(instance), self.attr_name, value)

    def __delete__(self, instance: str) -> None:
        delattr(self.delegate(instance), self.attr_name)

    def delegate(self, instance: str) -> Any:
        return getattr(instance, self.del_name)


def decorate(cls, src: str = None, attrs: Sequence[str] = None) -> Type:
    """
    This is where the class is actually modified. Each delegated attribute is
    subsituted on the owner class with attribute accessor object (see
    `Delegated`).

    By default, `decorate` expects attribute and delegatee to be specified in
    the arguments. If arguments are not given, method checks for "delegate"
    attribute on the class and tries to read missing arguments from its value.
    "delegate" can be a sequence or a single string with arguments separated by
    whitespace (similar to `namedtuple` syntax). Delegatee must always be the
    first argument. For example:

        delegate = 'attr spam ham eggs'

    where `spam`, `ham` and `eggs` are some attributes on `cls.<attr>`.
    """
    if not (src and attrs) and hasattr(cls, 'delegate'):
        if isinstance(cls.delegate, tuple):
            src, attrs = cls.delegate[0], cls.delegate[1:]

        elif isinstance(cls.delegate, str):
            delegate = cls.delegate.split(' ')
            src, attrs = delegate[0], delegate[1:]

    if src and attrs:
        for attr in attrs:
            setattr(cls, attr, Delegated(src, attr))
    else:
        raise ValueError(
            "Invalid arguments to 'decorate': %s, %s" % (src, attrs)
        )

    return cls


def delegator(cls: Type) -> Type:
    """
    Class decorator for the "delegate" string notation.
    """
    return decorate(cls)


class Delegator(type):
    """
    Metaclass for the "delegate" string notation.
    """
    def __new__(*args: Any, **kwargs: Any):
        return decorate(type.__new__(*args, **kwargs))


class delegate(object):
    """
    Class decorator for explicit argument passing. Expects a string or some
    sequence specifying delegatee and delegated attributes.
    """
    def __init__(self, src: str, *attrs: str) -> None:
        # self.src: str
        # self.attrs: Sequence[str]

        if src and attrs:
            self.src = src
            self.attrs = attrs
        elif src and isinstance(src, str):
            delegate = src.split(' ')
            self.src, self.attrs = delegate[0], delegate[1:]
        else:
            raise ValueError(
                "Invalid arguments to 'delegate': %s, %s" % (src, attrs)
            )

    def __call__(self, cls: Type) -> Type:
        return decorate(cls, self.src, self.attrs)
