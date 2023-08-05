=====
perth
=====
.. image:: https://travis-ci.org/tomokinakamaru/perth.svg?branch=master
    :target: https://travis-ci.org/tomokinakamaru/perth
    :alt: perth Build

About
=====

Wrapper for `threading.local` with enhanced value accessor.

Example
=======

.. sourcecode:: python

    import threading
    from perth import Perth

    # instanciate Perth and set a seed value.
    pth = Perth()
    pth.set_seed('counter', 0)

    # use in main thread
    pth.counter += 2


    # use in sub thread
    def f():
        pth.counter += 3
        print(pth.counter)  # will print 3

    t = threading.Thread(target=f)
    t.start()
    t.join()

    # result in main thread
    print(pth.counter)  # will print 2
    print(pth.get_seed('counter'))  # will print 0
