from django.conf import settings
from django.core.exceptions import PermissionDenied

from helpcenter import utils


class OptionalFormMixin(object):
    """Mixin allowing an optional form to be provided.

    The mixin first attempts to retrieve the form given in the provided
    settings value and then falls back to the original method.

    Attributes:
        form_class_setting (str):
            The name of the setting that the form class is in.
    """
    form_class_setting = None

    def get_form_class(self):
        """Get the form class for the view.

        First try to use the form from `get_form_class_setting`, then
        fall back to the parent class' implementation.

        Returns:
            A form class that is either the one specified in
            `get_form_class_setting` or one that is generated from the
            `model` and `fields` attributes of the class.
        """
        setting_name = self.get_form_class_setting()

        if setting_name is not None:
            form_class = getattr(settings, setting_name, None)

        if form_class is not None:
            try:
                return utils.string_to_class(form_class)
            except ImportError:
                pass

        return super(OptionalFormMixin, self).get_form_class()

    def get_form_class_setting(self):
        """ Get the name of the setting containing the form class.

        Returns:
            str:
                The instance's `form_class_setting` attribute.
        """
        return self.form_class_setting


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
