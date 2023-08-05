=================
Outernet Metadata
=================

This package contains tools for working with Outernet metadata.

Prerequisites
=============

Before you can use the scripts in this package, you will need Python_ 2.7.x or
3.4.x or newer installed. Depending on the platform, you will also need to
install pip_. In some cases these are installed with Python.

You will also need to be familiar with the command consoles (Command Prompt,
terminals, etc). You will also need an editor. If you are on Windows, avoid
using Notepad. Instead install SublimeText_ or any of the other more
fully-featured editors.

Installing
==========

To install this package, use pip. In your command console type the following::

    pip install outernet-metadata

For command line tools, conz is also required, but it is not installed
automatically to allow outernet-metadata's use as a library. To install conz::

    pip install conz

Getting started
===============

Please refer to the `Content packaging HOWTO`_ to get started.

About Outernet and Outernet content
===================================

Outernet_ is a data broadcast service with a goal of universal uncensored
information disemination (primarily) among the population without Internet 
access.

Outernet broadcasts content from the web packaged in a ZIP file that contains
metadata about the content. This package provides functionality for working
with the metadata.

Scripts
=======

This package contains two scripts (when installed using setuptools/pip). These
are:

- metacheck
- metagen
- imgcount

Please run each with ``-h`` switch to see usage notes.

About the metadata specification
================================

Official Outernet metadata specification is maintained as part of this
repository. You will find them in the `content-metadata-specification.rst`_ 
file.

.. _Python: https://www.python.org/
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _pip: https://pypi.python.org/pypi/pip/
.. _SublimeText: http://www.sublimetext.com/
.. _Content packaging HOWTO: docs/packaging-howto.rst
.. _Outernet: https://www.outernet.is/
.. _content-metadata-specification.rst: docs/content-metadata-specification.rst
