from flask import Flask, jsonify, abort, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__) #instantiates our app
app.config.from_pyfile('config.py') #config loaded into app
db = SQLAlchemy(app) #create database by instantiating an SQLAlchemy instance 


class User(db.Model):
       
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    
    def __repr__(self):
        return '<User %r>' % (self.name)
    

class Movie(db.Model):
    
    __tablename__ = 'movies'
    
    id = db.Columns(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    length = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Title %r>' % self.title
    
class Vote(db.Model):
    
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))