from app import db
from sqlalchemy import ForeignKey, BigInteger

class Banks(db.Model):
    __tablename__ = 'banks'

    id = db.Column(BigInteger, primary_key=True, nullable=False)
    name = db.Column(db.String(49))
    branches = db.relationship('Branches', backref=db.backref('branches', single_parent=True), lazy='dynamic')

    def __init__(self, name, bank_id):
        self.name = name
        self.id = bank_id


    def to_dict(self):
        return {
            'id': self.bank_id,
            'name': self.name,
        }

