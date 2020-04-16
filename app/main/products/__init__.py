from app.main.products.routes import Product, ProductList
from app.main.resources import api

api.add_resource(ProductList, '/products', endpoint='products')
api.add_resource(Product, '/products/<int:id>', endpoint='product')
