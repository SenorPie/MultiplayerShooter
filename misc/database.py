import sys
import sqlite3

class Database:

    def __init__(self, db_name: str):
        """
            The Database class takes in only 1 parameter
            Initialization tries to connect to the database and create tables
            @parameters
                db_name: a string with the database name
        """

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
        """
            add_item() inserts into the Item table with the values provided
            @parameters
                ItemDamage: int
                ItemOffset: int
        """

        self.cur.execute("""INSERT INTO Item(ItemDamage, ItemOffset)
                            VALUES(?, ?)""", (item_dmg, item_offset))
        self.conn.commit()

    def get_item(self, item_id: int) -> tuple:
        """
            get_item() queries the database to get the ItemDamage and ItemOffset from Item table
            @parameters
                item_id: int
            
            @returns tuple
        """
        item = self.cur.execute("""SELECT ItemDamage, ItemOffset FROM Item
                                   WHERE ItemID=?""", (item_id,))
        for i in item:
            return i

if __name__ == "__main__":
    Database(db_name="ibli.db").get_item(1)