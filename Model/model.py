import sqlite3
import random
import pandas as pd

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

    def add_product(self, name, quantity, sector):
        product = self.get_product_by_name(name)
        if product:
            # Verifica se já existe um produto com o mesmo nome em um setor diferente
            if product[3] != sector:
                product_id = self.generate_unique_id()  # Gera um novo ID único
                query = "INSERT INTO products (id, name, quantity, sector) VALUES (?, ?, ?, ?)"
                self.conn.execute(query, (product_id, name, quantity, sector))
            else:
                new_quantity = product[2] + quantity
                query = "UPDATE products SET quantity = ? WHERE name = ?"
                self.conn.execute(query, (new_quantity, name))
        else:
            product_id = self.generate_unique_id()
            query = "INSERT INTO products (id, name, quantity, sector) VALUES (?, ?, ?, ?)"
            self.conn.execute(query, (product_id, name, quantity, sector))
        self.conn.commit()


    def subtract_product_quantity_by_id(self, product_id, quantity):
        product = self.get_product_by_id(product_id)
        if product:
            new_quantity = max(product[2] - quantity, 0)
            query = "UPDATE products SET quantity = ? WHERE id = ?"
            self.conn.execute(query, (new_quantity, product_id))
            self.conn.commit()

    def delete_product(self, name):
        query = "DELETE FROM products WHERE name = ?"
        self.conn.execute(query, (name,))
        self.conn.commit()

    def delete_product_by_id(self, product_id):
        query = "DELETE FROM products WHERE id = ?"
        self.conn.execute(query, (product_id,))
        self.conn.commit()

    def get_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id = ?"
        cursor = self.conn.execute(query, (product_id,))
        return cursor.fetchone()

    def get_all_products(self):
        query = "SELECT * FROM products"
        cursor = self.conn.execute(query)
        return cursor.fetchall()
    
    def export_to_excel(self, file_path):
        query = "SELECT * FROM products"
        data = pd.read_sql(query, self.conn)
        data.to_excel(file_path, index=False)

    def get_all_sectors(self):
        query = "SELECT DISTINCT sector FROM products"
        cursor = self.conn.execute(query)
        sectors = [row[0] for row in cursor.fetchall()]
        return sectors

inventory = InventoryModel()