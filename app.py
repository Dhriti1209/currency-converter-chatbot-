from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "fca_live_XmjaWMI4NnNf7yJuaw10gFuBvGvBztaDygegg3zF"

def fetch_conversion_factor(source, target):
    url = (
        f"https://api.freecurrencyapi.com/v1/latest?"
        f"apikey={API_KEY}&base_currency={source}&currencies={target}"
    )
    response = requests.get(url).json()
    return response["data"][target]

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = round(amount * cf, 2)

    return jsonify({
        "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
    })

if __name__ == "__main__":
    app.run(debug=True)
