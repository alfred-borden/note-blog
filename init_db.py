from views import db
from models import Post
from datetime import date


db.create_all()

db.session.commit()