import customtkinter as ctk
from tkinter import messagebox

class InventoryView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("STOCK SEC - Gerenciador de Estoque")
        self.geometry("800x600")

        self.create_home_screen()

    