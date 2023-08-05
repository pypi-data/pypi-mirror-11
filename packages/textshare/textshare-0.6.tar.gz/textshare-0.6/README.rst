=========
textshare
=========

*A simple command line utility to share code and texts*

Download python package here `pypi <https://pypi.python.org/pypi/textshare/>`_

Submit issues here `github <https://github.com/bindingofisaac/textshare>`_

============
installation
============

.. code-block:: bash

    $ pip install textshare

=====
usage
=====

textshare [OPTIONS] [FILEPATHS]...

Options:

--input      uses stdin as input

--map        returns output as a map of filepaths and url

--help       Show this message and exit.

========
examples
========

.. code-block:: bash 

    $ texshare file1 file2
    
    $ cat file | textshare -i

    $ texshare --map file1 file2 | textshare -i

====
TODO
====

Split large files into chunks
