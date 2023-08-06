devpi-web: web interface plugin for devpi-server
================================================

This plugin adds a web interface with search for `devpi-server`_.

.. _devpi-server: http://pypi.python.org/pypi/devpi-server


Installation
------------

``devpi-web`` needs to be installed alongside ``devpi-server``.

You can install it with::

    pip install devpi-web

There is no configuration needed as ``devpi-server`` will automatically discover the plugin through calling hooks using the setuptools entry points mechanism.


Changelog
=========

2.4.1 (2015-10-09)
------------------

- fix issue255: close and discard whoosh searchers after each use, they use too
  much memory if stored in a thread local for reuse.


2.4.0 (2015-07-09)
------------------

- macros.pt: Add autofocus attribute to search field

- macros.pt and style.css: Moved "How to search?" to the right of the search
  button and adjusted width of search field accordingly.

- fix issue244: server status info

  - added support for status message plugin hook ``devpiweb_get_status_info``
  - macros.pt: added macros ``status`` and ``statusbadge`` and placed them
    below the search field.
  - added status.pt: shows server status information

- toxresults.pt: fix missing closing ``div`` tag.


2.3.0 (2015-05-13)
------------------

- toxresults.pt: use just one line for result status indicator

- adapt devpi-web to devpi-server-2.2.0 hash-spec changes

- version.pt: moved hash to title attribute of table cell. With the upcoming
  change to sha256 it's too long and it's available from the link url as well.

- use renamed devpiserver_run_commands hook 

- fix issue233: projects on root/pypi with no releases lead to a traceback


2.2.3 (2015-02-24)
------------------

- fix issue207: added documentation url for latest stable release of a package.


2.2.2 (2014-11-27)
------------------

- fix issue184: better height calculation of documentation iframe.



