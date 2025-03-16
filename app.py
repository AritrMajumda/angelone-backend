

from flask import Flask, request, jsonify
from SmartApi import SmartConnect
import pyotp
import os
import logging

app = Flask(__name__)
logger.info("Environment variables: %s", os.environ)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
API_KEY = os.getenv("ND6R2gMJ")
CLIENT_CODE = os.getenv("AAAJ462953")
PIN = os.getenv("0109")
TOTP_KEY = os.getenv("ZX2FX7WYTDTYNI23KHA7FN6BX4")

# Initialize SmartAPI connection
smart_api = SmartConnect(api_key=API_KEY)

def login():
    try:
        # Validate environment variables
        if not API_KEY:
            raise Exception("API_KEY is not set")
        if not CLIENT_CODE:
            raise Exception("CLIENT_CODE is not set")
        if not PIN:
            raise Exception("PIN is not set")
        if not TOTP_KEY:
            raise Exception("TOTP_KEY is not set")

        totp = pyotp.TOTP(TOTP_KEY).now()
        data = smart_api.generateSession(CLIENT_CODE, PIN, totp)
        if data["status"]:
            return smart_api
        else:
            raise Exception("Login failed: " + data["message"])
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Angel One Historical Data API! Use /historical-data to fetch data."})

@app.route("/historical-data", methods=["GET"])
def get_historical_data():
    try:
        api = login()
        exchange = request.args.get("exchange", "NSE")
        symbol_token = request.args.get("symbol_token", "3045")
        interval = request.args.get("interval", "ONE_MINUTE")
        from_date = request.args.get("from_date", "2025-03-01 09:15")
        to_date = request.args.get("to_date", "2025-03-15 15:15")

        historic_params = {
            "exchange": exchange,
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date
        }

        response = api.getCandleData(historic_params)
        if response["status"]:
            return jsonify({"status": "success", "data": response["data"]})
        else:
            return jsonify({"status": "error", "message": response["message"]}), 400

    except Exception as e:
        logger.error(f"Historical data error: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route("/debug", methods=["GET"])
def debug():
    return jsonify({
        "API_KEY": API_KEY,
        "CLIENT_CODE": CLIENT_CODE,
        "PIN": PIN,
        "TOTP_KEY": TOTP_KEY
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
