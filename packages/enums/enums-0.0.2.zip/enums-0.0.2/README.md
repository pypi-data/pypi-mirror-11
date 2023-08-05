# enums
*Enumeration types for Python*

Ever find yourself juggling constants, wondering whether the value `0x002A`
originated as the index to the `Comments` field or as the protocol version
number from that binary file? The `enums` module is a simple implementation
of named enumeration types for `Python`. It is useful for avoiding lots of
globally defined constants that don't remember who they are or where they
came from. With `enums`, you can define a collection of values as having a
common type and behavior, and the values will remember their original names
and types.

To use `enums`, define an enumeration class that inherits from `Enum`, and then
assign values within the class's scope as `Const` instances. Then call the
`close()` class method for your enumeration class, and all the `Const` values
will be converted in-place to unique instances of your enumeration type. If
you want to control the initialization of your enumeration class, define an
`__init__` method just as you would for any normal class, and pass the
arguments to `Const()`. The arguments will be passed on to your `__init__`
class unchanged.

The enums module also provides a `Registry` class, which allows multiple
owners to safely reserve name/value pairs within a shared space.


Example usage:

```
>>> from enums import Enum, Const

>>> class Enumeration(Enum):
>>>     VALUE1 = Const()
>>>     VALUE2 = Const()
>>> Enumeration.close()

>>> class Enumeration2(Enum):
>>>     def __init__(self, int_val):
>>>         assert isinstance(int_val, int)
>>>         self._int_val = int_val
>>>         super(Enumeration2, self).__init__(int_val)
>>>     def __int__(self):
>>>         return self._int_val
>>>     VALUE1 = Const(10)
>>>     VALUE2 = Const(100)
>>>     VALUE3 = Const(1000)
>>> Enumeration2.close()

>>> Enumeration.VALUE1
Enumeration.VALUE1

>>> Enumeration.VALUE2
Enumeration.VALUE2

>>> Enumeration.VALUE1 == Enumeration.VALUE2
False

>>> Enumeration.VALUE1 == Enumeration2.VALUE1
False

>>> isinstance(Enumeration.VALUE1, Enumeration)
True

>>> int(Enumeration2.VALUE3)
1000
```
