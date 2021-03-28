import datetime

import requests

# todo: https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014
# todo: https://api.privatbank.ua/p24api/pubinfo?jsonp=success&exchange=&coursid=11


class CurrencyRatesHandler(object):

    def __init__(
        self
    ) -> None:
        self.BANKNAME = "PrivatBank"
        self.DATA_URL = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
        self.API_DOCS_URL = "https://api.privatbank.ua/#p24/exchange"

    def handle(
        self
    ) -> list:
        # Fetch bank response
        url_response = requests.get(self.DATA_URL)
        url_response_json = url_response.json()
        # Format response data
        currencies_data = self.format(url_response_json)
        # Return currencies rates data
        return currencies_data

    def format(
        self,
        url_response_json: dict
    ) -> dict:
        # Work on currencies observations
        currencies_data = []
        for raw_currency_data in url_response_json:
            work_on_raw_currency_data = \
                (raw_currency_data['base_ccy'] == 'UAH')
            if work_on_raw_currency_data:
                currency_data = {
                    "source": self.BANKNAME,
                    "timestamp": None,
                    "currency": raw_currency_data["ccy"],
                    "buy": raw_currency_data["buy"],
                    "sell": raw_currency_data["sale"],
                    "rawdata": raw_currency_data,
                }
                currencies_data.append(currency_data)
        return currencies_data
