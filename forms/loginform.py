from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], _name='username')
    password = PasswordField('Пароль', validators=[DataRequired()], _name='password')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
