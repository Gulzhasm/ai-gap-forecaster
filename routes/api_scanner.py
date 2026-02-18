from flask import Blueprint, jsonify, request

api_scanner = Blueprint('api_scanner', __name__)


@api_scanner.route('/gaps')
def scan_gaps():
    min_gap = request.args.get('min_gap', 2.0, type=float)
    direction = request.args.get('direction', 'both')
    symbols = request.args.get('symbols', '')
    date = request.args.get('date', None)

    # TODO: Wire to gap_scanner service in Phase 4
    return jsonify({
        'data': {'scan_date': date, 'total_found': 0, 'gaps': []},
        'message': 'Scanner not yet implemented'
    })
