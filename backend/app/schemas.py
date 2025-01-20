from pydantic import BaseModel


class Nutrition(BaseModel):
    name: str
    calories: int
    protein: int
    carbohydrates: int
    fat: int
