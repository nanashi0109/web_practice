import logging

from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

from currency_model import CurrencyModel, CurrencyDP

app = FastAPI()
currency_db = CurrencyDP()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")


@app.get("/exchange-rates")
def exchange_rates():
    currencies = currency_db.get_currencies()

    logger.info("GET. Currency")
    return {"status": "ok", "currencies": currencies}


@app.post("/convert")
def convert(currency: CurrencyModel):
    if not currency_db.add_currency(currency):
        return HTTPException(400, "Валюта уже существует")

    logger.info(f"POST. Add currency \n"
                f"      name: {currency.name}, \n"
                f"      rate: {currency.rate}")

    return {"status": "ok"}


@app.patch("/update-rate/{name}")
def update_rate(name: str, rate: float = Body(embed=True)):
    try:
        rate = float(rate)
    except ValueError:
        return HTTPException(400, "Неверный ввод курса")

    if not currency_db.update_rate(name, rate):
        return HTTPException(404, "Валюта не найдена")

    logger.info(f"PATCH. Update rate {name} to {rate}")
    return {"status": "ok"}


@app.delete("/rate/{currency}")
def delete_rate(currency: str):
    if not currency_db.remove_currency(currency):
        return HTTPException(404, "Валюта не найдена")

    logger.info(f"DELETE. Remove currency: {currency}")
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="./static2", html=True), name="static2")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
