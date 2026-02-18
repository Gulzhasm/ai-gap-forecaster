from datetime import datetime, timedelta, timezone
from collections import defaultdict
from models import Trade


def get_summary() -> dict:
    """Calculate overall trading performance summary."""
    trades = Trade.query.all()
    closed = [t for t in trades if t.status == 'closed']
    open_trades = [t for t in trades if t.status == 'open']

    if not closed:
        return {
            'total_trades': len(trades),
            'open_trades': len(open_trades),
            'closed_trades': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_pnl': 0,
            'best_trade': 0,
            'worst_trade': 0,
            'avg_winner': 0,
            'avg_loser': 0,
            'profit_factor': 0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0
        }

    winners = [t for t in closed if t.pnl and t.pnl > 0]
    losers = [t for t in closed if t.pnl and t.pnl < 0]
    pnls = [t.pnl for t in closed if t.pnl is not None]

    total_pnl = sum(pnls)
    total_wins = sum(t.pnl for t in winners)
    total_losses = abs(sum(t.pnl for t in losers)) if losers else 0

    # Consecutive wins/losses
    sorted_closed = sorted(closed, key=lambda t: t.exit_date or t.entry_date)
    max_wins, max_losses, cur_wins, cur_losses = 0, 0, 0, 0
    for t in sorted_closed:
        if t.pnl and t.pnl > 0:
            cur_wins += 1
            cur_losses = 0
            max_wins = max(max_wins, cur_wins)
        elif t.pnl and t.pnl < 0:
            cur_losses += 1
            cur_wins = 0
            max_losses = max(max_losses, cur_losses)

    return {
        'total_trades': len(trades),
        'open_trades': len(open_trades),
        'closed_trades': len(closed),
        'win_rate': round(len(winners) / len(closed) * 100, 1) if closed else 0,
        'total_pnl': round(total_pnl, 2),
        'avg_pnl': round(total_pnl / len(closed), 2) if closed else 0,
        'best_trade': round(max(pnls), 2) if pnls else 0,
        'worst_trade': round(min(pnls), 2) if pnls else 0,
        'avg_winner': round(total_wins / len(winners), 2) if winners else 0,
        'avg_loser': round(-total_losses / len(losers), 2) if losers else 0,
        'profit_factor': round(total_wins / total_losses, 2) if total_losses > 0 else 0,
        'max_consecutive_wins': max_wins,
        'max_consecutive_losses': max_losses
    }


def get_pnl_series(period: str = 'daily', days: int = 30) -> dict:
    """Get P&L time series for charting."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    closed = Trade.query.filter(
        Trade.status == 'closed',
        Trade.exit_date >= cutoff
    ).order_by(Trade.exit_date).all()

    # Group by date
    daily_pnl = defaultdict(float)
    for t in closed:
        if t.exit_date and t.pnl is not None:
            date_key = t.exit_date.strftime('%Y-%m-%d')
            daily_pnl[date_key] += t.pnl

    # Build series with all dates
    labels = []
    daily_values = []
    cumulative = []
    running_total = 0

    current = cutoff.date()
    end = datetime.now(timezone.utc).date()
    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        pnl = round(daily_pnl.get(date_str, 0), 2)
        running_total = round(running_total + pnl, 2)

        labels.append(date_str)
        daily_values.append(pnl)
        cumulative.append(running_total)
        current += timedelta(days=1)

    return {
        'labels': labels,
        'cumulative_pnl': cumulative,
        'daily_pnl': daily_values
    }


def get_by_gap_type() -> dict:
    """Get performance breakdown by gap type."""
    result = {}
    for gap_type in ('gap_up', 'gap_down'):
        closed = Trade.query.filter_by(status='closed', gap_type=gap_type).all()
        if not closed:
            result[gap_type] = {'count': 0, 'win_rate': 0, 'avg_pnl': 0, 'total_pnl': 0}
            continue

        winners = [t for t in closed if t.pnl and t.pnl > 0]
        pnls = [t.pnl for t in closed if t.pnl is not None]

        result[gap_type] = {
            'count': len(closed),
            'win_rate': round(len(winners) / len(closed) * 100, 1),
            'avg_pnl': round(sum(pnls) / len(pnls), 2) if pnls else 0,
            'total_pnl': round(sum(pnls), 2) if pnls else 0
        }

    return result
