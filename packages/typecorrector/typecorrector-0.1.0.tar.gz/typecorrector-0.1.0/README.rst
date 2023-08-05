Type corrector
==============


Intro
-----

Type corrector is module that contains the decorator type_corrector.
This decorator let's the user specify what types the 
arguments to a function should have. It's not 100% safe to use as it
might result in a ValueError or TypeError if the user is not careful enough.
The motivation behing this module was to find a way that makes it easier
for the programmer to see what types the arguments should be, and at 
the same time allow some margin of error.
I'm not sure if this is a good idea, or if it's a good approach. It was
mostly developed for fun while playing around with decorators.

       
Usage
-----
First import type_corrector from typecorrector:

.. code:: python

    from typecorrector import type_corrector

Then you can decorate your functions with type_corrector

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

.. code:: python

    @type_corrector(int)
    def kw_mult(**kwargs):
        first = kwargs.get('first')
        second = kwargs.get('second')
        third = kwargs.get('third')
        return first * second * third


This allows us to call the functions like this:
mult('2', '3', '4')
kw_mult(first='2', second='3', third='3')

By looking at the function definitions we can still see that
the both parameters of add are supposed to be integers and mult and kw_mult
also work with integers. By decorating the functions this it should be a clear
hint what types we want to operate with, even though it allows some margin of
error.


Known issues
------------
When calling help on a decorated function the parameters are not shown
correctly, instead it will just say <function name>(\*args, \*\*kwargs)
Also, when using inspect to get the argument specification with
inspect.getargspec or getting the source code from inspect.getsourcelines
it will fail.
Thanks to the functools.wraps decorator the docstring of a wrapped function
will still shown correctly.
