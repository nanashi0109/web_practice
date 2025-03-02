import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

from cat_model import CatsDB, CatModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

cats_dp = CatsDB()
logger = logging.getLogger("uvicorn.error")


@app.get("/cats")
def get_cats():
    cats = cats_dp.get_cats()
    logger.info("Cats received")
    return {"status": "ok", "cats": cats}


@app.post("/cats")
def post_cat(cat: CatModel):
    cats_dp.add_cat(cat)
    logger.info("Cat was added")
    return {"status": "ok"}


@app.patch("/cats/{cat_id}/like")
def like_cat(cat_id: int):
    try:
        cat_id = int(cat_id)
    except ValueError:
        return HTTPException(400, "Incorrect id")

    count_like = cats_dp.increase_like(cat_id, 1)
    logger.info(f"Like! {count_like}")
    return {"status": "ok", "count_like": count_like}


@app.delete("/cats/{cat_id}")
def delete_cat(cat_id: int):
    logger.info("Start deleting")
    try:
        cat_id = int(cat_id)
    except ValueError:
        return HTTPException(400, "Incorrect id")

    cats_dp.remove_cat(cat_id)
    logger.info("Cat was deleted")
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="./static", html=True), name="static")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
