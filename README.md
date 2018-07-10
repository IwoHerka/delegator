<img align="left" width="275" src="https://raw.githubusercontent.com/IwoHerka/delegator/master/delegator.png">

## dele➣gator

[![Build Status](https://travis-ci.com/IwoHerka/delegator.svg?branch=master)](https://travis-ci.com/IwoHerka/delegator)
[![Coverage Status](https://coveralls.io/repos/github/IwoHerka/delegator/badge.svg?branch=master)](https://coveralls.io/github/IwoHerka/delegator?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/37e7d64cc51641b0b5b73ab8df41eb23)](https://www.codacy.com/app/IwoHerka/delegator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=IwoHerka/delegator&amp;utm_campaign=Badge_Grade)

**delegator** is a micro-package for defining delegated methods and attributes.

In short, it serves to get rid of boilerplate such as the one on the left hand side with the compact notation on the right hand side. It's very similar to delegation syntax in Ruby.

![alt text](https://raw.githubusercontent.com/IwoHerka/delegator/master/example.png "Example")

`delegate` attribue on the delegating class can be a **sequence** or a single **string** with arguments separated by whitespace (similar to `namedtuple`). Delegatee attribute must be the first argument. If you don't like the style - no worries - there are three interchangeable notations:

#### Metaclass

```python
class Foo(metaclass=Delegator):
    delegate = 'bar spam ham eggs'
    # or delegate = 'bar', 'spam', 'ham', 'eggs'
```

#### Explicit class decorator

```python
@delegate('bar spam ham eggs')
# or @delegate('bar', 'spam', 'ham', 'eggs')
class Foo(metaclass=Delegator):
```

#### Implicit class decorator

```python
@delegator
class Foo:
    delegate = 'bar spam ham eggs'
    # or, again: delegate = 'bar', 'spam', 'ham', 'eggs'
```

Internally, delegation works via simple attribute accessors with `__get__`, `__set__` and `__delete__` methods. Setting and deleting works as expected:

```python
foo.spam = 'chopped pork and ham'
foo.spam
# = 'chopped pork and ham'

del foo.spam
foo.spam
# = 'spam' (falls back to `spam` attribute on `Bar`)
```

For more details, see `decorate ` and `Delegated` in the source code. For more examples, check out `tests.py`.
