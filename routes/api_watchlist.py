from flask import Blueprint, jsonify, request
from models import db, Watchlist

api_watchlist = Blueprint('api_watchlist', __name__)


@api_watchlist.route('/')
def list_watchlist():
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    query = Watchlist.query
    if active_only:
        query = query.filter_by(is_active=True)
    items = query.order_by(Watchlist.added_date.desc()).all()
    return jsonify({
        'data': [item.to_dict() for item in items],
        'message': f'{len(items)} watchlist items'
    })


@api_watchlist.route('/', methods=['POST'])
def add_to_watchlist():
    data = request.get_json()
    if not data or not data.get('symbol'):
        return jsonify({'error': 'validation_error', 'message': 'symbol is required'}), 400

    symbol = data['symbol'].upper().strip()

    existing = Watchlist.query.filter_by(symbol=symbol).first()
    if existing:
        return jsonify({'error': 'duplicate', 'message': f'{symbol} is already on watchlist'}), 409

    item = Watchlist(
        symbol=symbol,
        notes=data.get('notes'),
        target_price=data.get('target_price'),
        sector=data.get('sector')
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'data': item.to_dict(),
        'message': f'{symbol} added to watchlist'
    }), 201


@api_watchlist.route('/<int:item_id>', methods=['PUT'])
def update_watchlist(item_id):
    item = db.session.get(Watchlist, item_id)
    if not item:
        return jsonify({'error': 'not_found', 'message': f'Watchlist item {item_id} not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'validation_error', 'message': 'Request body is required'}), 400

    if 'notes' in data:
        item.notes = data['notes']
    if 'target_price' in data:
        item.target_price = data['target_price']
    if 'is_active' in data:
        item.is_active = data['is_active']
    if 'sector' in data:
        item.sector = data['sector']

    db.session.commit()
    return jsonify({
        'data': item.to_dict(),
        'message': 'Watchlist item updated'
    })


@api_watchlist.route('/<int:item_id>', methods=['DELETE'])
def delete_from_watchlist(item_id):
    item = db.session.get(Watchlist, item_id)
    if not item:
        return jsonify({'error': 'not_found', 'message': f'Watchlist item {item_id} not found'}), 404

    symbol = item.symbol
    db.session.delete(item)
    db.session.commit()
    return jsonify({
        'data': None,
        'message': f'{symbol} removed from watchlist'
    })
