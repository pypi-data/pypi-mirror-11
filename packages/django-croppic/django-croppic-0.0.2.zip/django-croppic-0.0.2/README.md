django-croppic
==============

[Croppic](http://croppic.net/) is a jquery plugin which handles uploading and manipulating images via AJAX.

A Django package which uses [Croppic](http://croppic.net/) to upload and crop images.

Installation
============

Install from pypi:

    pip install django-croppic

To use `django-croppic` in your Django project:

1. Add `croppic` to your `INSTALLED_APPS` setting.
2. Add `croppic.urls` in your main `urls`
    * `url(r'^croppic/', include('croppic.urls', namespace='croppic')),`
3. Run `syncdb` command to initialise the `croppic` database table
4. Run `collectstatic` command to collect the static files of croppic into `STATIC_ROOT` (If on production)

Configuration
=============

Available settings:

* `CROPPIC_UPLOAD_PATH`
  * Default: `pictures`
  * The default path where to store uploaded files.
    * e.g. `CROPPIC_UPLOAD_PATH = 'user_photos'` (Notice no leading or trailing slashes).

* `CROPPIC_MIN_SIZE`
  * Default: `None` (No restrictions)
  * Restrict uploaded/cropped files to have at least minimum width and height as defined by `CROPPIC_MIN_SIZE`.
    * e.g. `CROPPIC_MIN_SIZE = (250, 250)`

* `CROPPIC_MIN_SIZE_ERROR`
  * Default: `Image is too small, must be at least {0}x{1} wide.` (The `{0}` and `{1}` will be used in string formatting to replace with width and height)
  * If `CROPPIC_MIN_SIZE` is specified you may want to update this to show a different error message if uploaded/cropped image does not satisfy `CROPPIC_MIN_SIZE`
