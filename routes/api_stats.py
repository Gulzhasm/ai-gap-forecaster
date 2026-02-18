from flask import Blueprint, jsonify

api_stats = Blueprint('api_stats', __name__)


@api_stats.route('/summary')
def summary():
    # TODO: Implement in Phase 5
    return jsonify({'data': {}, 'message': 'Stats not yet implemented'})
