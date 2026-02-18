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
            'setup_rating': self.setup_rating
        }
