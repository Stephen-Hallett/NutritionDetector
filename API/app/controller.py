import logging

from . import schemas
from .util import log

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @log
    def barcode(self, barcode: int) -> schemas.Nutrition:
        pass
