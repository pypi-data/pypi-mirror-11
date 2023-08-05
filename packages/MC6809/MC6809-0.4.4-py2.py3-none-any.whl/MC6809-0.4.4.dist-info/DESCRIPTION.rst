-------------------------------------
MC6809 CPU emulator written in Python
-------------------------------------

MC6809 is a Open source (GPL v3 or later) emulator for the legendary **6809** CPU, used in 30 years old homecomputer ``Dragon 32`` and ``Tandy TRS-80 Color Computer`` (CoCo)...

Tested with Python 2.7, 3.4 and PyPy

+-----------------------------------+-------------------------------+
| |Build Status on travis-ci.org|   | `travis-ci.org/6809/MC6809`_  |
+-----------------------------------+-------------------------------+
| |Coverage Status on coveralls.io| | `coveralls.io/r/6809/MC6809`_ |
+-----------------------------------+-------------------------------+

.. |Build Status on travis-ci.org| image:: https://travis-ci.org/6809/MC6809.svg
.. _travis-ci.org/6809/MC6809: https://travis-ci.org/6809/MC6809/
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/6809/MC6809/badge.svg
.. _coveralls.io/r/6809/MC6809: https://coveralls.io/r/6809/MC6809

A example usage can be find in: `MC6809/example6809.py <https://github.com/6809/MC6809/blob/master/MC6809/example6809.py>`_

There is a simple benchmark. Run e.g.:

::

    ~$ MC6809 benchmark --help

    # run benchmark with default settings:
    ~$ MC6809 benchmark

    # run with own settings:
    ~$ MC6809 benchmark --loops 10 --multiply 20

(**MC6809** is the cli installed by **setup.py**)

Unittest use `nose <https://pypi.python.org/pypi/nose/>`_, run them, e.g.:

::

    ~$ cd MC6809
    ~/MC6809 $ python2 setup.py nosetests
    ~/MC6809 $ python3 setup.py nosetests

TODO
====

#. Use bottle for http control server part

unimplemented OPs:

* RESET

* SWI / SWI2 / SWI3

* SYNC

-------
History
-------

(Some of the points are related to `DragonPy Emulator <https://github.com/jedie/DragonPy>`_)

* 10.08.2015 - `v0.4.4 <https://github.com/6809/MC6809/compare/v0.4.3...v0.4.4>`_ - bugfix and cleanup the tests

* 10.08.2015 - `v0.4.3 <https://github.com/6809/MC6809/compare/v0.4.2...v0.4.3>`_ - run unittests with nose

* 27.05.2015 - `v0.4.2 <https://github.com/6809/MC6809/compare/v0.4.1...v0.4.2>`_ - Add MC6809/example6809.py

* 26.05.2015 - `v0.4.0, 0.4.1 <https://github.com/6809/MC6809/compare/1a40593...v0.4.1>`_ - Split MC6809 from `DragonPy <https://github.com/jedie/DragonPy>`_

* 14.09.2014 - Release v0.2.0 - Add a speedlimit, config dialog and IRQ: `Forum post 11780 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&p=11780#p11780>`_

* 05.09.2014 - Release v0.1.0 - Implement pause/resume, hard-/soft-reset 6809 in GUI and improve a little the GUI/Editor stuff: `v0.1.0 <https://github.com/jedie/DragonPy/releases/tag/v0.1.0>`_ see also: `Forum post 11719 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&p=11719#p11719>`_.

* 27.08.2014 - Run CoCo with Extended Color Basic v1.1, bugfix transfer BASIC Listing with `8fe24e5...697d39e <https://github.com/jedie/DragonPy/compare/8fe24e5...697d39e>`_ see: `Forum post 11696 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=90#p11696>`_.

* 20.08.2014 - rudimenary BASIC IDE works with `7e0f16630...ce12148 <https://github.com/jedie/DragonPy/compare/7e0f16630...ce12148>`_, see also: `Forum post 11645 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=4439#p11645>`_.

* 05.08.2014 - Start to support CoCo, too with `0df724b <https://github.com/jedie/DragonPy/commit/0df724b3ee9d87088b524c3623040a41e9772eb4>`_, see also: `Forum post 11573 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11573>`_.

* 04.08.2014 - Use the origin Pixel-Font with Tkinter GUI, see: `Forum post 4909 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4909>`_ and `Forum post 11570 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11570>`_.

* 27.07.2014 - Copyrigth info from Dragon 64 ROM is alive with `543275b <https://github.com/jedie/DragonPy/commit/543275b1b90824b64b67dcd003cc5ab54296fc15>`_, see: `Forum post 11524 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11524>`_.

* 29.06.2014 - First "HELLO WORLD" works, see: `Forum post 11283 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=70#p11283>`_.

* 27.10.2013 - "sbc09" ROM works wuite well almist, see: `Forum post 9752 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=60#p9752>`_.

* 16.10.2013 - See copyright info from "Simple6809" ROM with `25a97b6 <https://github.com/jedie/DragonPy/tree/25a97b66d8567ba7c3a5b646e4a807b816a0e376>`_ see also: `Forum post 9654 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=50#p9654>`_.

* 10.09.2013 - Start to implement the 6809 CPU with `591d2ed <https://github.com/jedie/DragonPy/commit/591d2ed2b6f1a5f913c14e56e1e37f5870510b0d>`_

* 28.08.2013 - Fork "Apple ][ Emulator" written in Python: `https://github.com/jtauber/applepy <https://github.com/jtauber/applepy>`_ to `https://github.com/jedie/DragonPy <https://github.com/jedie/DragonPy>`_

------
Links:
------

+--------+---------------------------------------------------+
| Forum  | `http://forum.pylucid.org/`_                      |
+--------+---------------------------------------------------+
| IRC    | `#pylucid on freenode.net`_                       |
+--------+---------------------------------------------------+
| Jabber | pylucid@conference.jabber.org                     |
+--------+---------------------------------------------------+
| PyPi   | `https://pypi.python.org/pypi/DragonPyEmulator/`_ |
+--------+---------------------------------------------------+
| Github | `https://github.com/jedie/DragonPy`_              |
+--------+---------------------------------------------------+

.. _http://forum.pylucid.org/: http://forum.pylucid.org/
.. _#pylucid on freenode.net: http://www.pylucid.org/permalink/304/irc-channel
.. _https://pypi.python.org/pypi/DragonPyEmulator/: https://pypi.python.org/pypi/DragonPyEmulator/

--------
donation
--------

* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2F6809%2FMC6809%2F>`_

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

