from django.test import TestCase

from helpcenter import utils


class TestStringToClass(TestCase):
    """Test cases for the string_to_class method."""

    def test_class_name(self):
        """Test passing in a string containing only a class name.

        If the string only has a class name in it, a ValueError should
        be raised.
        """
        with self.assertRaises(ValueError):
            utils.string_to_class('DummyClass')

    def test_invalid_class(self):
        """Test passing in an invalid class name.

        If the module given exists, but the class doesn't, an
        ImportError should be raised.
        """
        with self.assertRaises(ImportError):
            utils.string_to_class('helpcenter.tests.test_utils.DummyClass')

    def test_invalid_module(self):
        """Test passing an invalid module to the function.

        If the module doesn't actually exist, eg: 'fake.DummyClass', an
        ImportError should be raised.
        """
        with self.assertRaises(ImportError):
            utils.string_to_class('fake.DummyClass')

    def test_valid_string(self):
        """Test passing in a valid string.

        If a valid name is given to the function, the class it points to
        should be returned.
        """
        result = utils.string_to_class(
            'helpcenter.tests.test_utils.TestStringToClass')

        self.assertEqual(TestStringToClass, result)
