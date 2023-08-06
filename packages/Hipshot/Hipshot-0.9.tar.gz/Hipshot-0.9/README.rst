Hipshot converts a video file or series of photographs into a
single image simulating a long-exposure photograph.

|image0| |image1|

Installation
============

Hipshot requires:

-  Python 2;
-  docopt;
-  the `Avena <https://pypi.python.org/pypi/Avena>`__ library;
-  the FFMPEG libraries; and
-  OpenCV and its Python bindings.

Install Hipshot with `pip <https://pip.pypa.io/en/stable/>`__:

::

    pip install hipshot

Usage
=====

The hipshot script takes a single argument: the video file.

::

    Hipshot - Simulate long-exposure photography

    Usage:
        hipshot video <file> [--display=<bool>]
        hipshot photos <file>... [--display=<bool>]
        hipshot -h | --help
        hipshot -v | --version

    Options:
        -d, --display=<bool>    Display the process [default: True].
        -h, --help              Print this help.
        -v, --version           Print version information.

Example
=======

The following image was created from the video: `ISS Near
Aurora
Borealis <http://www.youtube.com/watch?v=uYBYIhH4nsg>`__.

.. figure:: http://www.eliteraspberries.com/images/iss-borealis.png
   :alt: 

.. |image0| image:: https://travis-ci.org/eliteraspberries/hipshot.svg
   :target: https://travis-ci.org/eliteraspberries/hipshot
.. |image1| image:: https://img.shields.io/pypi/v/Hipshot.svg
   :target: https://pypi.python.org/pypi/Hipshot
