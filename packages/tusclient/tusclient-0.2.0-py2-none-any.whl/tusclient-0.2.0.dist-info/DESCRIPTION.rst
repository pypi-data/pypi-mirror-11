=========
tusclient
=========


python client for tus protocol 1.0.0 of the `tus resumable upload standard`_.

.. _tus resumable upload standard: http://tus.io

install
-------

::

    pip install tusclient

arguments
---------

``fpath``
    ``str``, required, path of upload file

``upload_url``
    ``str``, required, url for the resumable upload service

``tmp_dir``
    ``str``, optional, directory to store temporary files, default ``/tmp/upload``

``upload_metadata``
    ``dict``, optional, Tus ``Upload-Metadata``, default ``None``


example
-------

::

    from tusclient import TusClient

    tus = TusClient(fpath='upload_file.dat', upload_url='http://localhost/upload_resumable')
    tus.run()


