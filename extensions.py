import requests
import json
from config import keys


class ConvertionException(Exception):
    ...


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if float(amount) < 0:
            raise ConvertionException('Отрицательное количество валюты!')

        if quote == base:
            raise ConvertionException('Одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать сумму {amount}')

        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/217fb86abb2e447ec7985b84/pair/{quote_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(r.content)['conversion_result']

        return total_base
