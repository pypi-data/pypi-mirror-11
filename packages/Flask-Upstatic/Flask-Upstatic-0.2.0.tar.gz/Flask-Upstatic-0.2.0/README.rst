==============
Flask-Upstatic
==============

Opinionated library for working with CDNs in Flask.


-------------
Configuration
-------------

================================= ===============================================
``UPSTATIC_S3_ACCESS_KEY_ID``     S3 Access Key ID
``UPSTATIC_S3_SECRET_ACCESS_KEY`` S3 Secret Access Key
``UPSTATIC_S3_BUCKET_NAME``       S3 Bucket Name
``UPSTATIC_S3_KEY_PREFIX``        S3 Key Prefix
``UPSTATIC_S3_CDN_HOST``          S3 CDN Host
``UPSTATIC_SCHEME``               URI Scheme (defaults to http)
``UPSTATIC_DEBUG_USE_LOCAL``      Whether to use local version when in debug mode
================================= ===============================================

-----
Usage
-----

Initialize extension::

  upstatic = Upstatic(app)
  # or
  upstatic = Upstatic()
  upstatic.init_app(app)

Upload the static files::

  # Will upload files in your ``app.static_folder``
  upstatic.upload()

Override ``url_for``::

  app.add_template_global(upstatic.url_for)

``url_for`` will then return CDN url::

  <img src="{{ url_for('static', filename='/images/image.png') }}">
