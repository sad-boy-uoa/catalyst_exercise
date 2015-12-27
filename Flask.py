#TODO The constraint on Person voting on only one movie once 
#error message if someone has already voted

from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

"""Instantiates the app, loads config and creates database
"""
app = Flask(__name__) 
app.config.from_pyfile('Config.py') 
db = SQLAlchemy(app) 


"""Database models for catalyst_exercise
"""
class Person(db.Model):
       
    __tablename__ = 'person' 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    vote = db.relationship('Vote', backref='person')
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):        
        return '<Person %r>' % (self.name)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    

class Movie(db.Model):
    
    __tablename__ = 'movie'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    length = db.Column(db.Integer)
    votes = db.relationship('Vote', backref='movie')
    
    def __init__(self, title, length):
        self.title = title
        self.length = length
    
    def __repr__(self):
        return '<Title %r>' % self.title
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'length': self.length
        }
 
    
class Vote(db.Model):
    
    __tablename__ = 'vote'
    
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    
    def __init__(self, person, movie):
        self.person_id = person
        self.movie_id = movie
        
    def serialize(self):
        return {
            'person': self.person.name,
            'movie': self.movie.title
        }
 
db.create_all()       

"""URL routing for catalyst_exercise
"""
@app.route('/movies', methods = ['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify({'movies': [movie.serialize() for movie in movies]}) 
   
@app.route('/people', methods = ['GET'])
def get_Person():
    people = Person.query.all()
    return jsonify({'people': [person.serialize() for person in people]}) 

@app.route('/votes', methods = ['GET'])
def get_votes():
    votes = Vote.query.all()
    return jsonify({'votes': [vote.serialize() for vote in votes]})


@app.route('/vote/<int:person_id>/<int:movie_id>', methods = ['POST'])
def vote(person_id, movie_id):
    vote = Vote(person_id, movie_id)
    db.session.add(vote)
    db.session.commit()
    #return (400, jsonify({'error': 'You can only vote once'}))
    return jsonify({'vote': vote.serialize()})
    
    
@app.route('/people/<int:person_id>/votes', methods = ['DELETE'])
def delete_person_votes(person_id): #check this function
    vote = Vote.query.get(person_id)
    db.session.delete(vote)
    db.session.commit()
    return jsonify({'votes': "Votes for personID %r has been deleted" % person_id})
  
@app.route('/votes', methods = ['DELETE'])
def delete_all_votes(): #check this function
    votes = Vote.query.all()
    for vote in votes:
        db.session.delete(vote)
    db.session.commit()
    return jsonify({'votes': "All votes have been deleted"})



"""Run server
"""
if __name__ == '__main__':
    app.run(debug=True)