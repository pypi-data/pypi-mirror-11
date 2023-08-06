Support for using LMDB as a `shove<https://pypi.python.org/pypi/shove>`_ store.

*shove*'s URI for LMDB uses the form:

lmdb://<path>

Where <path> is a URL path to a LMDB database. Alternatively, the native
filesystem pathname to a LMDB database can be passed as the *engine* parameter.