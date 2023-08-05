======
pygcvs
======

.. image:: https://requires.io/github/zsiciarz/pygcvs/requirements.png?branch=master
    :target: https://requires.io/github/zsiciarz/pygcvs/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/pypi/v/pygcvs.svg
    :target: https://pypi.python.org/pypi/pygcvs/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/pygcvs.svg
    :target: https://pypi.python.org/pypi/pygcvs/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/pyversions/pygcvs.svg
    :target: https://pypi.python.org/pypi/pygcvs/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/pygcvs.svg
    :target: https://pypi.python.org/pypi/pygcvs/
    :alt: Wheel Status

.. image:: https://travis-ci.org/zsiciarz/pygcvs.svg?branch=master
    :target: https://travis-ci.org/zsiciarz/pygcvs

.. image:: https://coveralls.io/repos/zsiciarz/pygcvs/badge.png?branch=master
    :target: https://coveralls.io/r/zsiciarz/pygcvs?branch=master

A Python library for reading variable star data from the
`General Catalog of Variable Stars <http://www.sai.msu.su/gcvs/gcvs/iii/html/>`_.

Installation
------------

Use ``pip`` to install latest release available at PyPI::

    pip install pygcvs

Usage
-----

Download the ``iii.dat`` file from `GCVS <http://www.sai.msu.su/gcvs/gcvs/iii/>`_
and point the ``read_gcvs`` function at its location.
The function returns a generator which yields a single star data dictionary
at a time. See below::

    >>> import pygcvs
    >>> for star in pygcvs.read_gcvs('iii.dat'):
    ...     print(star['name'])
    R AND
    S AND
    #...
    V0515 VUL
    V0516 VUL

Resources
---------

 * `Documentation <http://pygcvs.rtfd.org>`_
 * `Issue tracker <https://github.com/zsiciarz/pygcvs/issues>`_
 * `CI server <https://travis-ci.org/zsiciarz/pygcvs>`_

Author
------

 * `Zbigniew Siciarz <http://siciarz.net>`_ (zbigniew at siciarz dot net)

License
-------

pygcvs is free software, licensed under the MIT/X11 License. A copy of
the license is provided with the source code in the LICENSE file.
