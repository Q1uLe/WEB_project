from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewRecipeForm(FlaskForm):
    recipe_name = StringField('Название рецепта', validators=[DataRequired()])
    recipe = TextAreaField("Введите рецепт", validators=[DataRequired()])
    ingredients = TextAreaField("Введите ингредиенты", validators=[DataRequired()])
    submit = SubmitField('Отправить')
