import datetime

import requests

# todo: https://www.oschadbank.ua/ua/ajax/CurrencyRates?date=2021-03-25&type=currency
# todo: https://online.oschadbank.ua/mobile/api/v2/currencies/fxrates/cross


class CurrencyRatesHandler(object):

    def __init__(
        self
    ) -> None:
        self.BANKNAME = "OschadBank"
        self.DATA_URL = "https://online.oschadbank.ua/mobile/api/v2/currencies/fxrates/base"
        self.API_DOCS_URL = None

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
        raw_currencies_data = url_response_json["baseRates"]
        for raw_currency_data in raw_currencies_data:
            timestamp = datetime.datetime.strptime(url_response_json["timestamp"], '%Y-%m-%dT%H:%M:%S.%f%z')
            currency_data = {
                "source": self.BANKNAME,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
                "currency": raw_currency_data["currency"],
                "buy": raw_currency_data["buyAt"],
                "sell": raw_currency_data["sellAt"],
                "rawdata": raw_currency_data,
            }
            currencies_data.append(currency_data)
        return currencies_data
