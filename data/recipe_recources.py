from flask_restful import Resource
from data import db_session
from data.Recipes import Recipes
from flask import jsonify
from flask_restful import abort


class RecipeResource(Resource):
    def get(self, recipe_id):
        session = db_session.create_session()
        recipe = session.query(Recipes).get(recipe_id)
        if not recipe:
            return jsonify({
                'error': 404,
                'message': f"Recipe {recipe_id} not found"
            })
        return jsonify({'recipes': recipe.to_dict(
            only=('title', 'ingredients', 'recipe', 'user_id'))})


class RecipeListResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipe = session.query(Recipes).all()
        return jsonify({'recipes': [item.to_dict(
            only=('title', 'ingredients', 'recipe', 'user.name')) for item in recipe]})
