============
Installation
============

Follow the instructions below to install |IGT|.

Requirements
============

|Python_supp|. (Note: Python 2 is not supported.)

We also recommend, but do not require, using Python virtual environments. For
more information, see documentation for venv_ or Anaconda_.

.. _venv: https://docs.python.org/3/tutorial/venv.html
.. _Anaconda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

Installation
============

Install the package to your environment using::

        pip install idmtools-git-tags --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple


Quick start guide
=================

After installation, the default configurations add git tags to all Experiment, Simulations, WorkItems, AssetCollections
upon their creation.

To change this behaviour, see Configuration