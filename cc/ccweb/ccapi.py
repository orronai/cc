from typing import List

import requests


def get_currencies() -> List[str]:
    response = requests.get('https://api.exchangeratesapi.io/latest')
    data = response.json()
    currencies = list(data.get('rates'))
    currencies.append(data.get('base'))
    return currencies


CURRENCIES = get_currencies()
