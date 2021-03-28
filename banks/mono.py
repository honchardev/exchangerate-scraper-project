import datetime

import requests


class CurrencyRatesHandler(object):

    def __init__(
        self
    ) -> None:
        self.BANKNAME = "Monobank"
        self.DATA_URL = "https://api.monobank.ua/bank/currency"
        self.API_DOCS_URL = "https://api.monobank.ua/docs/"

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
        # Validate url response
        url_response_json_is_dict = isinstance(url_response_json, dict)
        if url_response_json_is_dict:
            url_response_json_too_many_requests = \
                (url_response_json.get('errorDescription', '') == 'Too many requests')
            if url_response_json_too_many_requests:
                raise ValueError('mono: too many requests')
        # Work on currencies observations
        currencies_data = []
        for raw_currency_data in url_response_json:
            work_on_raw_currency_data = \
                ('rateBuy' in raw_currency_data) and \
                ('rateSell' in raw_currency_data) and \
                (raw_currency_data['currencyCodeB'] == 980)
            if work_on_raw_currency_data:
                timestamp = datetime.datetime.utcfromtimestamp(raw_currency_data["date"])
                currency_data = {
                    "source": self.BANKNAME,
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
                    "currency": self._currency_code_to_currency_str(raw_currency_data["currencyCodeA"]),
                    "buy": raw_currency_data["rateBuy"],
                    "sell": raw_currency_data["rateSell"],
                    "rawdata": raw_currency_data,
                }
                currencies_data.append(currency_data)
        return currencies_data

    def _currency_code_to_currency_str(
        self,
        code: int
    ) -> str:
        mapping = {
            840: 'USD',
            978: 'EUR',
            643: 'RUB',
            985: 'PLN',
        }
        currency_str = mapping[code]
        return currency_str
