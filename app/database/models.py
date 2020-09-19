from app.database import db


class LikedRecipes(db.Model):
    __tablename__ = 'liked_recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False, unique=True)


class DislikedRecipes(db.Model):
    __tablename__ = 'disliked_recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False, unique=True)
