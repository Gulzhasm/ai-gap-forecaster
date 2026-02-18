from flask import Blueprint, jsonify

api_watchlist = Blueprint('api_watchlist', __name__)


@api_watchlist.route('/')
def list_watchlist():
    # TODO: Implement in Phase 2
    return jsonify({'data': [], 'message': '0 watchlist items'})
