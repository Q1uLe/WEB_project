from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NewRecipeForm(FlaskForm):
    recipe_name = StringField('Название рецепта', validators=[DataRequired(), Length(max=100)])
    recipe = TextAreaField("Введите рецепт", validators=[DataRequired(), Length(max=1500)])
    ingredients = TextAreaField("Введите ингредиенты", validators=[DataRequired(), Length(max=1500)])
    submit = SubmitField('Отправить')
