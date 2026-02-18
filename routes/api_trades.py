from flask import Blueprint, jsonify

api_trades = Blueprint('api_trades', __name__)


@api_trades.route('/')
def list_trades():
    # TODO: Implement in Phase 3
    return jsonify({'data': {'trades': [], 'total': 0, 'page': 1, 'per_page': 50}, 'message': '0 trades returned'})
