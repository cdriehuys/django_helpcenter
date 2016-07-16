from django.core.exceptions import PermissionDenied


class PermissionsMixin(object):
    """ Mixin that requires the user to have certain permissions """

    def has_permission(self, request):
        """ Determine if the user has permission to access the view """
        return request.user.has_perms(getattr(self, 'permissions', []))

    def dispatch(self, request, *args, **kwargs):
        """ Check permissions and then call super's dispatch """
        if not self.has_permission(request):
            raise PermissionDenied()

        return super(PermissionsMixin, self).dispatch(request, *args, **kwargs)
