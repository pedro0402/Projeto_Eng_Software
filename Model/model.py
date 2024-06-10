import sqlite3
import random
import pandas as pd

class InventoryModel:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = self.create_connection()
        self.create_table()

    def create_connection(self):
        """Cria uma conexão com o banco de dados e retorna o objeto de conexão."""
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Cria a tabela de produtos se ela não existir."""
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            sector TEXT NOT NULL
        )
        """
        self.execute_query(query)

    def execute_query(self, query, params=()):
        """Executa uma consulta com parâmetros opcionais."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
            return None

    def generate_unique_id(self):
        """Gera um ID único para um produto."""
        while True:
            product_id = random.randint(1, 99999)
            if not self.product_exists(product_id):
                return product_id

    def product_exists(self, product_id):
        """Verifica se um produto existe pelo seu ID."""
        query = "SELECT 1 FROM products WHERE id = ?"
        cursor = self.execute_query(query, (product_id,))
        return cursor.fetchone() is not None if cursor else False

    def get_product_by_name(self, name):
        """Obtém um produto pelo seu nome."""
        query = "SELECT * FROM products WHERE name = ?"
        cursor = self.execute_query(query, (name,))
        return cursor.fetchone() if cursor else None

    def add_product(self, name, quantity, sector):
        """Adiciona um novo produto ou atualiza um existente."""
        if not name or not isinstance(quantity, int) or not sector:
            raise ValueError("Detalhes do produto inválidos.")

        product = self.get_product_by_name(name)
        if product:
            if product[3] != sector:
                product_id = self.generate_unique_id()
                query = "INSERT INTO products (id, name, quantity, sector) VALUES (?, ?, ?, ?)"
                self.execute_query(query, (product_id, name, quantity, sector))
            else:
                new_quantity = product[2] + quantity
                query = "UPDATE products SET quantity = ? WHERE name = ?"
                self.execute_query(query, (new_quantity, name))
        else:
            product_id = self.generate_unique_id()
            query = "INSERT INTO products (id, name, quantity, sector) VALUES (?, ?, ?, ?)"
            self.execute_query(query, (product_id, name, quantity, sector))

    def subtract_product_quantity_by_id(self, product_id, quantity):
        """Subtrai uma quantidade de um produto pelo seu ID."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantidade inválida.")

        product = self.get_product_by_id(product_id)
        if product:
            new_quantity = max(product[2] - quantity, 0)
            query = "UPDATE products SET quantity = ? WHERE id = ?"
            self.execute_query(query, (new_quantity, product_id))

    def delete_product(self, name):
        """Exclui um produto pelo seu nome."""
        query = "DELETE FROM products WHERE name = ?"
        self.execute_query(query, (name,))

    def delete_product_by_id(self, product_id):
        """Exclui um produto pelo seu ID."""
        query = "DELETE FROM products WHERE id = ?"
        self.execute_query(query, (product_id,))

    def get_product_by_id(self, product_id):
        """Obtém um produto pelo seu ID."""
        query = "SELECT * FROM products WHERE id = ?"
        cursor = self.execute_query(query, (product_id,))
        return cursor.fetchone() if cursor else None

    def get_all_products(self):
        """Obtém todos os produtos do banco de dados."""
        query = "SELECT * FROM products"
        cursor = self.execute_query(query)
        return cursor.fetchall() if cursor else []

    def export_to_excel(self, file_path):
        """Exporta todos os produtos para um arquivo Excel."""
        query = "SELECT * FROM products"
        data = pd.read_sql(query, self.conn)
        data.to_excel(file_path, index=False)

    def get_all_sectors(self):
        """Obtém todos os setores distintos da tabela de produtos."""
        query = "SELECT DISTINCT sector FROM products"
        cursor = self.execute_query(query)
        return [row[0] for row in cursor.fetchall()] if cursor else []

# Uso
if __name__ == "__main__":
    inventory = InventoryModel()
    # Realizar operações
    inventory.close_connection()
