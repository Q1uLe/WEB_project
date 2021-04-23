from data import db_session, rec_api
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.newrecipeform import NewRecipeForm
from data.User import User
from data.Recipes import Recipes
from data import recipe_recources

from flask_restful import Api

import logging

from flask import Flask, render_template, redirect, request, url_for, make_response, jsonify

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['JSON_AS_ASCII'] = False

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(filename='example.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/')
def just_slash():
    return redirect('/recipes')


# Главная страница
@app.route('/recipes', methods=['GET', 'POST'])
@app.route('/recipes/', methods=['GET', 'POST'])
@app.route('/recipes/<page>', methods=['GET', 'POST'])
@app.route('/recipes/<page>/', methods=['GET', 'POST'])
@app.route('/recipes/<page>/<page_request>', methods=['GET', 'POST'])
def index(page=0, page_request=''):
    param = {}
    if current_user.is_authenticated:
        param['user_name'] = current_user.name
    if request.method == 'POST':
        empty_string = request.form['request-text-area']
        return redirect(url_for('submit', req=empty_string, page=page))
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipes).filter(Recipes.title.like(f'%{page_request}%'))
    page_count = recipes.count() / 10
    if int(page) > page_count or int(page) < 0 or recipes.count() == 0:
        return redirect('/page_not_found')
    recipes = recipes.limit(10)
    recipes = recipes.offset(int(page) * 10)
    recipes = recipes.all()
    param['recipes'] = recipes
    param['counter'] = 0
    param['page'] = int(page)
    param['page_count'] = page_count
    return render_template('index.html', **param)


@app.route('/recipes/<page>/<req>', methods=['POST'])
def submit(page=0, req=''):
    return redirect(f'/recipes/0/{req}')


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
        return redirect('/recipes')
    param = {}
    if current_user.is_authenticated:
        param['user_name'] = current_user.name
    db_sess = db_session.create_session()
    recipe_obj = db_sess.query(Recipes).filter(Recipes.id.like(recipe_id)).first()
    param['recipe_name'] = recipe_obj.title
    param['ingredients'] = recipe_obj.ingredients
    param['recipe'] = recipe_obj.recipe
    return render_template('recipe.html', **param)


@app.route('/login', methods=['GET', 'POST'])
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


@app.errorhandler(404)
def error_404():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/page_not_found')
def page_not_found():
    return render_template('page_not_found.html')


if __name__ == '__main__':
    db_session.global_init("db/recipes.db")
    api.add_resource(recipe_recources.RecipeListResource, '/api/recipe')
    api.add_resource(recipe_recources.RecipeResource, '/api/recipe/<recipe_id>')
    app.run()
