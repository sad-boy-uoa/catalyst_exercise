from flask import Flask, jsonify, abort, request
from sqlalchemy.orm import relationship
from flask.ext.sqlalchemy import SQLAlchemy


#TODO The constraint on Person voting on only one movie once 
#error message if someone has already voted

"""
instantiates the app, loads config and creates database
"""
app = Flask(__name__) 
app.config.from_pyfile('Config.py') 
db = SQLAlchemy(app) 


"""
Database models for catalyst_exercise
"""
class Person(db.Model):
       
    __tablename__ = 'person' 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    votes = db.relationship('Vote', backref='person')
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):        
        return '<Person %r>' % (self.name)
    

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
 
    
class Vote(db.Model):
    
    __tablename__ = 'votes'
    
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    
    def __init__(self, user_id, movie_id): #something like this maybe
        self.user_id = user_id
        self.movie_id = movie_id
    #where the fuck do i do the constraint for voting uniqueness
    
db.create_all()


"""
URL routing for catalyst_exercise
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


@app.route('/vote/<int:person_id>/<int:movie_id>', methods = ['POST'])
def vote():
    vote = Vote(request.json.person_id, request.json.movie_id)

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


"""
Run server
"""
if __name__ == '__main__':
    app.run()