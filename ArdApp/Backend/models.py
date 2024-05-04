from flask_login import UserMixin
from datetime import datetime

from app import db, manager


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(128), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User: {self.id}, {self.login}>'   

class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable = False)
    date_entry= db.Column(db.DateTime, default=datetime.utcnow)
    soil_temperature = db.Column(db.Float)
    soil_humidity = db.Column(db.Float)
    air_temperature = db.Column(db.Float)
    air_humidity = db.Column(db.Float)
    light_intensity = db.Column(db.Float)

    def __repr__(self):
        return f'<History: {self.id}, {self.date_entry}, {self.soil_temperature}, {self.soil_humidity}, {self.air_temperature}, {self.air_humidity}, {self.light_intensity}>'   
    
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
