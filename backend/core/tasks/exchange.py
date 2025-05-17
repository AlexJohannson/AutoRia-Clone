from datetime import datetime

import requests
from configs.celery import app
from core.exchange_state import exchange_state


@app.task
def update_exchange_rates():
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    response = requests.get(url)
    data = response.json()

    rates = {}

    for item in data:
        if item['ccy'] in ['USD', 'EUR'] and item['base_ccy'] == 'UAH':
            ccy = item['ccy']
            uah_rate = float(item['sale'])
            rates[f"{ccy}_UAH"] = uah_rate

    if 'USD_UAH' in rates and 'EUR_UAH' in rates:
        rates['USD_EUR'] = round(rates['USD_UAH'] / rates['EUR_UAH'], 4)
        rates['EUR_USD'] = round(rates['EUR_UAH'] / rates['USD_UAH'], 4)

    rates['updated'] = datetime.now().isoformat()
    exchange_state.exchange_rates.update(rates)
