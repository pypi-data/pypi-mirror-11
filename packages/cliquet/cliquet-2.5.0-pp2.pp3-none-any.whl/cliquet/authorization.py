import re
import six
import functools
from pyramid.settings import aslist
from pyramid.security import IAuthorizationPolicy, Authenticated
from zope.interface import implementer

from cliquet import utils
from cliquet.storage import exceptions as storage_exceptions

# A permission is called "dynamic" when it's computed at request time.
DYNAMIC = 'dynamic'

# When permission is set to "private", only the current user is allowed.
PRIVATE = 'private'


@implementer(IAuthorizationPolicy)
class AuthorizationPolicy(object):
    # Callable that takes an object id and a permission and returns
    # a list of tuples (<object id>, <permission>).
    get_bound_permissions = None

    def permits(self, context, principals, permission):
        if permission == PRIVATE:
            return Authenticated in principals

        # Add prefixed user id to principals.
        if context.prefixed_userid:
            principals = principals + [context.prefixed_userid]
            prefix, user_id = context.prefixed_userid.split(':', 1)
            # Remove unprefixed user id to avoid conflicts.
            # (it is added via Pyramid Authn policy effective principals)
            if user_id in principals:
                principals.remove(user_id)
            # Retro-compatibility with cliquet 2.0 '_' user id prefixes.
            # Just in case it was used in permissions definitions.
            principals.append('%s_%s' % (prefix, user_id))

        if permission == DYNAMIC:
            permission = context.required_permission

        if permission == 'create':
            permission = '%s:%s' % (context.resource_name, permission)

        if context.allowed_principals:
            allowed = bool(set(context.allowed_principals) & set(principals))
        else:
            allowed = context.check_permission(
                permission,
                principals,
                get_bound_permissions=self.get_bound_permissions)

        return allowed

    def principals_allowed_by_permission(self, context, permission):
        raise NotImplementedError()  # PRAGMA NOCOVER


class RouteFactory(object):
    method_permissions = {
        "head": "read",
        "get": "read",
        "post": "create",
        "delete": "write",
        "patch": "write"
    }

    def __init__(self, request):
        # Make it available for the authorization policy.
        self.prefixed_userid = getattr(request, "prefixed_userid", None)

        # Store service, resource, record and required permission.
        service = utils.current_service(request)

        is_on_resource = (service is not None and
                          hasattr(service, 'viewset') and
                          hasattr(service, 'resource'))

        if not is_on_resource:
            object_id = None
            permission = None
            resource_name = None
            check_permission = None

        else:
            object_id = get_object_id(request.path)

            # Decide what the required unbound permission is depending on the
            # method that's being requested.
            if request.method.lower() == "put":
                # In the case of a "PUT", check if the targetted record already
                # exists, return "write" if it does, "create" otherwise.

                # If the view exists, call it with the request and catch an
                # eventual NotFound.
                resource = service.resource(request=request, context=self)
                try:
                    resource.collection.get_record(resource.record_id)
                except storage_exceptions.RecordNotFoundError:
                    object_id = service.collection_path.format(
                        **request.matchdict)
                    permission = "create"
                else:
                    permission = "write"
            else:
                method = request.method.lower()
                permission = self.method_permissions.get(method)

            resource_name = service.viewset.get_name(service.resource)
            check_permission = functools.partial(
                request.registry.permission.check_permission,
                object_id)

        settings = request.registry.settings
        settings_key = 'cliquet.%s_%s_principals' % (resource_name, permission)
        self.allowed_principals = aslist(settings.get(settings_key, ''))
        self.object_id = object_id
        self.required_permission = permission
        self.resource_name = resource_name
        self.check_permission = check_permission


def get_object_id(object_uri):
    # Remove potential version prefix in URI.
    return re.sub(r'^(/v\d+)?', '', six.text_type(object_uri))
