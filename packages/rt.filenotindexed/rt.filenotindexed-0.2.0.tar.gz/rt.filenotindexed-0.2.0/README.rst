Disable the Plone feature on indexing contents of File content types.

Use case
========

You are developing in a Plone environment with a production Data.fs (and blobs) that contains *a lot* of
File contents and then you need to perform some actions like "*Update catalog*" or "*Clean and Rebuild*".

It will be really slow, but probably the indexed files are not the reason why you are performing the action.

Or: you really don't want that Plone index contents fo your files.

How it works
============

This products is an hack that will monkey-patch the default Plone file content type (whatever it is) disabling the
feature that search inside file binary content.

This is automatically enabled in development mode while it's disabled in production mode.

On production mode you can force the indexing to stop working, adding the ``DISABLE_FILE_INDEXING``
environment var::

    [instance]
    ...
    
    environment-vars =
        DISABLE_FILE_INDEXING True

In the same way you can keep the indexing active while in development mode::

    [instance]
    ...
    
    environment-vars =
        DISABLE_FILE_INDEXING False

.. warning::
    Keep an eye open to this product if it will be pushed to a production environment and you are using it only for
    development purpose.
    
    While it will disabled in production mode, it will be enabled if you run a debug/emergency instance.

Compatibility
=============

* Plone 3 (with or without blob support)
* Plone 4 (with default file implementation or with plone.app.contenttypes)
* Plone 5

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
