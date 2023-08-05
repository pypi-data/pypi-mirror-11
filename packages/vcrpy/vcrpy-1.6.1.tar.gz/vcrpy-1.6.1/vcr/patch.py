'''Utilities for patching in cassettes'''
import functools
import itertools

from .compat import contextlib, mock
from .stubs import VCRHTTPConnection, VCRHTTPSConnection
from six.moves import http_client as httplib


# Save some of the original types for the purposes of unpatching
_HTTPConnection = httplib.HTTPConnection
_HTTPSConnection = httplib.HTTPSConnection


# Try to save the original types for requests
try:
    import requests.packages.urllib3.connectionpool as cpool
except ImportError:  # pragma: no cover
    pass
else:
    _VerifiedHTTPSConnection = cpool.VerifiedHTTPSConnection
    _cpoolHTTPConnection = cpool.HTTPConnection
    _cpoolHTTPSConnection = cpool.HTTPSConnection


# Try to save the original types for urllib3
try:
    import urllib3
except ImportError:  # pragma: no cover
    pass
else:
    _VerifiedHTTPSConnection = urllib3.connectionpool.VerifiedHTTPSConnection


# Try to save the original types for httplib2
try:
    import httplib2
except ImportError:  # pragma: no cover
    pass
else:
    _HTTPConnectionWithTimeout = httplib2.HTTPConnectionWithTimeout
    _HTTPSConnectionWithTimeout = httplib2.HTTPSConnectionWithTimeout
    _SCHEME_TO_CONNECTION = httplib2.SCHEME_TO_CONNECTION


# Try to save the original types for boto
try:
    import boto.https_connection
except ImportError:  # pragma: no cover
    pass
else:
    _CertValidatingHTTPSConnection = boto.https_connection.CertValidatingHTTPSConnection


# Try to save the original types for Tornado
try:
    import tornado.httpclient
    import tornado.simple_httpclient
except ImportError:  # pragma: no cover
    pass
else:
    _AsyncHTTPClient = tornado.httpclient.AsyncHTTPClient
    _SimpleAsyncHTTPClient = tornado.simple_httpclient.SimpleAsyncHTTPClient


try:
    import tornado.curl_httpclient
except ImportError:  # pragma: no cover
    pass
else:
    _CurlAsyncHTTPClient = tornado.curl_httpclient.CurlAsyncHTTPClient


