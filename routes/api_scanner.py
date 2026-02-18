from flask import Blueprint, jsonify, request
from services.gap_scanner import scan_gaps as do_scan

api_scanner = Blueprint('api_scanner', __name__)


@api_scanner.route('/gaps')
def scan_gaps():
    min_gap = request.args.get('min_gap', 2.0, type=float)
    direction = request.args.get('direction', 'both')
    symbols_str = request.args.get('symbols', '')
    date = request.args.get('date', None)

    # Parse comma-separated symbols or use defaults
    symbols = None
    if symbols_str.strip():
        symbols = [s.strip().upper() for s in symbols_str.split(',') if s.strip()]

    if min_gap < 0:
        return jsonify({'error': 'validation_error', 'message': 'min_gap must be a positive number'}), 400
    if direction not in ('up', 'down', 'both'):
        return jsonify({'error': 'validation_error', 'message': 'direction must be "up", "down", or "both"'}), 400

    result = do_scan(symbols=symbols, min_gap=min_gap, direction=direction, date=date)

    return jsonify({
        'data': result,
        'message': f'Found {result["total_found"]} gaps'
    })
