from io import BytesIO, StringIO

import azure.functions as func
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from .config import settings
from .controller import Controller
from .schemas import Nutrition

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


con = Controller()


@app.post("/barcode")
async def barcode_info(upc: int) -> Nutrition:
    return con.barcode(upc)


@app.post("/describe")
async def describe(file: UploadFile = File(...)) -> str:
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        image = image.convert("RGB")

        return con._describe_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e!s}")


@app.post("/image/calories")
async def calories(file: UploadFile = File(...)) -> Nutrition:
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        image = image.convert("RGB")

        return con.calories(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e!s}")


@app.post("/text/calories")
async def calories(context: str = Form(...)) -> Nutrition:
    return con.calories(context)


@app.get("/test")
async def test() -> str:
    return "What up big dog"


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return await func.AsgiMiddleware(app).handle_async(req, context)
