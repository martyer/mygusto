from app.database import db


class LikedRecipes(db.Model):
    __tablename__ = 'liked_recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False, unique=True)


class FeatureVectors(db.Model):
    __tablename__ = 'feature_vectors'

    id = db.Column(db.Integer, primary_key=True)
    features = db.Column(db.String, nullable=False)
    sentiment = db.Column(db.String, nullable=False)


class DislikedRecipes(db.Model):
    __tablename__ = 'disliked_recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False, unique=True)


class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False, unique=True)
