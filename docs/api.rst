.. _api:

RestIt API Reference
====================

.. py:module:: restit

This part of the documentation covers all the interfaces of RestIt.


Restit Application
------------------

.. autoclass:: RestItApp
   :members:


Resource Related
----------------

.. autoclass:: restit.Resource

.. py:module:: restit.decorator

.. autofunction:: path

.. autofunction:: path_parameter

.. autoclass:: restit._path_parameter.PathParameter

.. autofunction:: query_parameter

.. autofunction:: request_body

OpenApi Documentation
---------------------

.. py:module:: restit.open_api

.. autoclass:: OpenApiDocumentation
   :members: generate_spec, register_resource

.. autoclass:: InfoObject

.. autoclass:: LicenseObject

.. autoclass::  ContactObject
