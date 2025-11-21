from desktop_app.db.database import Database
from typing import Set

from desktop_app.model.Card import Card


class CardDAO:
    def __init__(self):
        self.__db = Database()

    def get_all(self) -> Set[Card]:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cards')
        rows = cursor.fetchall()

        return set([Card(row[0], row[1], row[2], row[3]) for row in rows])

    def get_by_id(self, card_id: str) -> Card | None:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
        row = cursor.fetchone()

        if row:
            return Card(row[0], row[1], row[3], row[4])
        return None


if __name__ == '__main__':
    cardDao = CardDAO()
    print(cardDao.get_all())
