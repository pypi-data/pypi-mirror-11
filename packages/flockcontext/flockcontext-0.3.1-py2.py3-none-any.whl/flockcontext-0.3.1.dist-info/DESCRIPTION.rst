===============================
Flockcontext
===============================

.. image:: https://img.shields.io/travis/AntoineCezar/flockcontext.svg
        :target: https://travis-ci.org/AntoineCezar/flockcontext

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
        :target: http://flockcontext.readthedocs.org/

.. image:: https://img.shields.io/coveralls/AntoineCezar/flockcontext.svg
        :target: https://coveralls.io/github/AntoineCezar/flockcontext

.. image:: https://img.shields.io/pypi/v/flockcontext.svg
        :target: https://pypi.python.org/pypi/flockcontext


Improves `fcntl.flock <https://docs.python.org/library/fcntl.html#fcntl.flock>`_ usage.

``flock`` is a Unix command for `file locking <https://en.wikipedia.org/wiki/File_locking>`_,
the mecanism that controls access restrictions of files.

Usage
-----

Exclusive blocking lock::

    from flockcontext import FlockOpen

    with FlockOpen('/tmp/my.lock', 'w') as lock:
        lock.fd.write('Locked\n')

Exclusive non-blocking lock::

    from flockcontext import FlockOpen

    try:
        with FlockOpen('/tmp/my.lock', 'w', blocking=False) as lock:
            lock.fd.write('Locked\n')
    except IOError as e:
        print('Can not acquire lock')

Shared blocking lock::

    from flockcontext import Flock

    with FlockOpen('/tmp/my.lock', 'w', exclusive=False) as lock:
        lock.fd.write('Locked\n')

Acquire and release within context::

    from flockcontext import FlockOpen

    with FlockOpen('/tmp/my.lock', 'w') as lock:
        print('Lock acquired')
        lock.fd.write('Locked\n')

        lock.release()
        print('Lock released')

        lock.acquire()
        print('Lock acquired')
        lock.fd.write('Locked\n')

Locking alredy opened file::

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd):
            fd.write('Locked\n')

License
-------

* Free software: BSD license




History
-------

0.3.1 (2015-08-24)
------------------

* Add syntax highlighting for code exemples
* Add Flock manager exemple in README

0.3.0 (2015-08-21)
------------------

* Add FlockOpen context manager.

0.2.0 (2015-08-20)
------------------

* Add Flock relase and acquire capability withing context.

0.1.0 (2015-08-19)
------------------

* Add Flock context manager.


