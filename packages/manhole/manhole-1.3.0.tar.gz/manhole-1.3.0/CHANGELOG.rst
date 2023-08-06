
Changelog
=========

1.3.0 (2015-09-03)
------------------

* Allowed Manhole to be configured without any thread or activation (in case you want to manually activate).
* Added an example and tests for using Manhole with uWSGi.
* Fixed error handling in ``manhole-cli`` on Python 3 (exc vars don't leak anymore).
* Fixed support for running in gevent/eventlet-using apps on Python 3 (now that they support Python 3).
* Allowed reinstalling the manhole (in non-``strict`` mode). Previous install is undone.

1.2.0 (2015-07-06)
------------------

* Changed ``manhole-cli``:

  * Won't spam the terminal with errors if socket file doesn't exist.
  * Allowed sending any signal (new ``--signal`` argument).
  * Fixed some validation issues for the ``PID`` argument.

1.1.0 (2015-06-06)
------------------

* Added support for installing the manhole via the ``PYTHONMANHOLE`` environment variable.
* Added a ``strict`` install option. Set it to false to avoid getting the ``AlreadyInstalled`` exception.
* Added a ``manhole-cli`` script that emulates ``socat readline unix-connect:/tmp/manhole-1234``.

1.0.0 (2014-10-13)
------------------

* Added ``socket_path`` install option (contributed by `Nir Soffer`_).
* Added ``reinstall_delay`` install option.
* Added ``locals`` install option (contributed by `Nir Soffer`_).
* Added ``redirect_stderr`` install option (contributed by `Nir Soffer`_).
* Lots of internals cleanup (contributed by `Nir Soffer`_).

0.6.2 (2014-04-28)
------------------

* Fix OS X regression.

0.6.1 (2014-04-28)
------------------

* Support for OS X (contributed by `Saulius Menkevičius`_).

.. _Saulius Menkevičius: https://github.com/razzmatazz
.. _Nir Soffer: https://github.com/nirs
