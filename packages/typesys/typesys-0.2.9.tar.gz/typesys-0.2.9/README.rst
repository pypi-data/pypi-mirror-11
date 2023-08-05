Typesys
=======


Intro
-----

Typesys is a module that is meant to make it more easy to manage types.
It contains four decorators; type_hints, type_corrector, return_type and
returns.

The *type_hints* decorator lets the user specify what the arguements of
a functions should be. If arguments of another type than specified in the
decorator are passed in, a TypeError will be raised.

The *type_corrector* decorator lets the user specify what types the 
arguments to a function should have, but not necessarily are passed in as,
which means it allows some margin of error. It's not 100% safe to use as it
still might result in a ValueError or TypeError if the user isn't careful enough.

The *return_type decorator* lets the user specify what type the decoratred
function should return. A TypeError will be raised if the function tries to 
return a value of another type.

The *returns* decorator lets the user specify what type a function's return type 
has to be (if possible to return this a value of this type). 

The motivation behing this module was to abstract some of the type checking and
type casting to a higher level. I wanted to find a way that makes it easier
for the programmer to see what types the arguments should be, what a type
a function should return or must return, and at the same time allow some margin 
of error (in case of type_corrector).
I'm not sure whether this is a good idea or not, or if it's a good approach.
It was mostly developed for fun while playing around with decorators.


Installation
------------

pip install typesys


Usage
-----

First import the decorators from the typesys module:

.. code:: python

    from typesys import type_hints, type_corrector, return_type, returns

Then you are ready to start decorating your functions.

type_hints
''''''''''

Decorate your functions with the types you want the arguments to be, as shown in
the examples below

.. code:: python
    
    # a and b must be integers
    @type_hints(int, int)
    def add(a, b):
        return a+b


    # also work with default arguments
    @type_hints(int, float)
    def add(a, b=0.0):
        return a+b


    # accepts both integers and floating 
    # point numbers as arguments
    @type_hints(int, float)
    def mult(*numbers):
        result = 1
        for num in numbers:
            result *= num
        return result


    # Only accept integer arguments
    @type_hints(int)
    def mult(**kwargs):
        x = kwargs.get('x')
        x = 1 if x is None else x
        y = kwargs.get('y')
        y = 1 if y is None else y
        z = kwargs.get('z')
        z = 1 if z is None else z
        return x * y * z


  
type_corrector
''''''''''''''

Decorate your functions with the types you want the arguments to be treated as, 
but not necessarily are passed in as, as shown in the examples below.

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
    def mult(**kwargs):
        x = kwargs.get('x')
        x = 1 if x is None else x
        y = kwargs.get('y')
        y = 1 if y is None else y
        z = kwargs.get('z')
        z = 1 if z is None else z
        return x * y * z   


This allows us to call the functions like this:

- mult(2, '3', '4') 
- kw_mult(x=2, y='3', z='4')

When looking at the function definitions of add, mult and kw_mult we can easily
see that the arguments are supposed to be integers.
By decorating the functions like this it should also be a clear
hint what types we want the arguments to be passed in as, even though it 
allows some margin of error.


return_type
'''''''''''

Decorate your functions with the type or types you want your functions to
return, as shown in the examples below.

.. code:: python
    
    # accepts both integers, floatint point numbers 
    # and complex numbers to be returned
    @return_type(int, float, complex)
    def add(x,y):
        return x+y


    # only accept integers to be returned
    @return_type(int)
    def strict_add(x,y):
        return x+y


The same applies for functions defined with \*args and/or \*\*kwargs

.. code:: python

    # accepts both integers and floating point numbers
    # to be returned
    @return_type(int, float)
    def mult(*numbers):
        res = 1
        for number in numbers:
            res *= number
        return res

    # only accepts integers to be returned
    @return_type(int)
    def stric_kw_mult(**kwargs):
        x = kwargs.get('x')
        x = 1 if x is None else x
        y = kwargs.get('y')
        y = 1 if y is None else y
        z = kwargs.get('z')
        z = 1 if z is None else z
        return x * y * z


returns
'''''''

Decorate your functions with the type your funcitons must return, as long as
it's possible.

.. code:: python

    # returns x+y as a string
    @returns(str)
    def add(x,y):
        return x+y
   

A call to add(1,2) will return the number 3 as a string.


Known issues
------------

- When calling help on a decorated function the parameters are not shown
  correctly, instead it will just say <function name>(\*args, \*\*kwargs).
  Thanks to the functools.wraps decorator the docstring of a decorated function
  will still be shown correctly.
- When using the inspect module to get the argument specification with
  inspect.getargspec or getting the source code from inspect.getsourcelines
  it will fail and show the wrapped function instead.


Bugs, problems and new features
-------------------------------

If you find any bugs, have any problems, or maybe you just want to request a 
new feature, then use the `issue tracker
<https://github.com/fredgj/typesys/issues>`_.

