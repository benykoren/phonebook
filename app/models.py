import dataclasses
from app import db


@dataclasses.dataclass
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    phone = db.Column(db.String(20), nullable=False, default='')
    address = db.Column(db.String(200), default='')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address
        }
