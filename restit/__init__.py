__version__ = "0.1.0"

import logging
import sys

DEFAULT_ENCODING = sys.getdefaultencoding()

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level=logging.WARNING)
