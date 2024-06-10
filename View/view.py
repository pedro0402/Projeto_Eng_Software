import customtkinter as ctk
from tkinter import messagebox

class InventoryView(ctk.CTk):
    def __init__(self, controller):
        """Inicializa a interface de usuário do gerenciador de estoque."""
        super().__init__()

        self.controller = controller
        self.title("STOCK SEC - Gerenciador de Estoque")
        self.geometry("800x600")

        self.create_home_screen()

    def create_home_screen(self):
        """Cria a tela inicial com botões para navegação."""
        self.clear_screen()

        self.title_label = ctk.CTkLabel(self, text="STOCK SEC", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.add_product_button = ctk.CTkButton(self, text="Cadastro de Produtos", command=self.create_add_product_screen)
        self.add_product_button.pack(pady=10)

        self.manage_inventory_button = ctk.CTkButton(self, text="Gestão do Estoque", command=self.create_manage_inventory_screen)
        self.manage_inventory_button.pack(pady=10)

    def create_add_product_screen(self):
        """Cria a tela para adicionar um novo produto."""
        self.clear_screen()
        self.create_form("Adicionar Produto", self.add_product)

    def create_form(self, button_text, submit_command):
        """Cria um formulário de produto com campos comuns."""
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

        self.submit_button = ctk.CTkButton(self, text=button_text, command=submit_command)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.create_home_screen)
        self.back_button.pack(pady=10)

    def validate_quantity(self, new_value):
        """Valida se a quantidade inserida é um número positivo."""
        return new_value.isdigit() or new_value == ""

    def create_manage_inventory_screen(self):
        """Cria a tela de gestão de inventário com opções de filtro e listagem de produtos."""
        self.clear_screen()

        self.create_filter_frame()
        self.create_product_list_frame()
        self.create_action_frame()

    def create_filter_frame(self):
        """Cria a seção de filtro por setor na tela de gestão de inventário."""
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=10)

        self.back_button = ctk.CTkButton(self.filter_frame, text="Voltar", command=self.create_home_screen)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.filter_label = ctk.CTkLabel(self.filter_frame, text="Filtrar por Setor:")
        self.filter_label.grid(row=0, column=1, padx=5, pady=5)

        self.filter_var = ctk.StringVar()
        self.filter_options = ["Todos"] + self.controller.model.get_all_sectors()
        self.filter_var.set("Todos")
        self.filter_menu = ctk.CTkOptionMenu(self.filter_frame, values=self.filter_options, variable=self.filter_var, command=self.apply_filter)
        self.filter_menu.grid(row=0, column=2, padx=5, pady=5)

    def create_product_list_frame(self):
        """Cria a lista de produtos na tela de gestão de inventário."""
        self.products_frame = ctk.CTkFrame(self)
        self.products_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.create_product_list()

    def create_action_frame(self):
        """Cria a seção de ações na tela de gestão de inventário."""
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(pady=10)

        self.remove_button = ctk.CTkButton(self.action_frame, text="Retirar Produto", command=self.show_remove_product_window)
        self.remove_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self.action_frame, text="Excluir Produto", command=self.show_delete_product_window)
        self.delete_button.pack(side="right", padx=10)

        self.show_export_excel_button()

    def create_product_list(self):
        """Cria a tabela de listagem de produtos."""
        self.products_table = ctk.CTkScrollableFrame(self.products_frame)
        self.products_table.pack(fill="both", expand=True, padx=10, pady=10)

        headers = ["ID", "Nome", "Quantidade", "Setor"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.products_table, text=header, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=i, padx=5, pady=5)

        self.update_product_list()

    def update_product_list(self):
        """Atualiza a lista de produtos com base no filtro selecionado."""
        sector_filter = self.filter_var.get()
        products = self.controller.get_all_products()

        if sector_filter != "Todos":
            products = [product for product in products if product[3] == sector_filter]

        self.clear_product_list()

        for row_num, product in enumerate(products, start=1):
            for col_num, detail in enumerate(product):
                if col_num == 2 and detail == 0:
                    detail = "Fora de Estoque"
                detail_label = ctk.CTkLabel(self.products_table, text=detail, font=("Arial", 12))
                detail_label.grid(row=row_num, column=col_num, padx=5, pady=5)
                if col_num == 0:
                    detail_label.bind("<Button-1>", lambda e, text=detail: self.copy_to_clipboard(text))

    def clear_product_list(self):
        """Limpa a tabela de listagem de produtos."""
        for widget in self.products_table.winfo_children():
            widget.destroy()

    def copy_to_clipboard(self, text):
        """Copia o ID do produto para a área de transferência."""
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("ID Copiado", f"ID {text} copiado para a área de transferência!")

    def apply_filter(self, *args):
        """Aplica o filtro de setor e atualiza a lista de produtos."""
        self.update_product_list()

    def add_product(self):
        """Adiciona um novo produto ao inventário."""
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        sector = self.sector_var.get()

        if not name:
            messagebox.showerror("Erro", "Por favor, preencha o nome do produto.")
            return

        if not quantity.isdigit():
            messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
            return

        quantity = int(quantity)

        self.controller.add_product(name, quantity, sector)
        self.create_manage_inventory_screen()

    def remove_product(self):
        """Remove uma quantidade especificada de um produto pelo seu ID."""
        id_or_name = self.remove_id_entry.get().strip()
        quantity = self.remove_quantity_entry.get().strip()

        if not id_or_name:
            messagebox.showerror("Erro", "Por favor, preencha o ID do produto.")
            return

        if not quantity.isdigit():
            messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
            return

        quantity = int(quantity)

        if quantity <= 0:
            messagebox.showerror("Erro", "A quantidade a ser retirada deve ser maior do que zero.")
            return

        product = self.controller.get_product_by_id(id_or_name)

        if not product:
            messagebox.showerror("Erro", "O ID está incorreto.")
            return

        if quantity > product[2]:
            messagebox.showerror("Erro", f"A quantidade a ser retirada ({quantity}) é maior do que a quantidade disponível no estoque ({product[2]}).")
            return

        self.controller.subtract_product_quantity_by_id(id_or_name, quantity)

        self.remove_window.destroy()
        self.create_manage_inventory_screen()

    def show_export_excel_button(self):
        """Exibe o botão de exportação para Excel."""
        self.export_button = ctk.CTkButton(self.action_frame, text="Exportar Excel", command=self.export_to_excel)
        self.export_button.pack(side="right", padx=16)

    def export_to_excel(self, file_path="inventory.xlsx"):
        """Exporta os dados do inventário para um arquivo Excel."""
        try:
            if not file_path:
                raise ValueError("Caminho do arquivo não fornecido.")

            self.controller.export_excel(file_path)

            messagebox.showinfo("Exportação Concluída", f"Os dados foram exportados para {file_path} com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro na Exportação", f"Ocorreu um erro ao exportar para Excel: {e}")

    def delete_product(self):
        """Exclui um produto pelo seu ID."""
        id_or_name = self.delete_id_entry.get().strip()

        if not id_or_name:
            messagebox.showerror("Erro", "Por favor, preencha o ID do produto.")
            return

        if not id_or_name.isdigit():
            messagebox.showerror("Erro", "O ID está incorreto.")
            return

        self.controller.delete_product_by_id(id_or_name)

        self.delete_window.destroy()
        self.create_manage_inventory_screen()

    def show_remove_product_window(self):
        """Exibe a janela para remover uma quantidade de um produto."""
        self.remove_window = ctk.CTkToplevel(self)
        self.remove_window.title("Retirar Produto")
        self.remove_window.geometry("400x200+{}+{}".format(self.winfo_x() + self.winfo_width() // 2 - 200, self.winfo_y() + self.winfo_height() // 2 - 100))
        self.remove_window.transient(self)
        self.remove_window.grab_set()

        self.remove_id_label = ctk.CTkLabel(self.remove_window, text="ID do Produto:")
        self.remove_id_label.pack(pady=5)
        self.remove_id_entry = ctk.CTkEntry(self.remove_window)
        self.remove_id_entry.pack(pady=5)

        self.remove_quantity_label = ctk.CTkLabel(self.remove_window, text="Quantidade a Retirar:")
        self.remove_quantity_label.pack(pady=5)
        self.remove_quantity_entry = ctk.CTkEntry(self.remove_window)
        self.remove_quantity_entry.pack(pady=5)

        self.remove_confirm_button = ctk.CTkButton(self.remove_window, text="Confirmar", command=self.remove_product)
        self.remove_confirm_button.pack(pady=10)

    def show_delete_product_window(self):
        """Exibe a janela para excluir um produto."""
        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.title("Excluir Produto")
        self.delete_window.geometry("400x150+{}+{}".format(self.winfo_x() + self.winfo_width() // 2 - 200, self.winfo_y() + self.winfo_height() // 2 - 75))
        self.delete_window.transient(self)
        self.delete_window.grab_set() 

        self.delete_id_label = ctk.CTkLabel(self.delete_window, text="ID do Produto:")
        self.delete_id_label.pack(pady=5)
        self.delete_id_entry = ctk.CTkEntry(self.delete_window)
        self.delete_id_entry.pack(pady=5)

        self.delete_confirm_button = ctk.CTkButton(self.delete_window, text="Confirmar", command=self.delete_product)
        self.delete_confirm_button.pack(pady=10)

    def clear_screen(self):
        """Limpa todos os widgets da tela atual."""
        for widget in self.winfo_children():
            widget.destroy()
