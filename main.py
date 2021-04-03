from data import db_session
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from data.User import User
from data.Recipes import Recipes

from flask import Flask, render_template, redirect, request

# from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/')
@app.route('/recipes')
@app.route('/recipes/<page>')
@app.route('/recipes/<page>/<request>')
def index(page='', request=''):
    param = {'page': page, 'request': request}
    return render_template('index.html', **param)


@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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


if __name__ == '__main__':
    db_session.global_init("db/recipes.db")
    app.run()
