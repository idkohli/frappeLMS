from library import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.Integer, nullable=True)
    dues = db.Column(db.Integer, nullable=True, default=0)
    books = db.relationship('Books', backref='member', lazy=True)

    def __repr__(self):
        return f"Member('{self.name}', '{self.email}', '{self.dues}')"

class Books(db.Model):
    id = db.Column(db.String(30), nullable=False, unique=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(1000), nullable=False)
    average_rating = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=True)
    isbn13 = db.Column(db.Integer, unique=True, nullable=True)
    language = db.Column(db.String(5), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    ratings_count = db.Column(db.Integer, nullable=True)
    text_reviews_count = db.Column(db.Integer, nullable=True)
    publication_date = db.Column(db.DateTime, nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.authors}', '{self.member_id}')"
