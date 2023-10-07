from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ("-recipe_preferences","-workout_preferences",)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    name = db.Column(db.String(255), nullable=False)


    workout_preferences = db.relationship('WorkoutPreference', backref='user', cascade="all, delete-orphan")
    recipe_preferences = db.relationship('RecipePreference', backref='user', cascade="all, delete-orphan")


    @hybrid_property
    def password_hash(self):
        raise AttributeError('Forbidden')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )
    

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    serialize_rules = ("-recipe_preference",)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

class Workout(db.Model, SerializerMixin):
    __tablename__ = 'workouts'
    serialize_rules = ("-workout_preference",)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    duration = db.Column(db.Integer, nullable=False)
    calories_burnt = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

class WorkoutPreference(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    workout = db.relationship('Workout', backref='workout_preference')

class RecipePreference(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe = db.relationship('Recipe', backref='recipe_preference')