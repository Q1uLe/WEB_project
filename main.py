from data import db_session
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.newrecipeform import NewRecipeForm
from data.User import User
from data.Recipes import Recipes

import logging

from flask import Flask, render_template, redirect, g

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)
#

logging.basicConfig(filename='example.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/')
@app.route('/recipes')
@app.route('/recipes/<page>')
@app.route('/recipes/<page>/<request>')
def index(page='', request=''):
    param = {}
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipes).filter(Recipes.title.like(f'%{request}%'))
    recipes = recipes.limit(10)
    if page.isdigit():
        recipes = recipes.offset(int(page) * 10)
    recipes = recipes.all()
    print(recipes)
    if current_user.is_authenticated:
        param['user_name'] = current_user.name
    param['recipes'] = recipes
    # param['counter'] = 0
    return render_template('index.html', **param)


@app.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():
    if current_user.is_authenticated:
        form = NewRecipeForm()
        if form.validate_on_submit():
            if current_user.is_authenticated:
                db_sess = db_session.create_session()
                recipe_obj = Recipes()
                recipe_obj.title = form.recipe_name.data
                recipe_obj.recipe = form.recipe.data
                recipe_obj.ingredients = form.ingredients.data
                recipe_obj.user_id = db_sess.query(User).filter(User.name == current_user.name).first().id
                db_sess.add(recipe_obj)
                db_sess.commit()
                return redirect('/')
        return render_template('new_recipe.html', user_name=current_user.name, form=form)
    return redirect('/login')


@app.route('/recipe', methods=['GET', 'POST'])
@app.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id=''):
    if recipe_id == '':
        return redirect('/')
    return render_template('recipe.html')


@app.route('/login', methods=['GET', 'POST'])
# @app.after_request
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.username.data).first()
        logging.info(f'User.name: {User.name}; form.username.data: {form.username.data}')
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/recipes.db")
    app.run()
