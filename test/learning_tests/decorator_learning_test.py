import unittest


def my_decorator(some_argument: str):
    def decorator(func):
        setattr(func, "some_argument", some_argument)

        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            return some_argument + " " + return_value

        return wrapper

    return decorator


@my_decorator(some_argument="Hello")
def my_function(what: str):
    return what


class DecoratorLearningTestCase(unittest.TestCase):
    def test_mix_decorator_types_not_possible(self):
        self.assertIsNone(getattr(my_function, "some_argument", None))
        self.assertEqual("Hello cat", my_function("cat"))
