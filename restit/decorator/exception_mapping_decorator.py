import logging
from typing import Type, Dict, Tuple, Union

from restit.exception import HttpError

LOGGER = logging.getLogger(__name__)


def exception_mapping(mapping: Dict[Type[Exception], Union[Tuple[Type[HttpError], str], Type[HttpError]]]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                for source_exception_class, target_exception_tuple_or_class in mapping.items():
                    if isinstance(exception, source_exception_class):
                        if isinstance(target_exception_tuple_or_class, tuple):
                            LOGGER.debug(
                                "Mapping exception class %s to %s with description: %s",
                                type(exception), target_exception_tuple_or_class[0], target_exception_tuple_or_class[1]
                            )
                            raise target_exception_tuple_or_class[0](target_exception_tuple_or_class[1])
                        else:
                            LOGGER.debug(
                                "Mapping exception class %s to %s", type(exception), target_exception_tuple_or_class
                            )
                            raise target_exception_tuple_or_class(str(exception))

                raise exception

        return wrapper

    return decorator
