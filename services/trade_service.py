from datetime import datetime, timezone


def compute_pnl(direction: str, entry_price: float, exit_price: float, quantity: int) -> tuple[float, float]:
    """Compute P&L and P&L percent when closing a trade.

    Returns (pnl_dollars, pnl_percent).
    """
    if direction == 'long':
        pnl = (exit_price - entry_price) * quantity
    else:  # short
        pnl = (entry_price - exit_price) * quantity

    pnl_percent = ((exit_price - entry_price) / entry_price) * 100
    if direction == 'short':
        pnl_percent = -pnl_percent

    return round(pnl, 2), round(pnl_percent, 2)


def close_trade(trade, exit_price: float, exit_date: datetime = None):
    """Close a trade by setting exit price, computing P&L, and updating status."""
    trade.exit_price = exit_price
    trade.exit_date = exit_date or datetime.now(timezone.utc)
    trade.status = 'closed'
    trade.pnl, trade.pnl_percent = compute_pnl(
        trade.direction, trade.entry_price, exit_price, trade.quantity
    )
    return trade
