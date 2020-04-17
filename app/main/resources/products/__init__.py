from app.main.extensions import api
from app.main.resources.products.routes import Product, ProductList

api.add_resource(ProductList, '/products', endpoint='products')
api.add_resource(Product, '/products/<int:id>', endpoint='product')
