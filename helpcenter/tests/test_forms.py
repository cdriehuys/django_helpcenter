from django.test import TestCase

from helpcenter import forms, models
from helpcenter.testing_utils import create_category


class TestCategoryForm(TestCase):
    """ Test cases for the category form """

    def test_blank(self):
        """ Test the errors on a blank form.

        When a blank form is validated, it should create errors for
        required fields.
        """
        form = forms.CategoryForm({})

        expected = {
            'title': ['This field is required.'],
        }

        self.assertFalse(form.is_valid())
        self.assertEqual(expected, form.errors)

    def test_init(self):
        """ Test initializing a CategoryForm instance.

        No extra kwargs should be required to create a new instance.
        """
        form = forms.CategoryForm()

        self.assertFalse(form.is_bound)

    def test_save(self):
        """ Test saving valid data.

        Saving valid data should result in a new Category instance
        being created.
        """
        parent = create_category()
        data = {
            'title': 'Test Category',
            'parent': parent.pk,
        }

        form = forms.CategoryForm(data)

        self.assertTrue(form.is_valid())

        category = form.save()

        self.assertEqual(2, models.Category.objects.count())
        self.assertEqual(data['title'], category.title)
        self.assertEqual(parent, category.parent)
