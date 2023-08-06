Bokuno Python Console
=======================

Bokuno-py-console helps python developers to easily get all the arguments from console as a python Dictionary.

Installation
------------
You can easily install 

``pip install bokuno-py-console``

Requirements
------------
Python 3

Usage
-----

``import bokuno_console``

``args = bokuno_console.get_args()``

Example
-------

``python your_script.py -p1 PARAMETER_1_VALUE -p2 PARAMETER_2_VALUE``

Import bokuno_console and run **get_args()** method to fetch arguments. It will return python dictionary formatted like this:
``{'-p1': 'PARAMETER_1_VALUE', '-p2': 'PARAMETER_2_VALUE'}``