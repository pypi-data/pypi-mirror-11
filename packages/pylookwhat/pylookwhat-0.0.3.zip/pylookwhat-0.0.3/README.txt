pylookwhat
==========

Sometimes when we need to reference other project's settings to do something, we can use execfile to parse file get variable inside. But a few things can make it difficult:

1. Dependency package(s) are not installed
2. Relative module(s) not in sys.path
3. Local module name confused due to scoping. 

Use pylookwhat to solve these

::

    import pylookwhat

    what = {}
    lookwhat = [ 'A', 'B'  ]
    filename = 'what.py'
    pylookwhat.lookwhat( filename, what, lookwhat  )

    print what
    
    
    

what.py

::

	A = { "Hello": "World" }
	B = [ 1, 2, 3 ]
	

Patch
-----
Modify variables in script. Backup file will be named with datetime.
::

    python -m pylookwhat patch target.py source.py false


target.py

::

    A="Hello"
    B=123


source.py

::

    A = "Hello World"

Patched target.py

::

    A = "Hello World"
    B=123


1.0.3
	Fix missing text when patch with dict variables