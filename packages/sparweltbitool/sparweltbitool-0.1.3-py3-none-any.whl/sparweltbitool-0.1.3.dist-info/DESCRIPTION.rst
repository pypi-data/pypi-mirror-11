============
sparwelttool
============

Goal and responsibility
=======================

Python library with standard modules used by Sparwelt GmbH BI Team in Web Services.

Publishing in PyPI (Ubuntu 14.04)
===========================================

Create file for authorization to pypi ~/.pypirc

::

    [server-login]
    username:sparwelt
    password:<PASSWORD_HERE>

Install all tools required for submiting new version to PyPI

::

    virtualenv -p /usr/bin/python3 dev
    pip install -U "pip>=1.4" "setuptools>=0.9" "wheel>=0.21"
    python3 setup.py register
    python3 setup.py sdist bdist_wheel upload


Command 'python setup.py register' is required only on creation of package.
On every new upload new version should be created.
Keep Semantic Versioning like described in: http://semver.org/.

