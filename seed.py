"""Seed the database with sample trade data for demo/testing."""
from datetime import datetime, timedelta, timezone
from app import create_app
from models import db, Watchlist, Trade

app = create_app()

SAMPLE_WATCHLIST = [
    {'symbol': 'AAPL', 'target_price': 195.00, 'sector': 'Technology', 'notes': 'Watch for gap fill on earnings'},
    {'symbol': 'TSLA', 'target_price': 260.00, 'sector': 'Consumer Cyclical', 'notes': 'High volatility gap candidate'},
    {'symbol': 'NVDA', 'target_price': 850.00, 'sector': 'Technology', 'notes': 'AI momentum plays'},
    {'symbol': 'META', 'target_price': 520.00, 'sector': 'Technology', 'notes': 'Strong support at 500'},
    {'symbol': 'JPM', 'target_price': 200.00, 'sector': 'Financial', 'notes': 'Banking sector gap play'},
]

SAMPLE_TRADES = [
    # Closed winners
    {'symbol': 'AAPL', 'direction': 'long', 'entry_price': 185.50, 'exit_price': 192.00, 'quantity': 100,
     'gap_type': 'gap_up', 'gap_percent': 2.5, 'setup_rating': 4, 'notes': 'Earnings gap, held overnight',
     'days_ago_entry': 25, 'days_ago_exit': 24},
    {'symbol': 'NVDA', 'direction': 'long', 'entry_price': 790.00, 'exit_price': 830.00, 'quantity': 20,
     'gap_type': 'gap_up', 'gap_percent': 4.1, 'setup_rating': 5, 'notes': 'AI news catalyst',
     'days_ago_entry': 20, 'days_ago_exit': 19},
    {'symbol': 'TSLA', 'direction': 'short', 'entry_price': 255.00, 'exit_price': 242.00, 'quantity': 50,
     'gap_type': 'gap_down', 'gap_percent': -3.2, 'setup_rating': 3, 'notes': 'Delivery miss gap down',
     'days_ago_entry': 15, 'days_ago_exit': 14},
    {'symbol': 'META', 'direction': 'long', 'entry_price': 505.00, 'exit_price': 518.00, 'quantity': 30,
     'gap_type': 'gap_up', 'gap_percent': 1.8, 'setup_rating': 4, 'notes': 'Ad revenue beat',
     'days_ago_entry': 10, 'days_ago_exit': 9},
    {'symbol': 'AMD', 'direction': 'long', 'entry_price': 165.00, 'exit_price': 175.00, 'quantity': 60,
     'gap_type': 'gap_up', 'gap_percent': 3.5, 'setup_rating': 4, 'notes': 'Data center demand',
     'days_ago_entry': 7, 'days_ago_exit': 6},
    # Closed losers
    {'symbol': 'JPM', 'direction': 'long', 'entry_price': 198.00, 'exit_price': 192.00, 'quantity': 40,
     'gap_type': 'gap_up', 'gap_percent': 2.1, 'setup_rating': 2, 'notes': 'False breakout, gap filled against',
     'days_ago_entry': 18, 'days_ago_exit': 17},
    {'symbol': 'BA', 'direction': 'short', 'entry_price': 180.00, 'exit_price': 188.00, 'quantity': 30,
     'gap_type': 'gap_down', 'gap_percent': -2.8, 'setup_rating': 2, 'notes': 'Bounced hard, stopped out',
     'days_ago_entry': 12, 'days_ago_exit': 11},
    # Open trades
    {'symbol': 'GOOGL', 'direction': 'long', 'entry_price': 175.00, 'exit_price': None, 'quantity': 50,
     'gap_type': 'gap_up', 'gap_percent': 2.2, 'setup_rating': 4, 'notes': 'Cloud growth story',
     'days_ago_entry': 2, 'days_ago_exit': None},
    {'symbol': 'CRM', 'direction': 'long', 'entry_price': 290.00, 'exit_price': None, 'quantity': 25,
     'gap_type': 'gap_up', 'gap_percent': 3.0, 'setup_rating': 3, 'notes': 'Enterprise AI momentum',
     'days_ago_entry': 1, 'days_ago_exit': None},
]


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seed watchlist
        for w in SAMPLE_WATCHLIST:
            db.session.add(Watchlist(**w))

        # Seed trades
        now = datetime.now(timezone.utc)
        for t in SAMPLE_TRADES:
            entry_date = now - timedelta(days=t['days_ago_entry'])
            exit_date = (now - timedelta(days=t['days_ago_exit'])) if t['days_ago_exit'] else None

            trade = Trade(
                symbol=t['symbol'],
                direction=t['direction'],
                entry_price=t['entry_price'],
                exit_price=t['exit_price'],
                quantity=t['quantity'],
                entry_date=entry_date,
                exit_date=exit_date,
                gap_type=t['gap_type'],
                gap_percent=t['gap_percent'],
                setup_rating=t['setup_rating'],
                notes=t['notes'],
                status='closed' if t['exit_price'] else 'open'
            )

            # Compute P&L for closed trades
            if trade.status == 'closed':
                from services.trade_service import compute_pnl
                trade.pnl, trade.pnl_percent = compute_pnl(
                    trade.direction, trade.entry_price, trade.exit_price, trade.quantity
                )

            db.session.add(trade)

        db.session.commit()
        print(f'Seeded {len(SAMPLE_WATCHLIST)} watchlist items and {len(SAMPLE_TRADES)} trades')


if __name__ == '__main__':
    seed()
