===============
Developer guide
===============

Bug Reports and Feature Requests
================================

If you have encountered a problem with Kobin or have an idea for a new feature,
please submit it to the issue tracker on Github.

Including or providing a link to the source files involved may help us fix the issue. If possible,
try to create a minimal project that produces the error and post that instead.

Documentation
=============

Build
-----

* English: ``make html``
* Japanese: ``make -e SPHINXOPTS="-D language='ja'" html``


Translation
-----------

Updating your po files by new pot files.

..code-block:: console

   $ make gettext
   $ sphinx-intl update -p build/locale
   # edit doc/source/locale/*.po files
   $ make -e SPHINXOPTS="-D language='ja'" html

Reference: `Internationalization -- Sphinx documentation <http://www.sphinx-doc.org/en/stable/intl.html>`_


Testing
=======

The following test are running in Kobin project.
If you add the changes to Kobin, Please run tox testing.

* pytest: ``python setup.py test``
* mypy: ``mypy --check-untyped-defs --fast-parser --python-version 3.6 kobin``
* Flake8: ``flake8``
* doctest: ``cd docs; make doctest``
