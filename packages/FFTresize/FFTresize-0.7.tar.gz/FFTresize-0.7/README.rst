FFTresize resizes images using zero-padding in the frequency
domain.

|image0| |image1|

*New*: Get the app for OS X:
https://www.eliteraspberries.com/hecta/.

Installation
============

FFTresize requires docopt, PIL, and NumPy.

FFTresize consists of a package and a script.

To install these from the source code,

::

    gunzip < FFTresize-0.7.tar.gz | tar -xf -
    cd FFTresize-0.7/
    python setup.py install

or with pip,

::

    pip install fftresize

Usage
=====

The fftresize script accepts two arguments: the file name of
the image to resize, and a decimal factor by which to resize
the image (1.0 meaning no change).

::

    FFTresize - Resize images using the FFT

    Usage:
        fftresize <factor> <file>...
        fftresize -h | --help
        fftresize -v | --version

    Options:
        -h, --help      Print this help.
        -v, --version   Print version information.

Example
=======

Below is an example image, resized to twice its original size.

.. figure:: http://www.eliteraspberries.com/images/drink.png
   :alt: 

.. figure:: http://www.eliteraspberries.com/images/drink-2x.png
   :alt: 

.. |image0| image:: https://travis-ci.org/eliteraspberries/fftresize.svg
   :target: https://travis-ci.org/eliteraspberries/fftresize
.. |image1| image:: https://img.shields.io/pypi/v/FFTresize.svg
   :target: https://pypi.python.org/pypi/FFTresize
