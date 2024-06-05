from Model.model import InventoryModel
from View.view import InventoryView

class InventoryController:
    def __init__(self):
        self.model = InventoryModel()
        self.view = InventoryView(self)

    def add_product(self, name, quantity, sector):
        self.model.add_product(name, quantity, sector)

    def subtract_product_quantity(self, name, quantity):
        self.model.subtract_product_quantity(name, quantity)

    def subtract_product_quantity_by_id(self, product_id, quantity):
        self.model.subtract_product_quantity_by_id(product_id, quantity)

    def delete_product(self, name):
        self.model.delete_product(name)

    def delete_product_by_id(self, product_id):
        self.model.delete_product_by_id(product_id)

    def get_all_products(self):
        return self.model.get_all_products()

    def run(self):
        self.view.mainloop()
