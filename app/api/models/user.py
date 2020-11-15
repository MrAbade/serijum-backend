from passlib.hash import pbkdf2_sha256

from ..models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def gen_hash(self):
        self.password = pbkdf2_sha256.hash(self.password)
    
    def password_verify(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return '<User %r>' % self.name
