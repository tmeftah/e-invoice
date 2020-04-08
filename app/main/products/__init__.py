from app.main.resources import api
from app.main.products.routes import ProductList, Product


api.add_resource(ProductList, '/products', endpoint='products')
api.add_resource(Product, '/products/<int:id>', endpoint='product')
