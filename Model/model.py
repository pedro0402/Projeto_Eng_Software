import sqlite3
import random

class InventoryModel:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            sector TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def generate_unique_id(self):
        while True:
            product_id = random.randint(1, 99999)
            if not self.product_exists(product_id):
                return product_id

    def product_exists(self, product_id):
        query = "SELECT 1 FROM products WHERE id = ?"
        cursor = self.conn.execute(query, (product_id,))
        return cursor.fetchone() is not None

    def get_product_by_name(self, name):
        query = "SELECT * FROM products WHERE name = ?"
        cursor = self.conn.execute(query, (name,))
        return cursor.fetchone()

