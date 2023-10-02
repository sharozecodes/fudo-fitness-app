#!/usr/bin/env python3

# Standard library imports
from random import randint, choice


# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import *

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Deleting all records...")
        Recipe.query.delete()
        User.query.delete()
        Workout.query.delete()
        WorkoutPreference.query.delete()
        RecipePreference.query.delete()

        print("Creating new users...")
        for i in range(20):
            
            username = fake.user_name()
            name = fake.name()
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
            weight = randint(80,500)
            height = randint(60, 272)

            user = User(username=username, name=name, date_of_birth=date_of_birth, weight=weight, height=height)
            user.password_hash = user.username + 'password'
            db.session.add(user)

        db.session.commit()

        print("Creating new workouts...")
            
        workout_types = ['Calisthenics','Cardio', 'Strength', 'Yoga', 'Pilates']
    
        for _ in range(20):
            title = fake.catch_phrase()
            category = choice(workout_types)
            instructions = fake.paragraph()
            duration = randint(15, 120)
            calories_burnt = randint(50, 500)
            image_url = fake.image_url()
            
            workout = Workout(title=title, category=category, instructions=instructions, duration=duration, calories_burnt=calories_burnt, image_url=image_url)
            db.session.add(workout)
        
        db.session.commit()



