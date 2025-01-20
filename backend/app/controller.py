import logging
import os

import requests

from . import schemas
from .util import log

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "x-app-id": os.environ.get("app_id"),
            "x-app-key": os.environ.get("app_key"),
        }

    @log
    def barcode(self, barcode: int) -> schemas.Nutrition:
        nutrients_raw = requests.get(
            "https://trackapi.nutritionix.com/v2/search/item/",
            params={"upc": barcode},
            headers=self.headers,
        )
        information = nutrients_raw.json()["foods"][0]
        return {
            "name": information["food_name"],
            "calories": round(information["nf_calories"]),
            "protein": round(information["nf_protein"]),
            "carbohydrates": round(information["nf_total_carbohydrate"]),
            "fat": round(information["nf_total_fat"]),
        }
