from datetime import datetime
from views import db

class Post(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<title {0}>'.format(self.title)