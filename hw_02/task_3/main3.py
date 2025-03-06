from fastapi import FastAPI, Body
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
    if status != "None":
        parcels = list(filter(lambda parcel: parcel.status == status, parcels))
    if destination != "None":
        parcels = list(filter(lambda parcel: parcel.destination == destination, parcels))

    logger.info(f"GET/parcels: {len(parcels)}")
    return {"status": "ok", "parcels": parcels}


@app.post("/parcels")
def add_parcels(model: ParcelsModel = Body(embed=True)):

    parcels_db.add_parcel(model)

    logger.info(f"POST/add-parcels: {model.weight}")
    return {"status": "ok"}


@app.patch("/parcels/{id}")
def update_parcels_status(id: int, status: str = Body(embed=True)):
    parcels_db.update_status(id=id, status=status)

    logger.info(f"PATCH/update-status: {id} - {status}")
    return {"status": "ok"}


@app.delete("/parcels/{id}")
def delete_parcels(id: int):
    parcels_db.remove_parcel(id)

    logger.info(f"DELETE/parcels: {id}")
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="./static_3", html=True), name="static_3")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main3:app", reload=True)
