from dao.AbstractProductDao import ProductDaoService
from db.db_connection import DBConnection
from models.product import Product
from typing import List
from pymysql.cursors import DictCursor
class ProductDaoImplementation(ProductDaoService):
    'implementation for abstract class ProductDaoService'
    #SQL queries
    DISPLAY_ALL = "SELECT * from products"
    INSERT_PRODUCT = "INSERT INTO products(productname,unitprice,categoryid,manufacturedate,isActive) VALUES (%s, %s, %s, %s, %s)"
    FIND_BY_ID = "SELECT * FROM products WHERE productid=%s"
    UPDATE_PRODUCT= "UPDATE products set productname=%s, unitprice=%s WHERE productid=%s"
    APPLY_GST = "CALL apply_gst_to_product(%s,%s)"
    def __init__(self):
        self.conn = DBConnection().get_connection()
    

    def insert_products(self, product:Product)->bool:
        try :
            cursor = self.conn.cursor() #create a cursor object
            cursor.execute(self.INSERT_PRODUCT, 
                           (product.get_productname(),
                           product.get_unitprice(),
                           product.get_category_id(),
                           product.get_manufature_date(),
                           product.get_is_active()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting product:",e)
            return False
        finally:
            cursor.close()

    def display_all_products(self)->List[Product]:
        products=[]#to store the records from db
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)#return data in dic format
            cursor.execute(self.DISPLAY_ALL)#fire the query
            rows = cursor.fetchall()
            for row in rows:
                products.append(Product(productid=row["productid"],
                                        productName=row["productname"],
                                        unitprice=row["unitprice"],
                                        categoryid=row["categoryid"],
                                        manufacturedate=row["manufacturedate"],
                                        is_active=row["isActive"]))
        except Exception as e:
            print("Error fetching products:",e)
        finally :
            cursor.close()
        return products
     
    
    def find_by_product_id(self, product_id:int):
        product = None
        try :
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_ID,(product_id,))
            row = cursor.fetchone()
            if row:
                product = Product(
                    productid=row["productid"],
                    productName=row["productname"],
                    unitprice=row["unitprice"],
                    categoryid=row["categoryid"],
                    manufacturedate=row["manufacturedate"],
                    is_active=row["isActive"]
                )
        except Exception as e:
            print("Error finding product:",e)
        finally:
            cursor.close()
        return product
    
    def update_product(self,product:Product, product_id:int)->bool:
        try :
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.UPDATE_PRODUCT,
                            (product.get_productname(),
                              product.get_unitprice(), product_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating product:",e)
            return False
        finally:
            cursor.close()
             
    def apply_gst(self,product_id:int,gst_percent:float)->bool:
        cursor = None
        try :
            cursor = self.conn.cursor()
            cursor.execute(self.APPLY_GST, (product_id,gst_percent))
            self.conn.commit()
            return cursor.rowcount >=0 #since sp returns 0 if already applied
        except Exception as e:
            print("Error Applying GST:",e)
            return False
        finally:
            if cursor:
                cursor.close()