from delegator import *


class Foo(metaclass=Delegator):
    pass

@delegator
class Bar(object):
    pass

class Spam(object):
    def func(self):
        return True

@delegate('spam', 'func')
class Eggs(object):
    def __init__(self):
        self.spam = Spam()


def test():
    foo = Foo()
    bar = Bar()
    eggs = Eggs()
