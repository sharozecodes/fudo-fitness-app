#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import *


# Views go here!
class Signup(Resource):
    def post(self):
        
        json = request.get_json()
        if 'username' in json and 'password' in json and 'name' in json and 'date_of_birth' in json and 'weight' in json and 'height' in json:
            user = User(
                username=json['username'],
                name=json['name'],
                date_of_birth=json['date_of_birth'],
                weight=json['weight'],
                height=json['height'],
                    
            )
            user.password_hash = json['password']
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id

            return user.to_dict(), 201
        else:
            return {'error': 'unprocessable entity'}, 422
        
class CheckSession(Resource):
    def get(self):
        if session.get('user_id') == None:
            return {'error': 'Unauthorized'}, 401
        else:
            user = User.query.filter_by(id=session.get('user_id')).first()
            return user.to_dict(), 200
        
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        user = User.query.filter_by(username=username).first()
        password = request.get_json()['password']

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'error': 'Invalid username/password'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        else:
            return {'error':'unauthorized'}, 401
        
class RecipeIndex(Resource):
    def get(self):
        recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
        return recipes, 200

class WorkoutIndex(Resource):
    def get(self):
        workouts = [workout.to_dict() for workout in Workout.query.all()]
        return workouts, 200
    
class UserWorkouts(Resource):
    def get(self):
        if session.get('user_id') == None:
            return {'errors': 'unauthorized'}, 401
        else:
            recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
            return recipes, 200
    
@app.route('/')
def index():
    return '<h1>Project Server</h1>'

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')
api.add_resource(WorkoutIndex, '/workouts', endpoint='workouts')
api.add_resource(WorkoutIndex, '/user/<id:int>/workouts', endpoint='workouts_by_user')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

