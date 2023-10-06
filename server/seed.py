#!/usr/bin/env python3

# Standard library imports
from random import randint, choice, sample


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
            
        workouts = [
            {
                "title": "Morning Yoga",
                "category": "Yoga",
                "instructions": "Start your day with a relaxing yoga session.",
                "duration": 30,
                "calories_burnt": 150,
                "image_url": "https://example.com/yoga.jpg"
            },
            {
                "title": "High-Intensity Interval Training",
                "category": "HIIT",
                "instructions": "A challenging HIIT workout for fat burning.",
                "duration": 20,
                "calories_burnt": 300,
                "image_url": "https://example.com/hiit.jpg"
            },
            # Add more workout entries here...
        ]
        for data in workouts:  # Adjust the range if you have more sample data
            workout = Workout(
                title=data["title"],
                category=data["category"],
                instructions=data["instructions"],
                duration=data["duration"],
                calories_burnt=data["calories_burnt"],
                image_url=data["image_url"]
            )
            db.session.add(workout)
        
        db.session.commit()

        print("Creating new recipes...")

        recipe_categories = ['Vegan', 'Keto', 'High-Protein', 'Mediterranean', 'Low-Carb', 'Gluten-Free', 'Paleo', 'Vegetarian', 'Low-Fat', 'Dessert']

        for _ in range(20):
            title = fake.catch_phrase()
            category = choice(recipe_categories)
            instructions = fake.paragraphs(nb=randint(3, 6))
            prep_time = randint(10, 120)
            calories = randint(100, 800)
            protein = randint(5, 50)

            
            recipe = Recipe(title=title, category=category, instructions='\n'.join(instructions), prep_time=prep_time, calories=calories, protein=protein)
            db.session.add(recipe)
        
        db.session.commit()

        print("Creating relationships...")
        users = User.query.all()
        workouts = Workout.query.all()
        recipes = Recipe.query.all()
        
        for user in users:
            num_workout_prefs = randint(1, len(workouts))
            num_recipe_prefs = randint(1, len(recipes))
            
            user_workout_prefs = sample(workouts, num_workout_prefs)
            user_recipe_prefs = sample(recipes, num_recipe_prefs)
            
            for workout in user_workout_prefs:
                workout_pref = WorkoutPreference(user_id=user.id, workout_id=workout.id)
                db.session.add(workout_pref)
            
            for recipe in user_recipe_prefs:
                recipe_pref = RecipePreference(user_id=user.id, recipe_id=recipe.id)
                db.session.add(recipe_pref)
        
        db.session.commit()



