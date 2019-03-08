from app import db
from models.banks import Banks
from sqlalchemy import ForeignKey, BigInteger

class Branches(db.Model):
    __tablename__ = 'branches'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    ifsc = db.Column(db.String(11), primary_key=True, nullable=False)
    bank_id = db.Column(BigInteger, ForeignKey("banks.id"))
    branch = db.Column(db.String(74))
    address = db.Column(db.String(195))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    state = db.Column(db.String(26))

    def __init__(self, ifsc, bank_id, branch="", address="", city="", district="", state="", name=""):
        self.ifsc = ifsc
        self.bank_id = bank_id
        self.branch = branch
        self.address = address
        self.city = city
        self.district = district
        self.state = state
        Banks(name=name, bank_id=bank_id)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        bank = Banks.query.filter_by(id=self.bank_id).first()
        bank_name = bank.name
        return {
            'bank_name': bank_name,
            'ifsc': self.ifsc,
            'bank_id': self.bank_id,
            'branch': self.branch,
            'address': self.address,
            'city': self.city,
            'district': self.district,
            'state': self.state
        }

