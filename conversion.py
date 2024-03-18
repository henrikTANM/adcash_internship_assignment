import requests
import json

class Conversion:

    def get_conversion_rate():
        res = requests.get("http://api-cryptopia.adca.sh/v1/prices/ticker")
        response = json.loads(res.text)["data"][0]["value"]
        return float(response)

    def get_BTC_value_in_EUR(BTC):
        return Conversion.get_conversion_rate() * BTC

    def get_EUR_value_in_BTC(EUR):
        return EUR / Conversion.get_conversion_rate()
        