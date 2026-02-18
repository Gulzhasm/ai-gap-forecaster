import yfinance as yf
from datetime import datetime, timedelta
from services.symbols import DEFAULT_SYMBOLS

# Simple cache for sector lookups
_sector_cache = {}


def scan_gaps(
    symbols: list[str] = None,
    min_gap: float = 2.0,
    direction: str = 'both',
    date: str = None
) -> dict:
    """Scan for gap openings in US stocks.

    Returns dict with scan_date, total_found, and gaps list.
    """
    if symbols is None:
        symbols = DEFAULT_SYMBOLS

    end_date = datetime.strptime(date, '%Y-%m-%d') if date else datetime.now()
    start_date = end_date - timedelta(days=7)  # 7 days to handle weekends/holidays

    results = []

    # Batch download for performance
    try:
        data = yf.download(
            tickers=symbols,
            start=start_date.strftime('%Y-%m-%d'),
            end=(end_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            group_by='ticker',
            progress=False
        )
    except Exception as e:
        return {
            'scan_date': end_date.strftime('%Y-%m-%d'),
            'total_found': 0,
            'gaps': [],
            'error': str(e)
        }

    for symbol in symbols:
        try:
            if len(symbols) == 1:
                df = data
            else:
                df = data[symbol]

            # Drop rows with NaN close/open
            df = df.dropna(subset=['Close', 'Open'])
            if len(df) < 2:
                continue

            yesterday = df.iloc[-2]
            today = df.iloc[-1]

            prev_close = float(yesterday['Close'])
            today_open = float(today['Open'])
            current_price = float(today['Close'])
            volume = int(today['Volume'])

            if prev_close == 0:
                continue

            gap_percent = ((today_open - prev_close) / prev_close) * 100
            gap_amount = today_open - prev_close

            # Direction filter
            if direction == 'up' and gap_percent <= 0:
                continue
            if direction == 'down' and gap_percent >= 0:
                continue

            # Min gap filter
            if abs(gap_percent) < min_gap:
                continue

            gap_direction = 'up' if gap_percent > 0 else 'down'

            results.append({
                'symbol': symbol,
                'prev_close': round(prev_close, 2),
                'open': round(today_open, 2),
                'current': round(current_price, 2),
                'gap_percent': round(gap_percent, 2),
                'gap_amount': round(gap_amount, 2),
                'direction': gap_direction,
                'volume': volume,
                'sector': _get_sector(symbol)
            })
        except Exception:
            continue

    # Sort by absolute gap percentage descending
    results.sort(key=lambda x: abs(x['gap_percent']), reverse=True)

    return {
        'scan_date': end_date.strftime('%Y-%m-%d'),
        'total_found': len(results),
        'gaps': results
    }


def _get_sector(symbol: str) -> str:
    """Get sector for a symbol with caching."""
    if symbol in _sector_cache:
        return _sector_cache[symbol]

    try:
        info = yf.Ticker(symbol).info
        sector = info.get('sector', 'Unknown')
        _sector_cache[symbol] = sector
        return sector
    except Exception:
        _sector_cache[symbol] = 'Unknown'
        return 'Unknown'
