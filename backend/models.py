from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

    def get_id(self):
        return f"admin-{self.id}"
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150))
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return f"user-{self.id}"
    
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    price_per_hour = db.Column(db.Float)
    total_spots = db.Column(db.Integer)
    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete-orphan")

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), default='A')
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    reservations = db.relationship('Reservation', backref='spot', cascade="all, delete-orphan")

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parked_at = db.Column(db.DateTime)
    left_at = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    vehicle_number = db.Column(db.String(20), nullable=False) 
    user = db.relationship('User', backref=db.backref('reservations', cascade='all, delete-orphan'))