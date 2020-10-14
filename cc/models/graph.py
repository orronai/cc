import base64
from datetime import datetime
from io import BytesIO
from typing import Dict

from flask import request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import requests

from cc.ccweb.ccapi import CURRENCIES
from cc.models.errors import CurrencyError, DateError


def get_graph() -> bytes:
    base_currency = request.args.get('base-currency')
    compare_currency = request.args.get('compare-currency')
    if (
        base_currency not in CURRENCIES
        or compare_currency not in CURRENCIES
        or base_currency == compare_currency
    ):
        raise CurrencyError('Bad currencies inputs.', 422)
    starting_date = request.args.get('starting-date')
    ending_date = request.args.get('ending-date')
    if (
        datetime.strptime(starting_date, '%Y-%m-%d') > datetime.today()
        or datetime.strptime(ending_date, '%Y-%m-%d') > datetime.today()
    ):
        raise DateError('Bad dates inputs.', 422)
    response = requests.get(
        f'https://api.exchangeratesapi.io/history?start_at={starting_date}&end'
        f'_at={ending_date}&base={base_currency}&symbols={compare_currency}',
    )

    currency_rates = dict(sorted(response.json().get('rates').items()))
    fig = create_figure(base_currency, compare_currency, currency_rates)
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return base64.b64encode(output.getvalue())


def create_figure(
    base_currency: str,
    compare_currency: str,
    currency_rates: Dict[str, int],
):
    fig = Figure(figsize=(8, 5.4))
    axis = fig.add_subplot(1, 1, 1)
    x_axis = list(currency_rates.keys())
    if not x_axis:
        raise DateError('Bad dates inputs.', 422)
    y_axis = [list(item.values())[0] for item in currency_rates.values()]
    axis.plot(x_axis, y_axis, color='green')
    axis.set_title(
        f'{compare_currency.upper()}/{base_currency.upper()}',
        color='darkgreen', fontsize=20,
    )
    axis.set_xlabel('Dates', color='darkgreen', fontsize=12)
    axis.set_ylabel('Rate', color='darkgreen', fontsize=12)
    axis.xaxis.set_major_locator(MaxNLocator(nbins=6))
    fig.autofmt_xdate(rotation=45, ha='center', bottom=0.3)
    return fig
