import sqlite3
from pydantic import BaseModel


class CurrencyModel(BaseModel):
    name: str
    rate: float


class CurrencyDP:
    def __init__(self):
        self.__connection = sqlite3.connect("currency.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.__create_db()

    def __create_db(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS Currencies(
        name    TEXT PRIMARY KEY,
        rate    FLOAT NOT NULL    
        );
        """)

        self.__connection.commit()

    def add_currency(self, currency: CurrencyModel) -> bool:
        if self.exists_currency(currency.name):
            return False

        self.__cursor.execute("""
        INSERT INTO Currencies(name, rate) 
        VALUES(?, ?)""", (currency.name, currency.rate))

        self.__connection.commit()
        return True

    def remove_currency(self, currency_name: str) -> bool:
        if not self.exists_currency(currency_name):
            return False
        self.__cursor.execute("""
        DELETE FROM Currencies WHERE name=?
        """, (currency_name, ))

        self.__connection.commit()
        return True

    def get_currencies(self) -> list:
        self.__cursor.execute("""SELECT * FROM Currencies""")

        currency_tuple = self.__cursor.fetchall()
        currencies = []

        for (name, rate) in currency_tuple:
            currency = CurrencyModel(name=name, rate=rate)
            currencies.append(currency)

        return currencies if currencies != [] else []

    def exists_currency(self, currency_name: str) -> bool:
        currencies = self.get_currencies()
        currency_names = [currency.name.lower() for currency in currencies]

        if currency_name.lower() in currency_names:
            return True

        return False

    def update_rate(self, currency_name: str, rate: float) -> bool:
        if not self.exists_currency(currency_name):
            return False

        self.__cursor.execute("""
        UPDATE Currencies 
        SET rate = ? 
        WHERE name = ?;""", (rate, currency_name))

        self.__connection.commit()

        return True
