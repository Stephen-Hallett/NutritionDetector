from pydantic import BaseModel


class Nutrition(BaseModel):
    calories: int
    protein: int
    carbohydrates: int
    fat: int
