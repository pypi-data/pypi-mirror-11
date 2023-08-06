====================
 Invenio-Ext v0.3.0
====================

Invenio-Ext v0.3.0 was released on October 2, 2015.

About
-----

Invenio module that provides integration with Flask extensions.

*This is an experimental developer preview release.*

Incompatible changes
--------------------

- Removes record related tasks in favor of `invenio-records`.

Bug fixes
---------

- Adds missing dependency to invenio-collections>=0.1.2.
- Removes references to invenio.config and replaces them with
  invenio_base.globals.cfg.
- Adds missing dependency to invenio-testing.
- Replaces if statement by try...except block to check if a model has
  a mixer associated with it.

Installation
------------

   $ pip install invenio-ext==0.3.0

Documentation
-------------

   http://invenio-ext.readthedocs.org/en/v0.3.0

Happy hacking and thanks for flying Invenio-Ext.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: https://github.com/inveniosoftware/invenio-ext
|   URL: http://invenio-software.org
