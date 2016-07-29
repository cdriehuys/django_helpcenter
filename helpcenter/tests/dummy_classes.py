from django import forms


class BlankForm(forms.Form):
    """A blank form for testing purposes."""

    def __init__(self, *args, **kwargs):
        """Consume arguments."""
        super(BlankForm, self).__init__()
