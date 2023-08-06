floatrange
==========

:author: Laurent Pointal <laurent.pointal@laposte.net>
:copyright: Laurent Pointal - 2011-2015
:license: MIT
:version: 0.2b

`Module documentation <http://floatrange.readthedocs.org/>`_

`Mercurial repository & bug tracking <http://sourceforge.net/projects/floatrange/>`_
(on SourceForge).

`Developer page <https://perso.limsi.fr/pointal/python:floatrange>`_

What is it?
-----------

A simple module providing a ``floatrange()`` to build generators
providing a range like interface for floating point numbers.
As floating point computation may not be exact, these generators
support a precision ``prec`` parameter to define how near a value
correspond to a value in the range.

..  note::
    Version is set to 0.Xb but module is normally usable.
    I wait for some positive feedback (or at least not negative until
    few wekks) to go to version 1.0 production stable.

Installation
------------

Unless someone built a package for your OS distro, the simplest procedure
is to use ``pip`` to install the module:

    pip install floatrange

If you have no admin access to install things on you computer, you may install
a virtualenv and run pip inside this virtual env, or you can do a local user
installation:

    pip install --user floatrange

