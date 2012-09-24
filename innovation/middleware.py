import logging
import traceback

from django.conf import settings

_logger = logging.getLogger(__name__)


class LogException(object):
    """Log request exceptions."""

    def process_exception(self, request, exception):
        _logger.warning(''.join(traceback.format_exc()))
