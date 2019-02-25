from service_api import db
from datetime import datetime


class User(db.Model):
    user_id = db.Column(db.String(25), primary_key=True, autoincrement=False)
    username = db.Column(db.String(25))
    email = db.Column(db.String(50))
    organization = db.Column(db.String(50))
    last_active_date = db.Column(db.DateTime, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __str__(self):
        return "user id: %s; username: %s; email: %s; organization: %s; last_active_date: %s" % \
               (self.user_id, self.username, self.email, self.organization, self.last_active_date)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(25))
    name = db.Column(db.String(25))
    is_user = db.Column(db.Boolean, default=True)
    content = db.Column(db.String(140))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __str__(self):
        return "user id: %s; name: %s; is_user: %s; content: %s" % (self.user_id, self.name, self.is_user, self.content)

