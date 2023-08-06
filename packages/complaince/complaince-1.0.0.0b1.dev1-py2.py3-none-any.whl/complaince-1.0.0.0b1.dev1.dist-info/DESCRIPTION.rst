# Complaince
A python function parameter and return type-checking decorator

Both the parameters types and return type(optional to check for return type)
can be done using a single decorator. 

Each parameter can have multiple possible types , mentioned in a tuple

Examples
========
When plainly checking parameter types

```python
   @param_check((int,float),(int,float))
   def myfunc(a, b):
```
This indicates the parameters a,b can be either int or float

```python
   @param_check((int,),(int,))
   def myfunc(a, b):
```
In this case both a and b have to be int only (tuple definition is a must )

There is are two optional parameters:

1. level - Key-Value pair indicates warning message(continue execution after type error) or throw an exception(essentially
   terminating the execution flow) (0 - warning , 1 - exception error) Default
   is warning i.e 0

2. ret - Key-Value pair indicating possible return types, in this case too
   value is a tuple

```python
   @param_check((int,float),(int,float), level = 1, ret = (int,float))
   def myfunc(a, b)
```
In the above example we will throw an exception if the parameters, return value do not match
required types. Return value can be either an in or float

Compatability
=============
Requires python 2.6 or higher
Works with python 3.0 and higher



