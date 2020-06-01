"""Seed database script."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


# script begin

# reset database
os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()


# seed movie data
## get movie data from file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

## store movies in list
movies_in_db = []

## create movie for each item in movie_data and add them to movies_in_db
for entry in movie_data:
    # process the release date string into datetime type
    format = '%Y-%m-%d'
    date = datetime.strptime(entry['release_date'], format)

    movie = crud.create_movie(entry['title'],
                        entry['overview'],
                        date,
                        entry['poster_path'])

    movies_in_db.append(movie)


# seed fake test users
## create 10 users, each with 10 ratings
for n in range(10):
    email = f'user{n}@test.com' # unique email
    password = 'test'

    user = crud.create_user(email, password)

    for _ in range(10):
        movie = choice(movies_in_db)
        score = randint(1, 5)

        crud.create_rating(user, movie, score)
