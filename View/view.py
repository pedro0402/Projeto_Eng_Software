import customtkinter as ctk
from tkinter import messagebox

class InventoryView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("STOCK SEC - Gerenciador de Estoque")
        self.geometry("800x600")

        self.create_home_screen()
        
    def create_home_screen(self):
        self.clear_screen()

        self.title_label = ctk.CTkLabel(self, text="STOCK SEC", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.add_product_button = ctk.CTkButton(self, text="Cadastro de Produtos", command=self.create_add_product_screen)
        self.add_product_button.pack(pady=10)

        self.manage_inventory_button = ctk.CTkButton(self, text="Gestão do Estoque", command=self.create_manage_inventory_screen)
        self.manage_inventory_button.pack(pady=10)

    def create_add_product_screen(self):
        self.clear_screen()

        self.name_label = ctk.CTkLabel(self, text="Nome do Produto:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=5)

        self.quantity_label = ctk.CTkLabel(self, text="Quantidade:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(self.validate_quantity), "%P"))
        self.quantity_entry.pack(pady=5)

        self.sector_label = ctk.CTkLabel(self, text="Setor:")
        self.sector_label.pack(pady=5)

        self.sector_var = ctk.StringVar(value="Informatica")
        self.sector_options = ["Informatica", "Papelaria", "Ferramentas", "Outros"]
        self.sector_menu = ctk.CTkOptionMenu(self, values=self.sector_options, variable=self.sector_var)
        self.sector_menu.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Adicionar Produto", command=self.add_product)
        self.add_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.create_home_screen)
        self.back_button.pack(pady=10)

    