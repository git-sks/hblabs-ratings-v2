"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    # table name
    __tablename__ = "users"

    # table columns
    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=True,
                        )
    email = db.Column(db.String, unique=True, nullable=True,)
    password = db.Column(db.String, nullable=True,)

    # relationships
    # ratings = a list of Rating objects

    def __repr__(self):
        """Human-readable summary of a user"""

        return f'<User user_id={self.user_id} email={self.email}>'


class Movie(db.Model):
    """A movie."""

    # table name
    __tablename__ = "movies"

    # table columns
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    title = db.Column(db.String,)
    overview = db.Column(db.Text,)
    release_date = db.Column(db.DateTime,)
    poster_path = db.Column(db.String,) # movie image URL

    # relationships
    # ratings = a list of Rating objects

    def __repr__(self):
        """Human-readable summary of a movie."""

        return (f'<Movie movie_id={self.movie_id} '
            + f'title={self.title} '
            + f'release_date={self.release_date}>')


class Rating(db.Model):
    """A rating."""

    # table name
    __tablename__ = "ratings"

    # table columns
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    score = db.Column(db.Integer,)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'),)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),)

    # relationships
    movie = db.relationship('Movie', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        """Human-readable summary of a movie."""

        return (f'<Rating rating_id={self.rating_id} score={self.score} '
                + f'movie_id={self.movie_id} user_id={self.user_id}>')


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
