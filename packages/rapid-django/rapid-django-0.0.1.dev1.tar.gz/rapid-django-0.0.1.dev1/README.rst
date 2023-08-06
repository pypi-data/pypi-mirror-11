Rapid Django
============

A set of opionated tools for rapid development of enterprise CRUD portals.

Rapid Django generates CRUD pages and menus, based on a simple to use
registry of models, forms and views.

How to Use
==========

Add the 'rapid' application to your installed apps, and run a database migration.
Create a 'base.html' template that will be used by the CRUD generator. A minimum
template looks as following:

::
   <DOCTYPE html>
   <html>
   <head>
       <link href="link to bootstrap" rel="stylesheet">
       <script src="link to jquery"></script>
   </head>
   <body>
       {% load rapid_crud %}{% load rapid_filters %}
       {% register_filters %}
       {% register_overlay %}
       {% load rapid_menu %}
       {% menu request %}
       {% block body %}{% endblock %}
       <script src="link to the jquery-form plugin">
   </body>
   </html>

A menu will be generated in a unumbered list (UL) at the "menu" tag, and the
registered data will be placed at the "body" block.

After that, one must register actions. For that, the module "rapid" has three helper functions:
"register_model", "register_instance_form", and "register_simple_select".

Use "register_model" for creating default actions for listing, viewing, editing, addin, and optionally
removing objects of a model.

Use "register_instance_form" for creating custom actions where users submit a form, and act upon
instances of a model. The form may not be a ModelForm, but must implement the save() method.

Use "register_simple_select" for enabling the rapid select widget for all generated edit forms
with fields that select the registered model (that is, foreign key, one to one, and one to many
fields, besides reverse relationships).

The module "rapid.permissions" includes helper functions for managing user permissions on the
registered actions. Permmissions may be managed for entire models and for instances (but not
columns yet).

