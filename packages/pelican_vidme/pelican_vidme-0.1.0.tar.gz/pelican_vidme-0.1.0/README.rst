=============
Pelican Vidme
=============

Pelican Vidme is a plugin to enabled you to embed Vidme videos in your pages
and articles.

Installation
============

To install pelican-vidme, simply install it from PyPI:

.. code-block:: bash

    $ pip install pelican-vidme

Then enabled it in your pelicanconf.py

.. code-block:: python

    PLUGINS = [
        # ...
        'pelican_vidme',
        # ...
    ]

Usage
=====

In your article or page, you simply need to add a line to embed you video.

.. code-block:: rst

    .. vidme:: VIDEO_ID

Which will result in:

.. code-block:: html

    <div class="vidme" align="left">
    <iframe width="420" height="315" src="https://vid.me/VIDEO_ID" frameborder="0"></iframe>
    </div>

License
=======

`MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT
