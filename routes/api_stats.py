from flask import Blueprint, jsonify, request
from services.stats_service import get_summary, get_pnl_series, get_by_gap_type

api_stats = Blueprint('api_stats', __name__)


@api_stats.route('/summary')
def summary():
    data = get_summary()
    return jsonify({'data': data, 'message': 'Performance summary'})


@api_stats.route('/pnl-series')
def pnl_series():
    period = request.args.get('period', 'daily')
    days = request.args.get('days', 30, type=int)
    data = get_pnl_series(period=period, days=days)
    return jsonify({'data': data, 'message': f'P&L series for {days} days'})


@api_stats.route('/by-gap-type')
def by_gap_type():
    data = get_by_gap_type()
    return jsonify({'data': data, 'message': 'Stats by gap type'})