class CassettePatcherBuilder(object):

    def _build_patchers_from_mock_triples_decorator(function):
        @functools.wraps(function)
        def wrapped(self, *args, **kwargs):
            return self._build_patchers_from_mock_triples(
                function(self, *args, **kwargs)
            )
        return wrapped

    def __init__(self, cassette):
        self._cassette = cassette
        self._class_to_cassette_subclass = {}

    def build(self):
        return itertools.chain(
            self._httplib(), self._requests(), self._urllib3(),
            self._httplib2(), self._boto(), self._tornado(),
            self._build_patchers_from_mock_triples(
                self._cassette.custom_patches
            ),
        )

    def _build_patchers_from_mock_triples(self, mock_triples):
        for args in mock_triples:
            patcher = self._build_patcher(*args)
            if patcher:
                yield patcher

    def _build_patcher(self, obj, patched_attribute, replacement_class):
        if not hasattr(obj, patched_attribute):
            return

        return mock.patch.object(obj, patched_attribute,
                                 self._recursively_apply_get_cassette_subclass(
                                     replacement_class))

    def _recursively_apply_get_cassette_subclass(self, replacement_dict_or_obj):
        """One of the subtleties of this class is that it does not directly
        replace HTTPSConnection with `VCRRequestsHTTPSConnection`, but a
        subclass of the aforementioned class that has the `cassette`
        class attribute assigned to `self._cassette`. This behavior is
        necessary to properly support nested cassette contexts.

        This function exists to ensure that we use the same class
        object (reference) to patch everything that replaces
        VCRRequestHTTP[S]Connection, but that we can talk about
        patching them with the raw references instead, and without
        worrying about exactly where the subclass with the relevant
        value for `cassette` is first created.

        The function is recursive because it looks in to dictionaries
        and replaces class values at any depth with the subclass
        described in the previous paragraph.
        """
        if isinstance(replacement_dict_or_obj, dict):
            for key, replacement_obj  in replacement_dict_or_obj.items():
                replacement_obj = self._recursively_apply_get_cassette_subclass(
                    replacement_obj)
                replacement_dict_or_obj[key] = replacement_obj
            return replacement_dict_or_obj
        if hasattr(replacement_dict_or_obj, 'cassette'):
            replacement_dict_or_obj =  self._get_cassette_subclass(
                replacement_dict_or_obj)
        return replacement_dict_or_obj

    def _get_cassette_subclass(self, klass):
        if klass.cassette is not None:
            return klass
        if klass not in self._class_to_cassette_subclass:
            subclass = self._build_cassette_subclass(klass)
            self._class_to_cassette_subclass[klass] = subclass
        return self._class_to_cassette_subclass[klass]

    def _build_cassette_subclass(self, base_class):
        bases = (base_class,)
        if not issubclass(base_class, object): # Check for old style class
            bases += (object,)
        return type('{0}{1}'.format(base_class.__name__, self._cassette._path),
                    bases, dict(cassette=self._cassette))

    @_build_patchers_from_mock_triples_decorator
    def _httplib(self):
        yield httplib, 'HTTPConnection', VCRHTTPConnection
        yield httplib, 'HTTPSConnection', VCRHTTPSConnection

    def _requests(self):
        try:
            import requests.packages.urllib3.connectionpool as cpool
        except ImportError:  # pragma: no cover
            return ()
        from .stubs import requests_stubs
        return self._urllib3_patchers(cpool, requests_stubs)

    def _patched_get_conn(self, connection_pool_class, connection_class_getter):
        get_conn = connection_pool_class._get_conn
        @functools.wraps(get_conn)
        def patched_get_conn(pool, timeout=None):
            connection = get_conn(pool, timeout)
            connection_class = pool.ConnectionCls if hasattr(pool, 'ConnectionCls') \
                               else connection_class_getter()
            # We need to make sure that we are actually providing a
            # patched version of the connection class. This might not
            # always be the case because the pool keeps previously
            # used connections (which might actually be of a different
            # class) around. This while loop will terminate because
            # eventually the pool will run out of connections.
            while not isinstance(connection, connection_class):
                connection = get_conn(pool, timeout)
            return connection
        return patched_get_conn

    def _patched_new_conn(self, connection_pool_class, connection_remover):
        new_conn = connection_pool_class._new_conn
        @functools.wraps(new_conn)
        def patched_new_conn(pool):
            new_connection = new_conn(pool)
            connection_remover.add_connection_to_pool_entry(pool, new_connection)
            return new_connection
        return patched_new_conn

    def _urllib3(self):
        try:
            import urllib3.connectionpool as cpool
        except ImportError:  # pragma: no cover
            return ()
        from .stubs import urllib3_stubs
        return self._urllib3_patchers(cpool, urllib3_stubs)

    @_build_patchers_from_mock_triples_decorator
    def _httplib2(self):
        try:
            import httplib2 as cpool
        except ImportError:  # pragma: no cover
            pass
        else:
            from .stubs.httplib2_stubs import VCRHTTPConnectionWithTimeout
            from .stubs.httplib2_stubs import VCRHTTPSConnectionWithTimeout

            yield cpool, 'HTTPConnectionWithTimeout', VCRHTTPConnectionWithTimeout
            yield cpool, 'HTTPSConnectionWithTimeout', VCRHTTPSConnectionWithTimeout
            yield cpool, 'SCHEME_TO_CONNECTION', {'http': VCRHTTPConnectionWithTimeout,
                                                  'https': VCRHTTPSConnectionWithTimeout}

    @_build_patchers_from_mock_triples_decorator
    def _boto(self):
        try:
            import boto.https_connection as cpool
        except ImportError:  # pragma: no cover
            pass
        else:
            from .stubs.boto_stubs import VCRCertValidatingHTTPSConnection
            yield cpool, 'CertValidatingHTTPSConnection', VCRCertValidatingHTTPSConnection

    @_build_patchers_from_mock_triples_decorator
    def _tornado(self):
        try:
            import tornado.httpclient as http
            import tornado.simple_httpclient as simple
        except ImportError:  # pragma: no cover
            pass
        else:
            from .stubs.tornado_stubs import VCRAsyncHTTPClient
            from .stubs.tornado_stubs import VCRSimpleAsyncHTTPClient

            yield http, 'AsyncHTTPClient', VCRAsyncHTTPClient
            yield simple, 'SimpleAsyncHTTPClient', VCRSimpleAsyncHTTPClient
        try:
            import tornado.curl_httpclient as curl
        except ImportError:  # pragma: no cover
            pass
        else:
            from .stubs.tornado_stubs import VCRCurlAsyncHTTPClient
            yield curl, 'CurlAsyncHTTPClient', VCRCurlAsyncHTTPClient

    def _urllib3_patchers(self, cpool, stubs):
        http_connection_remover = ConnectionRemover(
            self._get_cassette_subclass(stubs.VCRRequestsHTTPConnection)
        )
        https_connection_remover = ConnectionRemover(
            self._get_cassette_subclass(stubs.VCRRequestsHTTPSConnection)
        )
        mock_triples = (
            (cpool, 'VerifiedHTTPSConnection', stubs.VCRRequestsHTTPSConnection),
            (cpool, 'VerifiedHTTPSConnection', stubs.VCRRequestsHTTPSConnection),
            (cpool, 'HTTPConnection', stubs.VCRRequestsHTTPConnection),
            (cpool, 'HTTPSConnection', stubs.VCRRequestsHTTPSConnection),
            (cpool, 'is_connection_dropped', mock.Mock(return_value=False)),  # Needed on Windows only
            (cpool.HTTPConnectionPool, 'ConnectionCls', stubs.VCRRequestsHTTPConnection),
            (cpool.HTTPSConnectionPool, 'ConnectionCls', stubs.VCRRequestsHTTPSConnection),
        )
        # These handle making sure that sessions only use the
        # connections of the appropriate type.
        mock_triples += ((cpool.HTTPConnectionPool, '_get_conn',
                          self._patched_get_conn(cpool.HTTPConnectionPool,
                                                 lambda : cpool.HTTPConnection)),
                         (cpool.HTTPSConnectionPool, '_get_conn',
                          self._patched_get_conn(cpool.HTTPSConnectionPool,
                                                 lambda : cpool.HTTPSConnection)),
                         (cpool.HTTPConnectionPool, '_new_conn',
                          self._patched_new_conn(cpool.HTTPConnectionPool,
                                                 http_connection_remover)),
                         (cpool.HTTPSConnectionPool, '_new_conn',
                          self._patched_new_conn(cpool.HTTPSConnectionPool,
                                                 https_connection_remover)))

        return itertools.chain(self._build_patchers_from_mock_triples(mock_triples),
                               (http_connection_remover, https_connection_remover))


