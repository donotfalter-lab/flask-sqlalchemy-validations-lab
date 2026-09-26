from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Author must have a name.')
        existing = Author.query.filter(Author.name == name).first()
        if existing and existing.id != self.id:
            raise ValueError('Author name must be unique.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number is not None and not (len(phone_number) == 10 and phone_number.isdigit()):
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    CATEGORIES = ('Fiction', 'Non-Fiction')
    CLICKBAIT = ("Won't Believe", 'Secret', 'Top', 'Guess')

    @validates('title')
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError('Post must have a title.')
        if not any(phrase in title for phrase in self.CLICKBAIT):
            raise ValueError(f'Title must contain one of: {", ".join(self.CLICKBAIT)}.')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content is None or len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary is not None and len(summary) > 250:
            raise ValueError('Summary must be at most 250 characters long.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in self.CATEGORIES:
            raise ValueError('Category must be Fiction or Non-Fiction.')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
