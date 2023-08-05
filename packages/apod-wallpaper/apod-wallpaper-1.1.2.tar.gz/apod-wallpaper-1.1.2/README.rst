apod-wallpaper
==============

Utilizes NASA APOD API to generate wallpapers with explanations. 
- Will download images (single, random or all in date range) 
- Only supports image media types (no video). 
- Uses tkinter to attempt to size wallpaper if not specified. 
- By default, adds explanation of daily images in watermarked footer.

Install
=======

::

    pip install apod-wallpaper


For issues installing PIL dependency:
- Install libjpeg-dev & freetype-dev with your package manager (apt, yum, brew, etc)
::
    
    pip install PIL --allow-external PIL --allow-unverified PIL

Configuration
-------------

Get your 
`NASA API key <https://api.nasa.gov/index.html#apply-for-an-api-key>`__

Set ``NASA_API_KEY`` environment variable to your key.

Usage
=====

Download single date
--------------------

.. code:: python

    from apod_wallpaper import apod
    from datetime import date

    apod.download_single(single_date=date(2015, 07, 01))

Download random
---------------

Defaults to ``start_date=date(1995, 6, 20)`` (the first day NASA began
posting daily pics), and ``end_date=date.today()``

.. code:: python

    from apod_wallpaper import apod

    apod.download_random()

Download bulk
-------------

Select range of APOD (good for catching up on recent misses)

.. code:: python

    from apod_wallpaper import apod
    from datetime import date

    apod.download_bulk(start_date=date(2015, 07, 01), end_date=date(2015, 07, 05))

All NASA APOD images (BE NICE: you probably don't need this)

.. code:: python

    from apod_wallpaper import apod

    apod.download_bulk()

Optional arguments
------------------

::

    download_path: (optional) File location to store downloaded image (default ~/wallpapers).
    overwrite: (optional) Overwrite existing files in download_path (default: False)
    screen_width: (optional) Pixels of width to make image. Large than original will add a black background. If not specified, OS detection of screen width will be attempted.
    screen_height: (optional) Pixels of height to make image. Large than original will add a black background. If not specified, OS detection of screen width will be attempted.
    font: (optional) TrueType font to apply in image footer (default OpenSans-Regular.ttf).
    font_size: (optional) Size of TrueType font in image footer (default 18).
    margin: (optional) Pixels around image footer text (default 50).
    font_color: (optional) RGBA tuple for color of font (default white).
    background_color: (optional) RBGA tuple for color of background (default black).
    opacity: (optional) Opacity for image footer (default 0.8).

Tests
=====

.. code:: python

    python test_apod.py

Acknowledgements
================

-  NASA APOD API via `Bowshock <https://github.com/emirozer/bowshock>`__
   wrapper library
-  Open Sans font from `Font Squirrel <http://www.fontsquirrel.com/>`__
-  Image processing by
   `Pillow <https://github.com/python-pillow/Pillow>`__

