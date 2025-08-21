from dao.ProductDaoImple import ProductDaoImplementation
from dao.AbstractProductDao import ProductDaoService
from models.product import Product
from datetime import datetime
class ProductManagementLib:
    'handles CRUD logic'
    
    dao_service: ProductDaoService = ProductDaoImplementation()

    @staticmethod
    def display_all():
        products = ProductManagementLib.dao_service.display_all_products()
        for product in products:
            print(product)
    
    @staticmethod
    def add_product():
        product = Product()
        productname= input("Enter the product Name:")
        product.set_product_name(productname)
        unitprice= float(input("Enter the Unit Price:"))
        product.set_unitprice(unitprice)
        categoryid = int(input("Enter the Category Id:"))
        product.set_category_id(categoryid)
        m_date = input("Enter manufacture Date(dd/MM/YYYY):")
        util_date = datetime.strptime(m_date, "%d/%m/%Y")
        mysql_date = util_date.strftime("%Y-%m-%d")
        product.set_manufacture_date(mysql_date)

        if ProductManagementLib.dao_service.insert_products(product):
            print("inserted successfully....")
        else:
            print("something went wrong.....")

    @staticmethod
    def update_product():
        searchid = int(input("Enter the product ID:"))
        #create a method in DAO
        product = ProductManagementLib.dao_service.find_by_product_id(searchid)
        if not product:
            print("Product not found")
            return
        print(product)
        confirm = input("Do you want to edit this data?(y/n)")
        if confirm.lower()=='y':
            product.set_product_name(input("Enter new product Name:"))
            product.set_unitprice(float(input("Enter New Unit Price:")))
            #pass the object to dao update
            if ProductManagementLib.dao_service.update_product(product,searchid):
                print("updated successfully ....")
                  
            else:
                print("something went wrong....")
    
    @staticmethod
    def apply_gst_to_product():
        product_id = int(input("Enter the product ID to appply GST:"))
        gst_percent = float(input("Enter GST percentage to apply:"))
        if ProductManagementLib.dao_service.apply_gst(product_id,gst_percent):
            print(f"GST of {gst_percent} applied to product ID {product_id}")
        else:
            print("failed to apply GST")