class ConnectionRemover(object):

    def __init__(self, connection_class):
        self._connection_class = connection_class
        self._connection_pool_to_connections = {}

    def add_connection_to_pool_entry(self, pool, connection):
        if isinstance(connection, self._connection_class):
            self._connection_pool_to_connections.setdefault(pool, set()).add(connection)

    def remove_connection_to_pool_entry(self, pool, connection):
        if isinstance(connection, self._connection_class):
            self._connection_pool_to_connections[self._connection_class].remove(connection)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for pool, connections in self._connection_pool_to_connections.items():
            readd_connections = []
            while pool.pool and not pool.pool.empty() and connections:
                connection = pool.pool.get()
                if isinstance(connection, self._connection_class):
                    connections.remove(connection)
                else:
                    readd_connections.append(connection)
            for connection in readd_connections:
                pool._put_conn(connection)


def reset_patchers():
    yield mock.patch.object(httplib, 'HTTPConnection', _HTTPConnection)
    yield mock.patch.object(httplib, 'HTTPSConnection', _HTTPSConnection)
    try:
        import requests.packages.urllib3.connectionpool as cpool
    except ImportError:  # pragma: no cover
        pass
    else:
        # unpatch requests v1.x
        yield mock.patch.object(cpool, 'VerifiedHTTPSConnection', _VerifiedHTTPSConnection)
        yield mock.patch.object(cpool, 'HTTPConnection', _cpoolHTTPConnection)
        # unpatch requests v2.x
        if hasattr(cpool.HTTPConnectionPool, 'ConnectionCls'):
            yield mock.patch.object(cpool.HTTPConnectionPool, 'ConnectionCls',
                                    _cpoolHTTPConnection)
            yield mock.patch.object(cpool.HTTPSConnectionPool, 'ConnectionCls',
                                    _cpoolHTTPSConnection)

        if hasattr(cpool, 'HTTPSConnection'):
            yield mock.patch.object(cpool, 'HTTPSConnection', _cpoolHTTPSConnection)

    try:
        import urllib3.connectionpool as cpool
    except ImportError:  # pragma: no cover
        pass
    else:
        yield mock.patch.object(cpool, 'VerifiedHTTPSConnection', _VerifiedHTTPSConnection)
        yield mock.patch.object(cpool, 'HTTPConnection', _HTTPConnection)
        yield mock.patch.object(cpool, 'HTTPSConnection', _HTTPSConnection)
        if hasattr(cpool.HTTPConnectionPool, 'ConnectionCls'):
            yield mock.patch.object(cpool.HTTPConnectionPool, 'ConnectionCls', _HTTPConnection)
            yield mock.patch.object(cpool.HTTPSConnectionPool, 'ConnectionCls', _HTTPSConnection)

    try:
        import httplib2 as cpool
    except ImportError:  # pragma: no cover
        pass
    else:
        yield mock.patch.object(cpool, 'HTTPConnectionWithTimeout', _HTTPConnectionWithTimeout)
        yield mock.patch.object(cpool, 'HTTPSConnectionWithTimeout', _HTTPSConnectionWithTimeout)
        yield mock.patch.object(cpool, 'SCHEME_TO_CONNECTION', _SCHEME_TO_CONNECTION)

    try:
        import boto.https_connection as cpool
    except ImportError:  # pragma: no cover
        pass
    else:
        yield mock.patch.object(cpool, 'CertValidatingHTTPSConnection',
                                _CertValidatingHTTPSConnection)

    try:
        import tornado.httpclient as http
        import tornado.simple_httpclient as simple
    except ImportError:  # pragma: no cover
        pass
    else:
        yield mock.patch.object(http, 'AsyncHTTPClient', _AsyncHTTPClient)
        yield mock.patch.object(simple, 'SimpleAsyncHTTPClient', _SimpleAsyncHTTPClient)
    try:
        import tornado.curl_httpclient as curl
    except ImportError:  # pragma: no cover
        pass
    else:
        yield mock.patch.object(curl, 'CurlAsyncHTTPClient', _CurlAsyncHTTPClient)


@contextlib.contextmanager
def force_reset():
    with contextlib.ExitStack() as exit_stack:
        for patcher in reset_patchers():
            exit_stack.enter_context(patcher)
        yield
