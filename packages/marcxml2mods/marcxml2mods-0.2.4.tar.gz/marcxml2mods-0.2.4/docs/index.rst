marcxml2mods convertor
======================

The package is used for conversion of bibliographic data from MARC XML or OAI
to MODS format.

Package structure
-----------------

Relations between files in this package are captured at following image:

.. image:: /_static/relations.png
    :width: 600px

API
+++
:doc:`/api/marcxml2mods`:

.. toctree::
    :maxdepth: 1

    /api/transformators.rst
    /api/xslt_transformer.rst


:doc:`/api/mods_postprocessor/mods_postprocessor`:

.. toctree::
    :maxdepth: 1

    /api/mods_postprocessor/monograph.rst
    /api/mods_postprocessor/multi_monograph.rst
    /api/mods_postprocessor/periodical.rst
    /api/mods_postprocessor/shared_funcs.rst


:doc:`/api/xslt/xslt`:

.. toctree::
    :maxdepth: 1

    /api/xslt/MARC21slim2MODS3-4-NDK.rst
    /api/xslt/MARC21toMultiMonographTitle.rst
    /api/xslt/MARC21toPeriodicalTitle.rst


Installation
============
Module is hosted at `PYPI <https://pypi.python.org/pypi/marcxml2mods>`_, and
can be installed using `PIP`_::

    sudo pip install marcxml2mods

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29


Source code
-----------
Project is released as opensource (GPL) and source codes can be found at
GitHub:

- https://github.com/edeposit/marcxml2mods


Unittests
---------
Almost every feature of the project is tested by unittests. You can run those
tests using provided ``run_tests.sh`` script, which can be found in the root
of the project.

Requirements
++++++++++++
This script expects that pytest_ is installed. In case you don't have it yet,
it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/


Example
+++++++
::

    $ ./run_tests.sh
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.26 -- pytest-2.6.4
    plugins: cov
    collected 29 items 

    tests/test_transformators.py ..
    tests/test_xslt_transformer.py .........
    tests/mods_postprocessor/test_mods_postprocessor_init.py .
    tests/mods_postprocessor/test_monograph.py .......
    tests/mods_postprocessor/test_multi_monograph.py F
    tests/mods_postprocessor/test_periodical.py F
    tests/mods_postprocessor/test_shared_funcs.py ........

    =================================== FAILURES ===================================
    _________________________ test_postprocess_multi_mono __________________________

        def test_postprocess_multi_mono():
    >       raise NotImplementedError()
    E       NotImplementedError

    tests/mods_postprocessor/test_multi_monograph.py:27: NotImplementedError
    _________________________ test_postprocess_periodical __________________________

        def test_postprocess_periodical():
    >       raise NotImplementedError()
    E       NotImplementedError

    tests/mods_postprocessor/test_periodical.py:27: NotImplementedError
    ===================== 2 failed, 27 passed in 0.77 seconds ======================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
