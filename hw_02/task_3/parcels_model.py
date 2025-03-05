import sqlite3

from pydantic import BaseModel


class ParcelsModel(BaseModel):
    id: int | None = None
    name: str
    weight: float
    senders_address: str
    destination: str
    status: str = "in-transit"


class ParcelsDB:
    def __init__(self):
        self.__connection = sqlite3.Connection("parcels_.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.create_db()
    
    def create_db(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcel (
        id                  INT PRIMARY KEY,
        name                TEXT NOT NULL,
        status              TEXT NOT NULL,
        destination         TEXT NOT NULL,
        senders_address     TEXT NOT NULL,
        weight              FLOAT NOT NULL
        )
        """)
    
    def get_parcels(self):
        self.__cursor.execute("""SELECT * FROM parcel""")

        parcels_tuple = self.__cursor.fetchall()
        parcels = []

        for (id, name, status, destination, senders_address, weight) in parcels_tuple:
            parcel = ParcelsModel(id=id, name=name, status=status, destination=destination, senders_address=senders_address, weight=weight)
            parcels.append(parcel)

        return parcels

    def add_parcel(self, model: ParcelsModel):
        if model.id == None:
            model.id = self.__get_last_id()

        self.__cursor.execute("""
        INSERT INTO parcel(id, name, status, destination, senders_address, weight)
        VALUES(?, ?, ?, ?, ?, ?)
        """, (model.id, model.name, model.status, model.destination, model.senders_address, model.weight))

        self.__connection.commit()

    def remove_parcel(self, id: int):
        self.__cursor.execute("""
        DELETE FROM parcel WHERE id = ?
        """, (id, ))

        self.__connection.commit()

    def update_status(self, id: int, status: str):
        self.__cursor.execute("""
        UPDATE parcel SET status = ? WHERE id = ?
        """, (status, id))

        self.__connection.commit()

    def __get_last_id(self):
        parcels = self.get_parcels()

        return min(i.id for i in parcels) + 1
    