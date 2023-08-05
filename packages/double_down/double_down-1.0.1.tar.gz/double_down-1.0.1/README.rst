Double down
-----------

A silly example of a python decorator.

Simply calls the decorated function twice.


Installation
------------

Double down has been published to python package index and is available via pip:

::

    pip install double_down

Otherwise, if you want to install it manually:

::

    git clone git@github.com:smelnicki/double_down.git
    sudo python setup.py install


Usage
------------

This is about as simple as it gets when it comes to decorators. It literally makes
your function code execute twice.

For example, see below:

.. code:: python

    # example.py
    from double_down import double_down

    @double_down
    def hello():
        print "Hello, Python"

    if __name__ == "__main__":
      hello()


Then in your terminal:

::

    > python example.py
    Hello, Python
    Hello, Python


Questions
------------

This project was just a fun little foray into learning how decorators work. In all
honesty, it'd be a big stretch of the imagination to justify its use in some real
life application.

If you're curious how decorators work or want to get some hands on experience, I'd
strongly encourage making one of your own. There's plenty of documentation out there
to use.
