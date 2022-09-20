import sys
import sqlite3

class Database:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(database=db_name)
            self.cur = self.conn.cursor()

            # CREATE TABLES
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Item ( 
                             ItemID integer PRIMARY KEY AUTOINCREMENT,
                             ItemDamage integer NOT NULL,
                             ItemOffset integer NOT NULL);""")

            self.conn.commit()

        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

    def add_item(self, item_dmg: int, item_offset: int):
        self.cur.execute("""INSERT INTO Item(ItemDamage, ItemOffset)
                            VALUES(?, ?)""", (item_dmg, item_offset))
        self.conn.commit()

    def get_item(self, item_id: int) -> tuple:
        item = self.cur.execute("""SELECT ItemDamage, ItemOffset FROM Item
                                   WHERE ItemID=?""", (item_id,))
        for i in item:
            return i

if __name__ == "__main__":
    Database(db_name="ibli.db").get_item(1)