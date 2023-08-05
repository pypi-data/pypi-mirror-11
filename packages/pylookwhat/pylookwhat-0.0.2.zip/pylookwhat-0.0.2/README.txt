pylookwhat
==========

Sometimes need reference other project's settings to do something, 
Could use execfile to parse file get variable inside .
But something make difficult

1. Dependency packages are not installed
2. Relative modue not in sys.path
3. Local module name confused

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
Modify variables in script. backup file will be named with datetime.
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

