from datetime import datetime

import requests


def get_exchange_rates():
    try:
        response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5')
        response.raise_for_status()
        data = response.json()

        rates = {}
        for rate in data:
            if rate['ccy'] == 'USD':
                rates['USD_UAH'] = float(rate['sale'])
                rates['USD_EUR'] = float(rate['sale']) / next(
                    float(r['sale']) for r in data if r['ccy'] == 'EUR'
                )
            elif rate['ccy'] == 'EUR':
                rates['EUR_UAH'] = float(rate['sale'])
                rates['EUR_USD'] = float(rate['sale']) / next(
                    float(r['sale']) for r in data if r['ccy'] == 'USD'
                )

        if not all(key in rates for key in ['USD_UAH', 'EUR_UAH']):
            raise Exception("Necessary exchange rates not found")

        rates['updated'] = datetime.now()
        return rates

    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        raise Exception("Exchange rates not loaded")
