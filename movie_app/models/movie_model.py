from movie_app import db

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.String(), nullable=False, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer(), nullable=True)
    rating = db.Column(db.Integer(), nullable=True)
    genre = db.Column(db.String(), nullable=True)
    director = db.Column(db.String(), nullable=True)
    actors = db.Column(db.String(), nullable=True)
    cover = db.Column(db.String(), nullable=True)
    plot = db.Column(db.String(), nullable=True)
    
    def __init__(self, id, title, year, rating, genre,
    director, writer, plot, cover):
        self.id = id
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.director = director
        self.writer = writer
        self.cover = cover
        self.plot = plot


    
    def __repr__(self):
        return f"Movies {self.id}"