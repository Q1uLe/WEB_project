import flask

from . import db_session
from .Recipes import Recipes

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/recipes')
def get_news():
    return "Обработчик в news_api"
