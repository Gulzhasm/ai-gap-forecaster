import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(basedir, "instance", "gap_forecaster.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Finnhub
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')
    FINNHUB_CALLS_PER_MINUTE = 60
    FINNHUB_CACHE_TTL = 300  # seconds

    # Interactive Brokers
    IB_HOST = os.getenv('IB_HOST', '127.0.0.1')
    IB_PORT = int(os.getenv('IB_PORT', '7497'))  # 7497=TWS paper, 4002=Gateway paper
    IB_CLIENT_ID = int(os.getenv('IB_CLIENT_ID', '1'))
    IB_TRADING_MODE = os.getenv('IB_TRADING_MODE', 'paper')  # 'paper' or 'live'

    # Risk Management
    RISK_MAX_POSITION_PCT = float(os.getenv('RISK_MAX_POSITION_PCT', '5.0'))
    RISK_MAX_DAILY_LOSS = float(os.getenv('RISK_MAX_DAILY_LOSS', '500.0'))
    RISK_DEFAULT_RISK_PCT = float(os.getenv('RISK_DEFAULT_RISK_PCT', '1.0'))


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
