"""
    delegator
    ~~~~~~~~~

    Similar to `def_delegator` in Ruby, allows to forward/delegate attributes
    and methods to some attribute on the object. Supports setting and deleting.
"""


class Delegated(object):
    """
    Your typical, run-of-the-mill attribute accessor.
    Forwards access to attribute <attr_name> to <del_name> on the owner.
    """
    def __init__(self, name, attr):
        self.attr_name = attr
        self.del_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(self.delegate(instance), self.attr_name)

    def __set__(self, instance, value):
        setattr(self.delegate(instance), self.attr_name, value)

    def __delete__(self, instance):
        delattr(self.delegate(instance), self.attr_name)

    def delegate(self, instance):
        return getattr(instance, self.del_name)


def decorate(cls, src = None, attrs = None):
    """
    This is where the class is actually modified.
    """
    if src and attrs:
        for attr in attrs:
            setattr(cls, attr, Delegated(src, attr))
    return cls


def delegator(cls):
    return decorate(cls)


class delegate(object):
    def __init__(self, src, *attrs):
        # TODO: Validate
        self.src = src
        self.attrs = attrs

    def __call__(self, cls):
        return decorate(cls, self.src, self.attrs)


class Delegator(type):
    def __new__(*args, **kwargs):
        return decorate(type.__new__(*args, **kwargs))
