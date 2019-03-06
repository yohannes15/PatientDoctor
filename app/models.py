from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    patients = db.relationship('Patient', backref='therapist', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    dateofbirth = db.Column(db.String(32))
    treatments = db.relationship('Treatment', backref='patientref', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Patient {}>'.format(self.firstname)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    treatmentname = db.Column(db.String(64))
    treatmentnotes = db.Column(db.String(128))
    treatmentdate = db.Column(db.String(32))
    treatmentprice = db.Column(db.Integer())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return '<Treatment {}>'.format(self.treatmentname)
