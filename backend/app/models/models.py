from app import db
from werkzeug.security import generate_password_hash, check_password_hash

association_table = db.Table('saved_news',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('news_id', db.Integer, db.ForeignKey('news.id')),
                             )


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    saved_news = db.relationship('News', secondary=association_table, backref=db.backref('saved_users', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    news_filter_id = db.Column(db.String, nullable=False, unique=True)
    source = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    description = db.Column(db.String)
    url = db.Column(db.String)
    image_url = db.Column(db.String)
    published_at = db.Column(db.String)
    text = db.Column(db.String)
    logits = db.Column(db.String)
    sentiment = db.Column(db.String)


# class Link(db.Model):
#     __tablename__ = 'link'
#
#     id = db.Column(db.Integer(), primary_key=True)
#     news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
