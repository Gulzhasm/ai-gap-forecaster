from datetime import datetime
from flask import Blueprint, jsonify, request
from models import db, Trade
from services.trade_service import close_trade

api_trades = Blueprint('api_trades', __name__)


@api_trades.route('/')
def list_trades():
    status = request.args.get('status', 'all')
    symbol = request.args.get('symbol')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = Trade.query
    if status != 'all':
        query = query.filter_by(status=status)
    if symbol:
        query = query.filter_by(symbol=symbol.upper())

    query = query.order_by(Trade.entry_date.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'data': {
            'trades': [t.to_dict() for t in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        },
        'message': f'{len(pagination.items)} trades returned'
    })


@api_trades.route('/', methods=['POST'])
def create_trade():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'validation_error', 'message': 'Request body is required'}), 400

    required = ['symbol', 'direction', 'entry_price', 'quantity', 'gap_type']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': 'validation_error', 'message': f'Missing required fields: {", ".join(missing)}'}), 400

    if data['direction'] not in ('long', 'short'):
        return jsonify({'error': 'validation_error', 'message': 'direction must be "long" or "short"'}), 400
    if data['gap_type'] not in ('gap_up', 'gap_down'):
        return jsonify({'error': 'validation_error', 'message': 'gap_type must be "gap_up" or "gap_down"'}), 400
    if float(data['entry_price']) <= 0:
        return jsonify({'error': 'validation_error', 'message': 'entry_price must be positive'}), 400

    entry_date = data.get('entry_date')
    if entry_date:
        try:
            entry_date = datetime.fromisoformat(entry_date)
        except ValueError:
            return jsonify({'error': 'validation_error', 'message': 'entry_date must be ISO format'}), 400
    else:
        entry_date = datetime.utcnow()

    trade = Trade(
        symbol=data['symbol'].upper().strip(),
        direction=data['direction'],
        entry_price=float(data['entry_price']),
        quantity=int(data['quantity']),
        entry_date=entry_date,
        gap_type=data['gap_type'],
        gap_percent=data.get('gap_percent'),
        notes=data.get('notes'),
        setup_rating=data.get('setup_rating')
    )
    db.session.add(trade)
    db.session.commit()

    return jsonify({
        'data': trade.to_dict(),
        'message': f'Trade opened for {trade.symbol}'
    }), 201


@api_trades.route('/<int:trade_id>', methods=['PUT'])
def update_trade(trade_id):
    trade = db.session.get(Trade, trade_id)
    if not trade:
        return jsonify({'error': 'not_found', 'message': f'Trade {trade_id} not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'validation_error', 'message': 'Request body is required'}), 400

    # Close trade if exit_price provided on an open trade
    if 'exit_price' in data and trade.status == 'open':
        exit_date = None
        if 'exit_date' in data:
            try:
                exit_date = datetime.fromisoformat(data['exit_date'])
            except ValueError:
                return jsonify({'error': 'validation_error', 'message': 'exit_date must be ISO format'}), 400

        close_trade(trade, float(data['exit_price']), exit_date)
        db.session.commit()
        pnl_str = f'+${trade.pnl:.2f}' if trade.pnl >= 0 else f'-${abs(trade.pnl):.2f}'
        return jsonify({
            'data': trade.to_dict(),
            'message': f'Trade closed with P&L {pnl_str}'
        })

    # Otherwise update editable fields
    if 'notes' in data:
        trade.notes = data['notes']
    if 'setup_rating' in data:
        trade.setup_rating = data['setup_rating']
    if 'status' in data and data['status'] == 'cancelled':
        trade.status = 'cancelled'

    db.session.commit()
    return jsonify({
        'data': trade.to_dict(),
        'message': 'Trade updated'
    })


@api_trades.route('/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    trade = db.session.get(Trade, trade_id)
    if not trade:
        return jsonify({'error': 'not_found', 'message': f'Trade {trade_id} not found'}), 404

    db.session.delete(trade)
    db.session.commit()
    return jsonify({
        'data': None,
        'message': f'Trade {trade_id} deleted'
    })
