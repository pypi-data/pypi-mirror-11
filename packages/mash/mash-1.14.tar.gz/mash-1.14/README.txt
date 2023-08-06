=============
Mash
=============

A tool that creates objects from hash recursive.


Install
=======

.. code-block:: sh

    $pip install mash

Usage
=====

.. code-block:: python

    from Mash import Mash

    dict_instance = {'a':1, 'b':{'c':2}}
    object = Mash(dict_instance)
    print object.a


License
=======

MIT