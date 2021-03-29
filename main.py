from data import db_session


from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('main_page.html')


if __name__ == '__main__':
    db_session.global_init("db/recipes.db")
    app.run()
