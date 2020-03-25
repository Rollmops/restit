import logging
from typing import Type, Dict, Tuple, Union

from restit.exception import HttpError

LOGGER = logging.getLogger(__name__)


def exception_mapping(mapping: Dict[Type[Exception], Union[Tuple[Type[HttpError], str], Type[HttpError]]]):
    def decorator(func_or_class):
        LOGGER.debug("Registering exception mapping %s for %s", mapping, func_or_class)
        setattr(func_or_class, "__exception_mapping__", mapping)
        return func_or_class

    return decorator
