from app.main.resources import api
from app.main.products.routes import List, GetProduct


api.add_resource(List, '/product/list')
api.add_resource(GetProduct, '/product/')
