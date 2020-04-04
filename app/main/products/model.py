from app.main.resources import db


class ProductModel(db.Model):
    """ User Model for storing user details """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(120), unique=True, nullable=False)
    weight = db.Column(db.Float)

    @classmethod
    def find_by_ref(self, ref):
        return self.query.filter_by(ref=ref).first()

    @classmethod
    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    @classmethod
    def return_all(self):
        def to_json(product):
            return {
                'id': product.id,
                'ref': product.ref
            }
        return {'products': list(map(lambda user: to_json(user), ProductModel.query.all()))}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Product '{}'>".format(self.ref)
