from abc import ABC, abstractmethod
from typing import List
from models.product import Product

class ProductDaoService(ABC):
    @abstractmethod
    def display_all_products(self)->List[Product]:
        '''fetch all products'''
        pass

    @abstractmethod
    def insert_products(self)->bool:
        '''insert a product to db'''
        pass
    @abstractmethod
    def find_by_product_id(self,product_id:int) ->Product:
        '''find a product by ID'''
        pass
    @abstractmethod
    def update_product(self, product:Product,product_id:int)->bool:
        '''update a product by its ID'''
        pass

    @abstractmethod
    def apply_gst(self, product_id:int, gst_percent:float) ->bool:
        '''compute the gst of the product'''
        pass
