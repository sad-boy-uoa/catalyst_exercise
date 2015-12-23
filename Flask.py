from flask import Flask, jsonify, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

#TODO The constraint on people voting on only one movie once 

"""
instantiates the app, loads config and creates database
"""
app = Flask(__name__) 
app.config.from_pyfile('config.py') 
db = SQLAlchemy(app) 


"""
Classes for the database
"""
class People(db.Model):
       
    __tablename__ = 'people' 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):        
        return '<People %r>' % (self.name)
    

class Movie(db.Model):
    
    __tablename__ = 'movies'
    
    id = db.Columns(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    length = db.Column(db.Integer)
    
    def __init__(self, title, length):
        self.title = title
        self.length = length
    
    def __repr__(self):
        return '<Title %r>' % self.title
 
    
class Vote(db.Model):
    
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    #TODO figure out how to do init for a vote
    
    def __init__(self, user_id, movie_id): #something like this maybe
        self.user_id = user_id
        self.movie_id = movie_id
    #where the fuck do i do the constraint for voting uniqueness
    
   
db.createAll()


"""
Handles requests for GET
"""
@app.route('/movies', methods = ['GET'])
def get_movies():
    return jsonify({'movies': Movie.query.all()})
    
@app.route('/people', methods = ['GET'])
def get_people():
    return jsonify({'people': People.query.all()})

@app.route('/votes', methods = ['GET'])
def get_votes():
    return jsonify({'votes': Vote.query.all()})


"""
Handles requests for POST
"""
@app.route('s/vote/<int:person_id>/<int:movie_id>', methods = ['POST'])
def vote():
    if request.json or not 'person_id' in request.json: #check this if statment
        abort(400)
       
    vote = Vote(request.json.person_id, request.json.movie_id)

    db.session.add(vote)
    db.session.commit()
    return jsonify({'vote': vote}), 201
    
    
"""
Handles requests for DELETE
"""
# DELETE /people/<int:person_id>/votes
#     - delete all votes for a given person ID.
# 
# DELETE /votes
#     - delete all votes.  







