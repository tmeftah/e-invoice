from app.main.brands.routes import Brand, BrandList
from app.main.resources import api

api.add_resource(BrandList, '/brands', endpoint='brands')
api.add_resource(Brand, '/brands/<int:id>', endpoint='brand')
