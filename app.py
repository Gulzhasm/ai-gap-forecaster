import os
from flask import Flask
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config
from models import db

load_dotenv()


class PrefixMiddleware:
    """Middleware that sets SCRIPT_NAME for subpath deployments."""

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if self.prefix:
            environ['SCRIPT_NAME'] = self.prefix
            path_info = environ.get('PATH_INFO', '')
            if path_info.startswith(self.prefix):
                environ['PATH_INFO'] = path_info[len(self.prefix):]
        return self.app(environ, start_response)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Trust proxy headers from Vercel/Render
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Apply subpath prefix for production
    url_prefix = os.getenv('URL_PREFIX', '')
    if url_prefix:
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=url_prefix)

    db.init_app(app)

    # Register blueprints
    from routes.views import views
    from routes.api_scanner import api_scanner
    from routes.api_watchlist import api_watchlist
    from routes.api_trades import api_trades
    from routes.api_stats import api_stats

    app.register_blueprint(views)
    app.register_blueprint(api_scanner, url_prefix='/api/scanner')
    app.register_blueprint(api_watchlist, url_prefix='/api/watchlist')
    app.register_blueprint(api_trades, url_prefix='/api/trades')
    app.register_blueprint(api_stats, url_prefix='/api/stats')

    with app.app_context():
        # Ensure instance directory exists for SQLite
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
