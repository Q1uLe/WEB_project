from data import db_session


from flask import Flask, render_template
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


if __name__ == '__main__':
    db_session.global_init("db/recipes.db")
    app.run()
