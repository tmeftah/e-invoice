from app.main.extensions import api
from app.main.resources.brands.routes import Brand, BrandList

api.add_resource(BrandList, '/brands', endpoint='brands')
api.add_resource(Brand, '/brands/<int:id>', endpoint='brand')
