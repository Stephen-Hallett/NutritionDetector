import json
import logging
import os

import requests
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

from . import schemas
from .util import log

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "x-app-id": os.environ.get("APP_ID"),
            "x-app-key": os.environ.get("APP_KEY"),
        }
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base", clean_up_tokenization_spaces=True
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.pretext = "a photograph of "

    @log
    def barcode(self, barcode: int) -> schemas.Nutrition:
        nutrients_raw = requests.get(  # NOQA
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

    @log
    def _describe_image(self, image: Image) -> str:
        inputs = self.processor(image, self.pretext, return_tensors="pt")
        out = self.model.generate(**inputs, max_new_tokens=100)
        return self.processor.decode(out[0], skip_special_tokens=True)

    @log
    def _nutritionix_nlq(self, context: str) -> schemas.Nutrition:
        nutrients_raw = requests.post(  # NOQA
            "https://trackapi.nutritionix.com/v2/natural/nutrients",
            data=json.dumps({"query": context}),
            headers=self.headers,
        )
        information = nutrients_raw.json()["foods"]
        nutrition = {
            "name": context.replace(self.pretext, ""),
            "calories": 0,
            "protein": 0,
            "carbohydrates": 0,
            "fat": 0,
        }
        for food in information:
            nutrition["calories"] += round(food["nf_calories"])
            nutrition["protein"] += round(food["nf_protein"])
            nutrition["carbohydrates"] += round(food["nf_total_carbohydrate"])
            nutrition["fat"] += round(food["nf_total_fat"])
        return nutrition

    @log
    def calories(self, item: Image.Image | str) -> schemas.Nutrition:
        if isinstance(item, str):
            return self._nutritionix_nlq(item)
        context = self._describe_image(item)
        return self._nutritionix_nlq(context)
