from flask import Flask, request, jsonify
from SmartApi import SmartConnect
import pyotp
import os

app = Flask(__name__)
API_KEY = os.getenv("Ex19gQKe")
CLIENT_CODE = os.getenv("AAAJ462953")
PIN = os.getenv("0109")
TOTP_KEY = os.getenv("ZX2FX7WYTDTYNI23KHA7FN6BX4")  # Secret key for TOTP from your authenticator setup


# Initialize SmartAPI connection
smart_api = SmartConnect(api_key=API_KEY)

def login():
    try:
        totp = pyotp.TOTP(TOTP_KEY).now()
        data = smart_api.generateSession(CLIENT_CODE, PIN, totp)
        if data["status"]:
            return smart_api
        else:
            raise Exception("Login failed: " + data["message"])
    except Exception as e:
        raise Exception("Authentication error: " + str(e))

@app.route("/historical-data", methods=["GET"])
def get_historical_data():
    try:
        # Login to SmartAPI
        api = login()

        # Get parameters from query string
        exchange = request.args.get("exchange", "NSE")
        symbol_token = request.args.get("symbol_token", "3045")  # Default: SBIN-EQ
        interval = request.args.get("interval", "ONE_MINUTE")
        from_date = request.args.get("from_date", "2025-03-01 09:15")
        to_date = request.args.get("to_date", "2025-03-15 15:15")

        # Historical data parameters
        historic_params = {
            "exchange": exchange,
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date
        }

        # Fetch data
        response = api.getCandleData(historic_params)
        if response["status"]:
            return jsonify({"status": "success", "data": response["data"]})
        else:
            return jsonify({"status": "error", "message": response["message"]}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
