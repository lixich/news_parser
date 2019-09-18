from .news import app_url as news_url
from .news import app_url as error_url
from .error import generate_error


def register_blueprints(app):
    app.register_blueprint(news_url, url_prefix='/posts')

    @app.errorhandler(404)
    def not_found(error):
        return generate_error(404)

