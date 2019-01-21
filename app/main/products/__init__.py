from ..resources import api
from . routes import List, GetProduct


api.add_resource(List, '/product/list')
api.add_resource(GetProduct, '/product/')
