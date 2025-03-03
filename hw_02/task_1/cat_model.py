from pydantic import BaseModel
import sqlite3


class CatModel(BaseModel):
    id: int | None = None
    name: str
    age: int
    count_likes: int = 0

    # @property
    # def id(self):
    #     return self.__id
    #
    # @property
    # def name(self):
    #     return self.__name
    #
    # @property
    # def age(self):
    #     return self.__age
    #
    # @property
    # def count_likes(self):
    #     return self.__count_likes
    #
    # @id.setter
    # def id(self, value):
    #     self.__id = value
    #
    # def __str__(self):
    #     result = (f"id: {self.__id}\n"
    #               f"name: {self.__name}\n"
    #               f"age: {self.__age}\n"
    #               f"count_likes: {self.__count_likes}")
    #
    #     return result


class CatsDB:
    def __init__(self):
        self.__connection = sqlite3.connect("cats.dp", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.__create_dp()

    def __create_dp(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cats (
        id              INTEGER PRIMARY KEY,
        name            TEXT NOT NULL,
        age             INTEGER NOT NULL,
        count_likes     INTEGER NOT NULL
        );
        """)

    def add_cat(self, cat: CatModel):
        if cat.id is None:
            cat_id = self.__get_last_id()
            cat.id = cat_id

        self.__cursor.execute("""
        INSERT INTO Cats(id, name, age, count_likes) 
        VALUES (?, ?, ?, ?)""", (cat.id, cat.name, cat.age, cat.count_likes))

        self.__connection.commit()

    def remove_cat(self, cat_id):
        self.__cursor.execute("""DELETE FROM Cats WHERE id=?""",
                              (cat_id, ))

        self.__connection.commit()

    def get_cats(self):
        self.__cursor.execute("""SELECT * FROM Cats""")

        cats = []
        cats_tuples = self.__cursor.fetchall()
        for (id, name, age, count_likes) in cats_tuples:
            cat = CatModel(id=id, name=name, age=age, count_likes=count_likes)
            cats.append(cat)

        return cats

    def increase_like(self, cat_id, count_likes):
        self.__cursor.execute("""UPDATE Cats SET count_likes = count_likes + ? WHERE id = ?""",
                              (count_likes, cat_id))

        self.__connection.commit()

        self.__cursor.execute("""SELECT count_likes FROM Cats WHERE id=?""",
                              (cat_id, ))
        
        return self.__cursor.fetchone()[0]

    def __get_last_id(self) -> int:
        cats = self.get_cats()
        if cats == []:
            return 0

        max_id = max(i.id for i in cats)
        return max_id+1
