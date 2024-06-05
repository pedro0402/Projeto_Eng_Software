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
        
    def validate_quantity(self, new_value):
        if new_value.isdigit() or new_value == "":
            return True
        return False

    def create_manage_inventory_screen(self):
        self.clear_screen()

        self.products_frame = ctk.CTkFrame(self)
        self.products_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.create_product_list()

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(pady=10)

        self.remove_button = ctk.CTkButton(self.action_frame, text="Retirar Produto", command=self.show_remove_product_window)
        self.remove_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self.action_frame, text="Excluir Produto", command=self.show_delete_product_window)
        self.delete_button.pack(side="right", padx=10)

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.create_home_screen)
        self.back_button.pack(pady=10)


    def create_product_list(self):
        products = self.controller.get_all_products()
        self.products_table = ctk.CTkScrollableFrame(self.products_frame)
        self.products_table.pack(fill="both", expand=True, padx=10, pady=10)

        headers = ["ID", "Nome", "Quantidade", "Setor"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.products_table, text=header, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=i, padx=5, pady=5)

        for row_num, product in enumerate(products, start=1):
            for col_num, detail in enumerate(product):
                detail_label = ctk.CTkLabel(self.products_table, text=detail, font=("Arial", 12))
                detail_label.grid(row=row_num, column=col_num, padx=5, pady=5)
                if col_num == 0:  # ID column
                    detail_label.bind("<Button-1>", lambda e, text=detail: self.copy_to_clipboard(text))

    