Type corrector
==============


Intro
-----

Typesys is a module that is meant to make it more easy to manange types.
It contains three decorators; type_hints, type_corrector, and return_type.

The type_hints decorator lets the user specify what what the arguements of
a functions should be. If arguments of another type than specified in the
decorator if passed in, a TypeError will be raised.

The type_corrector decorator lets the user specify what types the 
arguments to a function should have. It's not 100% safe to use as it
might result in a ValueError or TypeError if the user is not careful enough.
The motivation behing this module was to find a way that makes it easier
for the programmer to see what types the arguments should be, and at 
the same time allow some margin of error.

The return_type decorator lets the user specify what type the decoratred
function should return. A TypeError will be raised if the function tries to 
return a value of another type. 

I'm not sure whether this is a good idea or not, or if it's a good approach.
It was mostly developed for fun while playing around with decorators.


Installation
------------

pip install typesys


Usage
-----

First import the decorators from the typecorrector module:

.. code:: python

    from typecorrector import type_hints, type_corrector, return_type

Then you can decorate your functions with these decorators

type_hints
''''''''''

Decorate your functions with the types you want the arguments to be as shown in
the examples below

.. code:: python
    
    # a and b must be integers
    @type_hints(int, int)
    def hint_add(a, b):
        """Adds two numbers"""
        return a+b


    @type_hints(int, int)
    def def_add(a, b=0):
        return a+b

    # accepts bot integers and floats as arguments
    @type_hints(int, float)
    def hint_mult(*numbers):
        result = 1
        for num in numbers:
            result *= num
        return result


    @type_hints(int, float)
    def hint_kw_mult(**kwargs):
        first = kwargs.get('first')
        second = kwargs.get('second')
        third = kwargs.get('third')    
        return first * second * third


  
type_corrector
''''''''''''''

Decorate your function with the types you want the arguments to be, but not
necessary are passed in as, as shown in the examples below.

.. code:: python

    @type_corrector(int, int)
    def add(x,y):
        return x+y

    
    @type_corrector(float, float)
    def div(x,y):
        return x/y
       

A call to add(1,'2') will cast '2' to an int, since that is what we
specified as the type of the second paramater in the decorator.
We can also call div as div('10', '3'), and div will return 3.3333333333333335
as expected.

This decorator also works with \*args and \*\*kwargs

.. code:: python

    @type_corrector(int)
    def mult(*numbers):
        result = 1
        for num in numbers:
            result *= num
        return result


    @type_corrector(int)
    def kw_mult(**kwargs):
        first = kwargs.get('first')
        second = kwargs.get('second')
        third = kwargs.get('third')
        return first * second * third


This allows us to call the functions like this:

- mult('2', '3', '4') 
- kw_mult(first='2', second='3', third='4')

When looking at the function definitions of add, mult and kw_mult we can easily
see that the arguments are supposed to be integers.
By decorating the functions like this it should be a clear
hint what types we want the parameters to be passed in as, even though it 
allows some margin of error.


return_type
'''''''''''

Decorate your functions with the type or types you want your functions to
return, as shown in the examples below.

.. code:: python
    
    # aceppts both integers, float and complex numbers
    # to be returned
    @return_type(int, float, complex)
    def add(x,y):
        return x+y

    # only accept integers to be returned
    @return_type(int)
    def strict_add(x,y):
        return x+y

Known issues
------------

- When calling help on a decorated function the parameters are not shown
  correctly, instead it will just say <function name>(\*args, \*\*kwargs).
  Thanks to the functools.wraps decorator the docstring of a wrapped function
  will still be shown correctly.
- When using the inspect module to get the argument specification with
  inspect.getargspec or getting the source code from inspect.getsourcelines
  it will fail and show the wrapped function instead.


Bugs, problems and new features
-------------------------------

If you find any bugs, have any problems, or maybe you just want to request a 
new feature, then use the `issue tracker
<https://github.com/fredgj/typesys/issues>`_.

