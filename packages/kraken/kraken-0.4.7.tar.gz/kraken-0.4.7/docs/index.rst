kraken
======

.. toctree::
   :hidden:
   :maxdepth: 2

   advanced
   API <api>
   Models <models>

kraken is a turn-key OCR system forked from `ocropus
<https://github.com/tmbdev/ocropy>`_. It is intended to rectify a number of
issues while preserving (mostly) functional equivalence. 

If you already got a model trained for ocropus you can always expect it to work
with kraken without all the fuss of the original ocropus tools.

Features
========

kraken's main features are:

  - Explicit input/output handling
  - Word bounding boxes and character cuts in hOCR
  - Removal of runtime dependency on gcc
  - Removal of unused spaghetti code
  - :ref:`Lightweight model files <models>`

Currently missing or underdocumented are:

  - Clean public API 
  - Tests
  - CLSTM compatibility
  - New training interface (possibly only for CLSTM)

All functionality not pertaining to OCR and prerequisite steps has been
removed, i.e. no more ground truth editing, error rate measuring, etc.

Pull requests and code contributions are always welcome. 

Installation
============

While kraken does not require a working C compiler on run-time anymore numpy
and scipy compilation still requires build-essential or your distributions
equivalent and some dependencies. Additionally we require require a `HDF5
<https://www.hdfgroup.org/HDF5/>`_ library for `h5py <http://h5py.org>`_ to
link against.

.. code-block:: console

        # apt-get install gcc gfortran python-dev libblas-dev liblapack-dev
        cython libhdf5-dev

Because the build behavior of pip versions older than 6.1.0 interferes with the
scipy build process numpy has to be installed before doing the actual install:

.. code-block:: console

  # pip install numpy

Install kraken either from pypi:

.. code-block:: console

  $ pip install kraken

or by running pip in the git repository:

.. code-block:: console

  $ pip install .

.. note::

  While kraken is Python 2/3 compliant, there are limits to its compatibility.
  For various reasons it is not possible to use :ref:`pickled models
  <pyrnn>` under Python 3. As the vast majority of models are still in
  the legacy format it is recommended to use Python 2.7.

Finally you'll have to scrounge up an RNN to do the actual recognition of
characters. To download ocropus' default RNN converted to the new format and
place it in the kraken directory for the current user:

.. code-block:: console

  $ kraken download

Quickstart
==========

To binarize a single image using the nlbin algorithm:

.. code-block:: console

  $ kraken binarize grey.png bw.png

To segment a binarized image into reading-order sorted lines:

.. code-block:: console

  $ kraken segment bw.png lines.txt

To OCR a binarized image using the default RNN and the previously generated
page segmentation:

.. code-block:: console

  $ kraken ocr --lines lines.txt bw.png
  Loading RNN     ✓
  Reading line bounds  [####################################]  100%
  Recognizing lines  [######------------------------------]   17%  00:00:17


.. _license:

License
=======

``Kraken`` is provided under the terms and conditions of the `Apache 2.0
License <https://github.com/mittagessen/kraken/blob/master/LICENSE>`_ retained
from the original ``ocropus`` distribution.
