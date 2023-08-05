djmemcache
=====================

An efficient fast Django Memcached backend with a pool of connectors, based on
pymemcache.

See https://github.com/duanhongyi/djmemcache

Each connection added in the pool stays connected to Memcache or Membase,
drastically limiting the number of reconnections and open sockets your
application will use on high load.

If you configure more than one Memcache server, each new connection
will randomly pick one.

Everytime a socket timeout occurs on a server, it's blacklisted so
new connections avoid picking it for a while.

To use this backend, make sure the package is installed in your environment
then use `djmemcache.backend.PyMemcacheCache` as backend in your settings.


Here's an example::


    CACHES = {
        'default': {
            'BACKEND': 'djmemcache.backend.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
            'OPTIONS': {
                    'MAX_POOL_SIZE': 100,
                    'KEY_PREFIX': b'uuboard_prefix',
                    'TIMEOUT': 30,
                    'CONNECT_TIMEOUT': 30,
                    'USE_POOLING':True,
                }
            }
        }


Options:

- **MAX_POOL_SIZE:** -- The maximum number of connectors in the pool for eatch host. default: 2 ** 31.
- **KEY_PREFIX** -- The time in seconds a server stays in the blacklist. default: b''
- **TIMEOUT** -- The time in seconds for the socket timeout. defaults to "forever"
- **CONNECT_TIMEOUT** -- The time in seconds for the connect socket timeout. defaults to "forever"
- **USE_POOLING** -- Whether to apply the connection pool. defaults to "False"