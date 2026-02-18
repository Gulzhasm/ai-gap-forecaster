from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def dashboard():
    return render_template('dashboard.html')


@views.route('/watchlist')
def watchlist():
    return render_template('watchlist.html')


@views.route('/journal')
def journal():
    return render_template('journal.html')


@views.route('/performance')
def performance():
    return render_template('performance.html')
