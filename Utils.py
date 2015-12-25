"""Utility functions to help with testing 
"""

from Flask import Person, Movie, db


def create_test_data():
    """Creates a set of people and movies to make testing easier
    """
    people = (
              Person('Chris'),
              Person('Max'),
              Person('John'),
              Person('Allan'),
              )
    for person in people:
        db.session.add(person)
    db.session.commit()
    
    movies = (
              Movie('Die Hard', 132),
              Movie('Shrek', 90),
              Movie('Toy Story', 81))
    for movie in movies:
        db.session.add(movie)
    db.session.commit()