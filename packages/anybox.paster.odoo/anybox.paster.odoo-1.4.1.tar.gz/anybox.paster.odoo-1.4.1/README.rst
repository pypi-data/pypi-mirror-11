anybox.paster.odoo
==================

Collection of paster templates that can be used to quickly create an Odoo instance or module

.. contents::

Install the templates
~~~~~~~~~~~~~~~~~~~~~

You can either use::

    pip install anybox.paster.odoo


or the same in a virtualenv::

    virtualenv sandbox
    source ./sandbox/bin/activate
    pip install anybox.paster.odoo

or manually download the archive below, uncompress, and::

    python setup.py install

Usage
~~~~~

This package depends on `PasteScript <http://pythonpaste.org/>`_, which will be
installed as a dependency and which offers a pluggable command
called ``paster``.  For more information on PasteScript, consult its
documentation.

You can list all the available templates with::

    paster create --list-templates

Creating an Odoo instance
-------------------------

This template will create an empty Odoo instance with an optional local
module for client customizations. The Odoo version can be pulled from
the bazaar branches of from the latest nightly build.

Run the `paster` command like this::

    paster create -t odoo_instance

Then answer the questions, and run the commands given at the end.

You can then modify the buildout configuration file as needed. For this part,
please consult the documentation of `anybox.recipe.odoo
<http://pypi.python.org/pypi/anybox.recipe.odoo>`_

Creating an Odoo module
-----------------------

Once you have a running instance, you can create new modules in the `addons` directory.
Run the `paster` command like this::

    paster create -t odoo_module

Authors and contributors
~~~~~~~~~~~~~~~~~~~~~~~~

- Jean-Sebastien Suzanne
- Christophe Combelles
- Georges Racinet

We are open to all contributions.
The source code and bug tracker are hosted on Bitbucket:

https://bitbucket.org/anybox/anybox.paster.odoo/

