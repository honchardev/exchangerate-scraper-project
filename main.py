import json

from flask import Flask

from banks.mono import CurrencyRatesHandler as monohandler
from banks.oschad import CurrencyRatesHandler as oschadhandler
from banks.privat import CurrencyRatesHandler as privathandler


app = Flask(__name__)

currencies_storage = []


@app.route('/')
@app.route('/currencies')
def currencies():
    response_data = currencies_storage
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/update')
def update():
    #
    global currencies_storage
    #
    bank_handlers_storage = {
        'mono': monohandler(),
        'oschad': oschadhandler(),
        'privat': privathandler()
    }
    #
    response_data = {
        'success': [],
        'failed': [],
    }
    #
    for bank_name, bank_handler in bank_handlers_storage.items():
        try:
            currencies_storage.extend(
                bank_handler.handle()
            )
            response_data['success'].append(bank_name)
        except ValueError:
            response_data['failed'].append(bank_name)
    #
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8888,
        debug=True,
    )
