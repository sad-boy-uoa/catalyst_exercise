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
            'name': self.name,
            'vote': self.vote.movie.name
        }
    

class Movie(db.Model):
    
    __tablename__ = 'movie'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    length = db.Column(db.Integer)
    vote = db.relationship('Vote', backref='movie')

    
    def __init__(self, title, length):
        self.title = title
        self.length = length
    
    def __repr__(self):
        return '<Title %r>' % self.title
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'length': self.length,
            'votes': [vote.person.name for vote in self.vote]
        }
 
    
class Vote(db.Model):
    
    __tablename__ = 'votes'
    
    person = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    movie = db.Column(db.Integer, db.ForeignKey('movie.id'))
    
    def __init__(self, person, movie):
        self.person = person
        self.movie = movie
    
    
db.create_all()

"""URL routing for catalyst_exercise
"""
@app.route('/movies', methods = ['GET'])
def get_movies():
    return jsonify({'movies': Movie.query.all()})
    
@app.route('/Person', methods = ['GET'])
def get_Person():
    return jsonify({'Person': Person.query.all()})

@app.route('/votes', methods = ['GET'])
def get_votes():
    return jsonify({'votes': Vote.query.all()})


@app.route('/vote/<int:person_id>/<int:movie>', methods = ['POST'])
def vote():
    vote = Vote(request.json.person_id, request.json.movie)

    db.session.add(vote)
    db.session.commit()
    return jsonify({'vote': vote})
    
    
@app.route('/Person/<int:person_id>/votes', methods = ['DELETE'])
def delete_person_votes(): #check this function
    votes = Person.query.filter(id=vote.id).all()
    votes.delete()
    db.session.commit()
  
@app.route('/votes', methods = ['DELETE'])
def delete_all_votes(): #check this function
    Vote.query.all.delete()
    db.session.commit()


"""Run server
"""
if __name__ == '__main__':
    app.run(debug=True)