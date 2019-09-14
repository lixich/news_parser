from .news import app_url as news_url


def register_blueprints(app):
    app.register_blueprint(news_url, url_prefix='/posts')
