from Model.model import InventoryModel
from View.view import InventoryView

class InventoryController:
    def __init__(self):
        self.model = InventoryModel()
        self.view = InventoryView(self)
