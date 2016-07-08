from django import forms

from helpcenter import models


class CategoryForm(forms.ModelForm):
    """ Form for the Category model """

    class Meta:
        fields = ('title', 'parent')
        model = models.Category
