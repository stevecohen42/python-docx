
.. _shape_api:

Shape-related objects
=====================

.. currentmodule:: docx.parts.document


|InlineShapes| objects
----------------------

.. autoclass:: InlineShapes
   :members:


.. currentmodule:: docx.shape


|InlineShape| objects
---------------------

The ``width`` and ``height`` property of |InlineShape| provide a length object
that is an instance of |Length|. These instances behave like an int, but also
have built-in units conversion properties, e.g.::

    >>> inline_shape.height
    914400
    >>> inline_shape.height.inches
    1.0

.. autoclass:: InlineShape
   :members: height, type, width
