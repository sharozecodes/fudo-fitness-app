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
        
        if 'username' in json and 'password' in json and 'name' in json:
            username=json['username']
            user_check = User.query.filter_by(username=username).first()
            if not user_check:
                user = User(
                    username=username,
                    name=json['name'],
                )
                user.password_hash = json['password']
                db.session.add(user)
                db.session.commit()
                session['user_id'] = user.id
                return user.to_dict(), 201
            else:
                return {'error': 'user already exists'}, 208
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
        
class UserProfile(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            print(user)
            return user.to_dict(), 200
        else:
            return {'error': 'User not found'}, 404

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {}, 204
        else:
            return {'error': 'User not found'}, 404
        
        
class RecipeIndex(Resource):
    def get(self):
        recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
        return recipes, 200

class WorkoutIndex(Resource):
    def get(self):
        workouts = [workout.to_dict() for workout in Workout.query.all()]
        return workouts, 200
    
class UserWorkouts(Resource):
    def get(self, id):
        workout_prefs = WorkoutPreference.query.filter_by(user_id=id).all()
        if workout_prefs:
            workouts = [workout_pref.workout.to_dict() for workout_pref in workout_prefs]
            return workouts, 200
        else:
            return {'error': 'User not found'}, 404
    
    def post(self, id):
        json = request.get_json()
        workout_id = json['workout_id']
        user = User.query.filter_by(id=id).first()
        workout = Workout.query.filter_by(id=workout_id).first()

        if user and workout:
            workout_preference = WorkoutPreference.query.filter_by(user_id=id, workout_id=workout_id).first()
            if not workout_preference:
                workout_pref = WorkoutPreference(user_id = id, workout_id= workout_id)
                db.session.add(workout_pref)
                db.session.commit()
                return workout_pref.workout.to_dict(), 201
            else:
                return {'error': 'preference already exists'}, 208
        else:
            return {'error': 'Invalid user_id/workout_id'}, 401
    
class UserRecipes(Resource):   
    def get(self, id):
        recipe_prefs = RecipePreference.query.filter_by(user_id=id).all()
        if recipe_prefs:
            recipes = [recipe_pref.recipe.to_dict() for recipe_pref in recipe_prefs]
            return recipes, 200
        else:
            return {'error': 'User not found'}, 404
        
    def post(self, id):
        json = request.get_json()
        recipe_id = json['recipe_id']
        user = User.query.filter_by(id=id).first()
        recipe = Recipe.query.filter_by(id=recipe_id).first()

        if user and recipe:
            recipe_preference = RecipePreference.query.filter_by(user_id=id, recipe_id=recipe_id).first()
            if not recipe_preference:
                recipe_pref = RecipePreference(user_id = id, recipe_id= recipe_id)
                db.session.add(recipe_pref)
                db.session.commit()
                return recipe_pref.recipe.to_dict(), 201
            else:
                return {'error': 'preference already exists'}, 208
        else:
            return {'error': 'Invalid user_id/recipe_id'}, 401
        
class WorkoutById(Resource):   
    def get(self, id):
        workout = Workout.query.filter_by(id=id).first()
        if workout:
            return workout.to_dict(), 200
        else:
            return {'error': 'Workout not found'}, 404
        
class RecipeById(Resource):   
    def get(self, id):
        recipe = Recipe.query.filter_by(id=id).first()
        if recipe:
            return recipe.to_dict(), 200
        else:
            return {'error': 'Recipe not found'}, 404
    

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')
api.add_resource(WorkoutIndex, '/workouts', endpoint='workouts')
api.add_resource(WorkoutById, '/workouts/<int:id>', endpoint='workout_by_id')
api.add_resource(RecipeById, '/recipes/<int:id>', endpoint='recipe_by_id')
api.add_resource(UserWorkouts, '/users/<int:id>/workouts', endpoint='workouts_by_user')
api.add_resource(UserRecipes, '/users/<int:id>/recipes', endpoint='recipes_by_user')
api.add_resource(UserProfile, '/users/<int:id>', endpoint='user_profile')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

