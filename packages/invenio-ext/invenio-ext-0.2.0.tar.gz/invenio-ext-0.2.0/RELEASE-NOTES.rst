====================
 Invenio-Ext v0.2.0
====================

Invenio-Ext v0.2.0 was released on September 22, 2015.

About
-----

Invenio module that provides integration with Flask extensions.

*This is an experimental developer preview release.*

Incompatible changes
--------------------

- Removes `get_record` from global Jinja context.
- Removes possibility to import config as invenio package attribute.
  Replace `from invenio import config` by using `current_app.config`.
- Removes endpoints serving legacy webinterfaces and legacy admin
  pages.
- Removes bibdocfile dependency.

Bug fixes
---------

- Adds missing invenio-base, raven and redis dependencies.
- Adds missing dependencies to SQLAlchemy-Utils and intbitset.
- Adds missing invenio-celery>=0.1.0 dependency.
- Removes dependency on legacy WebUser module.

Installation
------------

   $ pip install invenio-ext==0.2.0

Documentation
-------------

   http://invenio-ext.readthedocs.org/en/v0.2.0

Happy hacking and thanks for flying Invenio-Ext.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: https://github.com/inveniosoftware/invenio-ext
|   URL: http://invenio-software.org
