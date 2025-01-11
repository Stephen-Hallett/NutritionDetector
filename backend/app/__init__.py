import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controller import Controller

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
async def barcode_info(barcode: int) -> str:
    pass


@app.get("/test")
async def test() -> str:
    return "What up big dog"


# async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
#     return await func.AsgiMiddleware(app).handle_async(req, context)
