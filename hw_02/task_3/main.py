from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
import logging

from parcels_model import ParcelsDB, ParcelsModel


logger = logging.getLogger("uvicorn.error")
app = FastAPI()
parcels_db = ParcelsDB()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/parcels")
def get_parcels(status: str, destination: str):
    parcels = parcels_db.get_parcels()
    if status is not None:
        parcels = list(filter(lambda parcel: parcel.status == status, parcels))
    if destination is not None:
        parcels = list(filter(lambda parcel: parcel.destination == destination, parcels))

    logger.info(f"GET/parcels: {parcels}")
    return {"status": "ok", "parcels": parcels}


@app.post("/parcels")
def add_parcels(model: ParcelsModel):
    parcels_db.add_parcel(model)

    logger.info(f"POST/add-parcels: {model.name}")
    return {"status": "ok"}


@app.patch("/parcels/{id}")
def update_parcels_status(id: int, status: str):
    parcels_db.update_status(id=id, status=status)

    logger.info(f"PATCH/update-status: {id} - {status}")
    return {"status": "ok"}


@app.delete("/parcels/{id}")
def delete_parcels(id: int):
    parcels_db.remove_parcel(id)

    logger.info(f"DELETE/parcels: {id}")
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="./static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
