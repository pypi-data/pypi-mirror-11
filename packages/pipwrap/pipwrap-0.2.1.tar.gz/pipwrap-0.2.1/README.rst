pipwrap
=======

|Build Status| |Coverage Status| |PyPI Version| |Supported Versions| |Downloads|

pipwrap simplifies handling Python project requirements across multiple
environments. pip freeze > requirements.txt gets your project started,
but do you really want mock, coverage, etc. installed on your production
server? If you've ever found yourself sifting through the output of pip
freeze trying to figure out what packages you've installed but didn't yet
add to one of your requirements files, then pipwrap is the tool for you.

Features
--------

-  Create or update requirements files based on installed packages
-  Remove stray packages in virtualenv
-  List discrepancies between installed packages and requirements files

Installation
------------

You can get pipwrap from PyPI with:

::

    pip install pipwrap

The development version can be installed with:

::

    pip install -e git://github.com/jessamynsmith/pipwrap.git#egg=pipwrap

If you are developing locally, your version can be installed from the
working directory with:

::

    python setup.py.install

Usage
-----

Note: You may ignore warnings about "Recursive requirements not supported." These
are due to current limitations of the requirements-parser library.

**Getting Started with pipwrap**

1. (Optional) Create requirements files with a list of your packages

2. Interactively populate requirements files from currently installed
   packages:

   pipwrap -r

3. Create a top-level requirements.txt file that points to your
   production requirements, e.g. "-r production.txt"

**Keeping requirements up to date with pipwrap**

1. Interactively update requirements files from currently installed
   packages:

   pipwrap -r  # Adds packages in virtualenv

   pipwrap -rc  # Adds packages in virtualenv and removes packages not in virtualenv

2. Remove stray packages in virtualenv:

   pipwrap -x

3. See discrepancies between installed packages and requirements files:

   pipwrap -l

NOTE: This last option can be used to determine what the other options would do. Any packages
in the "Packages installed but not present in requirements" section would be uninstalled with
the -x option or added to requirements with the -r option. Any packages in the "Packages present
in requirements but not installed" section would be removed from the requirements files with the
-rc option.

Development
-----------

Fork the project on github and git clone your fork, e.g.:

::

    git clone https://github.com/<username>/pipwrap.git

Create a virtualenv and install dependencies:

::

    mkvirtualenv pipwrap
    pip install -r requirements/package.txt -r requirements/test.txt

Run tests with coverage (should be 100%) and check code style:

::

    coverage run -m nose
    coverage report -m
    flake8

Verify all supported Python versions:

::

    pip install tox
    tox

Install your local copy:

::

    python setup.py.install

.. |Build Status| image:: https://circleci.com/gh/jessamynsmith/pipwrap.svg?style=shield
   :target: https://circleci.com/gh/jessamynsmith/pipwrap
.. |Coverage Status| image:: https://coveralls.io/repos/jessamynsmith/pipwrap/badge.svg?branch=master
   :target: https://coveralls.io/r/jessamynsmith/pipwrap?branch=master
.. |PyPI Version| image:: https://pypip.in/version/pipwrap/badge.svg
   :target: https://pypi.python.org/pypi/pipwrap
.. |Supported Versions| image:: https://pypip.in/py_versions/pipwrap/badge.svg
   :target: https://pypi.python.org/pypi/pipwrap
.. |Downloads| image:: https://pypip.in/download/pipwrap/badge.svg
   :target: https://pypi.python.org/pypi/pipwrap
