import logging
from Model.model import InventoryModel
from View.view import InventoryView

class InventoryController:

   
    def __init__(self, model=None, view=None):
         
        """Inicializa o controlador, conectando o modelo e a visão.
        Permite injeção de dependência para facilitar testes."""

        try:
            self.model = model if model is not None else InventoryModel()
            self.view = view if view is not None else InventoryView(self)
        except ImportError as e:
            logging.error(f"Erro ao importar módulos: {e}")

        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_quantity(self, quantity):
        """Valida a quantidade, permitindo que seja um número positivo."""
        if quantity <= 0:
            self.logger.error("Quantidade deve ser positiva.")
            return False
        return True

    def add_product(self, name, quantity, sector):
        """Adiciona um produto ao invntário"""

        if not self.validate_quantity(quantity):
            return "Quantidade inválida. Deve ser positiva."
        try:
            self.model.add_product(name, quantity, sector)
            self.logger.info(f"Produto  adicionado {name}, Quantidade: {quantity}, Setor: {sector}")
            return "Produto adicionado com sucesso."
        except Exception as e:
            self.logger.error(f"Erro ao adicionar produto: {e}")
            return "Erro ao adicionar produto."
            
    def subtract_product_quantity(self, name, quantity):
        """Subtrai a quantidade de um produto do inventário."""
        
        if not self.validate_quantity(quantity):
            return "Quantidade inválida. Deve ser positiva."
        try:
            self.model.subtract_product_quantity(name, quantity)
            self.logger.info(f"Produto subtraído: {name}, Quantidade subtraída: {quantity}")
        except Exception as e:
            self.logger.error(f"Erro ao subtrair quantidade: {e}")

    def subtract_product_quantity_by_id(self, product_id, quantity):
        """Subtrai a quantidade de um produto do inventário pelo ID."""

        if not self.validate_quantity(quantity):
            return "Quantidade inválida. Deve ser positiva."
        try:
            self.model.subtract_product_quantity_by_id(product_id, quantity)
            self.logger.info(f"Produto subtraído por ID: {product_id}, Quantidade: {quantity}")
            return "Quantidade subtraída com sucesso."
        except Exception as e:
            self.logger.error(f"Erro ao subtrair produto por ID: {e}")
            return("Erro ao subtrair quantidade.")
        
    def delete_product(self, name):
        """Remove um produto do inventário pelo nome."""
        try:
            self.model.delete_product(name)
            self.logger.info(f"Produto deletado: {name}")
            return "Produto deletado com sucesso."
        except Exception as e:
            self.logger.error(f"Erro ao deletar produto: {e}")
            return "Erro ao deletar produto."
        
    def delete_product_by_id(self, product_id):
        """Remove um produto do inventário pelo ID."""
        try:
            self.model.delete_product_by_id(product_id)
            self.logger.info(f"Produto deletado por ID: {product_id}")
            return "Produto por ID deletado com sucesso."
        except Exception as e:
            self.logger.error(f"Erro ao deletar por ID: {e}")
            return "Erro ao deletar produto"
        
    def get_all_products(self):
        """Retorna todos os produtos do inventário."""
        try:
            products = self.model.get_all_products()
            self.logger.info("Recuperado todos os produtos.")
            return products
        except Exception as e:
            self.logger.error(f"Erro ao recuperar produtos: {e}")
            return "Erro ao recuperar"
        

    def get_product_by_id(self, product_id):
        return self.model.get_product_by_id(product_id)
    
    
    def get_product_by_name(self, name):
        return self.model.get_product_by_name(name)
    
    def get_product_addition_history(self):
        return self.model.get_product_addition_history()
    
    def get_history(self):
        return self.model.get_product_addition_history()
    
    def export_excel(self, file_path):
        return self.model.export_to_excel(file_path)
    
    def run(self):
        """Inicia interface gráfica"""
        try:
            self.view.mainloop()
        except Exception as e:
            self.logger.error(f"Erro ao executar interface gráfica: {e}")
