class InventoryController:
    def __init__(self):
        self.model = InventoryModel()
        self.view = InventoryView(self)
