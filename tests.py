import pytest

from delegator import *


class Baz(object):
    def spam(self):
        return 'spam'

    def ham(self):
        return 'ham'

    def eggs(self):
        return 'eggs'

class Delegating(object):
    def __init__(self):
        self.baz = Baz()

class Foo(Delegating, metaclass=Delegator):
    delegate = 'baz spam ham eggs'

@delegator
class Bar(Delegating):
    delegate = 'baz spam ham eggs'

@delegator
class Qux(Delegating):
    delegate = 'baz', 'spam', 'ham', 'eggs'

@delegate('baz', 'spam', 'ham', 'eggs')
class Grok(Delegating):
    pass

@delegate('baz spam ham eggs')
class Quux(Delegating):
    pass


def test_valid():
    objs = [Foo(), Bar(), Grok(), Qux(), Quux()]

    for obj in objs:
        assert obj.spam() == 'spam'
        assert obj.ham() == 'ham'
        assert obj.eggs() == 'eggs'

        obj.spam = 'spam'
        obj.ham = 'ham'
        obj.eggs = 'eggs'

        assert obj.spam == 'spam'
        assert obj.ham == 'ham'
        assert obj.eggs == 'eggs'

        assert obj.baz.spam == 'spam'
        assert obj.baz.ham == 'ham'
        assert obj.baz.eggs == 'eggs'

        assert Baz().spam() == 'spam'

        del obj.spam
        del obj.ham
        del obj.eggs

        assert obj.spam() == 'spam'
        assert obj.ham() == 'ham'
        assert obj.eggs() == 'eggs'


def test_invalid():
    with pytest.raises(ValueError):
        @delegate('')
        class Quux(Delegating):
            pass

    with pytest.raises(ValueError):
        @delegator
        class Corge(Delegating):
            pass

    with pytest.raises(ValueError):
        class Grault(Delegating, metaclass=Delegator):
            pass

if __name__ == '__main__':
    test_valid()
    test_invalid()
