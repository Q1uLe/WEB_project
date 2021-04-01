import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Recipes(SqlAlchemyBase):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    recipe_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    recipe = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ingredients = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture_directory = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
