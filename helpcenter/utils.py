"""A collection of utility functions."""

import importlib
import logging


def string_to_class(class_string):
    """Convert a string to a python class.

    The string is first split into a module and a class name. For
    example, 'dummy.package.FakeClass' would be split into
    'dummy.package' and 'FakeClass'. The package/module are then
    imported, and the class is returned.

    Args:
        class_string (str):
            The full string name of the class to import. This should
            include the package and module if applicable.

    Returns:
        Class:
            If the path exists, the python class in the location given
            by `class_string` is returned.

    Raises:
        ImportError: If the path `class_string` doesn't exist.
        ValueError: If `class_string` is not a fully qualified name.
            eg: `DummyClass` instead of `module.DummyClass`.
    """
    logger = logging.getLogger(__name__)

    if '.' not in class_string:
        logger.error(
            "'{}' is not a fully qualifed class name".format(class_string))

        raise ValueError("'class_string' must be a fully qualifed name.")

    module_name, class_name = class_string.rsplit('.', 1)

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        logger.error(
            "Could not import '{}'".format(module_name), exc_info=True)

        raise

    try:
        class_obj = getattr(module, class_name)
    except AttributeError:
        error_msg = "Could not import '{}' from '{}'.".format(
            class_name, module_name)

        logger.error(error_msg, exc_info=True)

        raise ImportError(error_msg)

    logger.debug("Succesfully imported '{}' from '{}'.".format(
        class_name, module_name))

    return class_obj
