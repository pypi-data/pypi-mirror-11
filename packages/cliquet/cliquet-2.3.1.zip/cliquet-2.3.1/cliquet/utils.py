import ast
import hashlib
import hmac
import os
import six
import time
from base64 import b64decode, b64encode
from binascii import hexlify
from six.moves.urllib import parse as urlparse

# ujson is not installable with pypy
try:
    import ujson as json  # NOQA
except ImportError:  # pragma: no cover
    import json  # NOQA

# psycopg2cffi is installed under pypy, instead of psycopg2
try:
    import psycopg2  # NOQA
except ImportError:  # pragma: no cover
    try:
        from psycopg2cffi import compat
    except ImportError:
        psycopg2 = None
    else:
        compat.register()
        import psycopg2  # NOQA

from pyramid.request import Request
from cornice import cors
from colander import null


def strip_whitespace(v):
    """Remove whitespace, newlines, and tabs from the beginning/end
    of a string.
    """
    return v.strip(' \t\n\r') if v is not null else v


def msec_time():
    """Return current epoch time in milliseconds."""
    return int(time.time() * 1000.0)  # floor


def classname(obj):
    """Get a classname from a class."""
    return obj.__class__.__name__.lower()


def merge_dicts(a, b):
    """Merge b into a recursively, without overwriting values."""
    for k, v in b.items():
        if isinstance(v, dict):
            merge_dicts(a.setdefault(k, {}), v)
        else:
            a.setdefault(k, v)


def random_bytes_hex(bytes_length):
    """Return a hexstring of bytes_length cryptographic-friendly random bytes.
    """
    return hexlify(os.urandom(bytes_length)).decode('utf-8')


def native_value(value):
    """Convert string value to native python values."""
    if isinstance(value, six.string_types):
        if value.lower() in ['on', 'true', 'yes']:
            value = True
        elif value.lower() in ['off', 'false', 'no']:
            value = False
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass
    return value


def read_env(key, value):
    """Read the setting key from environment variables.

    :param key: the setting name
    :param value: default value if undefined in environment
    :returns: the value from environment, coerced to python type
    """
    envkey = key.replace('.', '_').replace('-', '_').upper()
    return native_value(os.getenv(envkey, value))


def encode64(content, encoding='utf-8'):
    """Encode some content in base64."""
    return b64encode(content.encode(encoding)).decode(encoding)


def decode64(encoded_content, encoding='utf-8'):
    """Decode some base64 encoded content."""
    return b64decode(encoded_content.encode(encoding)).decode(encoding)


def hmac_digest(secret, message, encoding='utf-8'):
    """Return hex digest of a message HMAC using secret"""
    return hmac.new(secret.encode(encoding),
                    message.encode(encoding),
                    hashlib.sha256).hexdigest()


def Enum(**enums):
    return type('Enum', (), enums)


COMPARISON = Enum(
    LT='<',
    MIN='>=',
    MAX='<=',
    NOT='!=',
    EQ='==',
    GT='>',
)


def reapply_cors(request, response):
    """Reapply cors headers to the new response with regards to the request.

    We need to re-apply the CORS checks done by Cornice, in case we're
    recreating the response from scratch.

    """
    service = current_service(request)
    if service:
        request.info['cors_checked'] = False
        response = cors.ensure_origin(service, request, response)
    return response


def current_service(request):
    """Return the Cornice service matching the specified request.

    :returns: the service or None if unmatched.
    :rtype: cornice.Service
    """
    if request.matched_route:
        services = request.registry.cornice_services
        pattern = request.matched_route.pattern
        try:
            service = services[pattern]
        except KeyError:
            return None
        else:
            return service


def build_request(original, dict_obj):
    """
    Transform a dict object into a ``pyramid.request.Request`` object.

    :param original: the original batch request.
    :param dict_obj: a dict object with the sub-request specifications.
    """
    api_prefix = '/%s' % original.upath_info.split('/')[1]
    path = dict_obj['path']
    if not path.startswith(api_prefix):
        path = api_prefix + path

    path = path.encode('utf-8')

    method = dict_obj.get('method') or 'GET'
    headers = dict(original.headers)
    headers.update(**dict_obj.get('headers') or {})
    payload = dict_obj.get('body') or ''

    # Payload is always a dict (from ``BatchRequestSchema.body``).
    # Send it as JSON for subrequests.
    if isinstance(payload, dict):
        headers['Content-Type'] = 'application/json; charset=utf-8'
        payload = json.dumps(payload)

    if six.PY3:  # pragma: no cover
        path = path.decode('latin-1')

    request = Request.blank(path=path,
                            headers=headers,
                            POST=payload,
                            method=method)

    return request


def build_response(response, request):
    """
    Transform a ``pyramid.response.Response`` object into a serializable dict.

    :param response: a response object, returned by Pyramid.
    :param request: the request that was used to get the response.
    """
    dict_obj = {}
    dict_obj['path'] = urlparse.unquote(request.path)
    dict_obj['status'] = response.status_code
    dict_obj['headers'] = dict(response.headers)

    body = ''
    if request.method != 'HEAD':
        # XXX : Pyramid should not have built response body for HEAD!
        try:
            body = response.json
        except ValueError:
            body = response.body
    dict_obj['body'] = body

    return dict_obj
