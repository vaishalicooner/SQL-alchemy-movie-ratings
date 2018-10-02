"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
import datetime


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print("Movies")

        # Delete all rows in table, so if we need to run this a second time,
        # we won't be trying to add duplicate users
    Movie.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        item = row.split("|")
        # print(item)
        movie_id = item[0]
        title = item[1]
        released_str = item[2]
        imdb_url = item[3]
        #print (released_str)
        if released_str:
            released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        else:
              released_at = None

        movie = Movie(movie_id=movie_id,title = title,
                    released_at=released_at,imdb_url = imdb_url)

        # We need to add to the session or it won't ever be smovies (movie_id, title, released_at, imdb_url) VALUES (%(movie_id)s, %(title)s, %(released_at)s, %(imdb_url)s)'] [parameters: ({'movie_id': '1', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '2', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '3', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '4', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '5', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '6', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '7', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '8', 'title': None, 'released_at': datetime.datetime(1995, 1, 1, 0, 0), 'imdb_url': None}  ... displaying 10 of 1681 total bound parameter sets ...  {'movie_id': '1681', 'title': None, 'released_at': datetime.datetime(1994, 1, 1, 0, 0), 'imdb_url': None}, {'movie_id': '1682tored
        db.session.add(movie)

    # Once we're done, we should commit our work
    db.session.commit()



def load_ratings():
    """Load ratings from u.data into database."""

    print("Ratings")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        rating_id, movie_id, user_id, score = row.split("\t")

        rating = Rating(user_id=user_id,
                    movie_id=movie_id, score = score, rating_id = rating_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
