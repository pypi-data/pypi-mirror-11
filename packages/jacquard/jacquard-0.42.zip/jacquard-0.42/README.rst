========
Jacquard
========
Suite of command-line tools to expedite analysis of exome variant data from 
multiple patients and multiple variant callers.

.. image:: https://travis-ci.org/umich-brcf-bioinf/Jacquard.svg?branch=develop
    :target: https://travis-ci.org/umich-brcf-bioinf/Jacquard
    :alt: Build Status

.. image:: https://coveralls.io/repos/umich-brcf-bioinf/Jacquard/badge.png?branch=develop
    :target: https://coveralls.io/r/umich-brcf-bioinf/Jacquard?branch=develop
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/l/Jacquard.svg
    :target: https://pypi.python.org/pypi/jacquard/
    :alt: License

.. image:: http://img.shields.io/pypi/v/colour.svg?style=flat
   :target: https://pypi.python.org/pypi/jacquard/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Jacquard.svg
   :target: https://pypi.python.org/pypi/jacquard/
    :alt: Downloads Counter

The official repository is at:

https://github.com/umich-brcf-bioinf/Jacquard

Usage
=====

::

   $ jacquard <subcommand> [options] [arguments]

*Subcommands*

:translate:
   Creates new VCFs, adding a controlled vocabulary of new FORMAT tags.
:merge:
   Integrates a directory of VCFs into a single VCF.
:summarize:
   Adds new INFO fields and FORMAT tags that combine variant data from the
   merged VCF.
:expand:
   Explodes a VCF file into a tab-delimited file.

For help on a specific subcommand:

::

   $ jacquard <subcommand> --help


See `ReadTheDocs <http://jacquard.readthedocs.org/>`_ for full documentation.

====

Email bfx-jacquard@umich.edu for support and questions.

UM BRCF Bioinformatics Core

