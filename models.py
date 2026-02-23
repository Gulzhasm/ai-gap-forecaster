from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    added_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    notes = db.Column(db.Text, nullable=True)
    target_price = db.Column(db.Float, nullable=True)
    sector = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'added_date': self.added_date.isoformat(),
            'notes': self.notes,
            'target_price': self.target_price,
            'sector': self.sector,
            'is_active': self.is_active
        }


class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # long / short
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    exit_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), nullable=False, default='open')  # open / closed / cancelled
    pnl = db.Column(db.Float, nullable=True)
    pnl_percent = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    gap_type = db.Column(db.String(10), nullable=False)  # gap_up / gap_down
    gap_percent = db.Column(db.Float, nullable=True)
    setup_rating = db.Column(db.Integer, nullable=True)  # 1-5

    # Phase 1: IB + Catalyst fields
    ib_order_id = db.Column(db.Integer, nullable=True)
    catalyst_id = db.Column(db.Integer, db.ForeignKey('catalysts.id'), nullable=True)
    catalyst_type = db.Column(db.String(30), nullable=True)
    stop_loss = db.Column(db.Float, nullable=True)
    take_profit = db.Column(db.Float, nullable=True)
    source = db.Column(db.String(10), nullable=False, default='manual')  # manual / ib
    trading_mode = db.Column(db.String(5), nullable=False, default='paper')  # paper / live

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'direction': self.direction,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'quantity': self.quantity,
            'entry_date': self.entry_date.isoformat(),
            'exit_date': self.exit_date.isoformat() if self.exit_date else None,
            'status': self.status,
            'pnl': self.pnl,
            'pnl_percent': self.pnl_percent,
            'notes': self.notes,
            'gap_type': self.gap_type,
            'gap_percent': self.gap_percent,
            'setup_rating': self.setup_rating,
            'ib_order_id': self.ib_order_id,
            'catalyst_id': self.catalyst_id,
            'catalyst_type': self.catalyst_type,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'source': self.source,
            'trading_mode': self.trading_mode,
        }


class Catalyst(db.Model):
    __tablename__ = 'catalysts'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, index=True)
    catalyst_type = db.Column(db.String(30), nullable=False)
    headline = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(50), nullable=True)  # finnhub_news, finnhub_earnings, finnhub_filings
    sentiment_score = db.Column(db.Float, nullable=True)  # -1.0 to 1.0
    detected_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    event_date = db.Column(db.DateTime, nullable=True)
    raw_data = db.Column(db.Text, nullable=True)  # JSON blob
    catalyst_score = db.Column(db.Float, nullable=True)  # 0-100

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'catalyst_type': self.catalyst_type,
            'headline': self.headline,
            'source': self.source,
            'sentiment_score': self.sentiment_score,
            'detected_date': self.detected_date.isoformat(),
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'catalyst_score': self.catalyst_score,
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    ib_order_id = db.Column(db.Integer, nullable=True, unique=True)
    ib_trade_id = db.Column(db.Integer, nullable=True)
    symbol = db.Column(db.String(10), nullable=False)
    action = db.Column(db.String(4), nullable=False)  # BUY / SELL
    order_type = db.Column(db.String(10), nullable=False)  # MKT / LMT / STP
    quantity = db.Column(db.Integer, nullable=False)
    limit_price = db.Column(db.Float, nullable=True)
    stop_price = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    fill_price = db.Column(db.Float, nullable=True)
    fill_quantity = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True)
    trading_mode = db.Column(db.String(5), nullable=False, default='paper')
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ib_order_id': self.ib_order_id,
            'ib_trade_id': self.ib_trade_id,
            'symbol': self.symbol,
            'action': self.action,
            'order_type': self.order_type,
            'quantity': self.quantity,
            'limit_price': self.limit_price,
            'stop_price': self.stop_price,
            'status': self.status,
            'fill_price': self.fill_price,
            'fill_quantity': self.fill_quantity,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'trading_mode': self.trading_mode,
            'notes': self.notes,
        }


class RiskConfig(db.Model):
    __tablename__ = 'risk_config'

    id = db.Column(db.Integer, primary_key=True)
    max_position_pct = db.Column(db.Float, nullable=False, default=5.0)
    max_daily_loss = db.Column(db.Float, nullable=False, default=500.0)
    default_risk_pct = db.Column(db.Float, nullable=False, default=1.0)
    max_open_positions = db.Column(db.Integer, nullable=False, default=5)
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'max_position_pct': self.max_position_pct,
            'max_daily_loss': self.max_daily_loss,
            'default_risk_pct': self.default_risk_pct,
            'max_open_positions': self.max_open_positions,
            'updated_at': self.updated_at.isoformat(),
        }
