import os
from flask import Flask
from dotenv import load_dotenv
from config import config
from models import db

load_dotenv()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

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
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
