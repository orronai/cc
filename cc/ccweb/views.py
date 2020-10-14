from flask import jsonify, render_template

from cc.ccweb import app
from cc.ccweb.ccapi import CURRENCIES
from cc.models.errors import CurrenciesError, fail  # type: ignore
from cc.models.graph import get_graph  # type: ignore


@app.route('/')
def main():
    return render_template(
        'converter.html',
        currencies=CURRENCIES,
    )


@app.route('/graph')
def graph():
    try:
        io_graph = get_graph()
    except CurrenciesError as e:
        error_message, status_code = e.args
        return fail(status_code, error_message)

    return jsonify({'success': 'true', 'graph': io_graph})
