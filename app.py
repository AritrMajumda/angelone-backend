from flask import Flask, jsonify
from SmartApi import SmartConnect
import pyotp

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Angel One API is working!"})

@app.route('/historical-data')
def historical_data():
    return jsonify({"message": "Historical data will be fetched here"})

if __name__ == '__main__':
    app.run(debug=True)
# 🔹 Replace these with your Angel One API credentials
API_KEY = "Ex19gQKe"
CLIENT_ID = "651548e7-0eee-4603-a6f9-a9838d997d29"
PASSWORD = "Ayantika@1"
TOTP_SECRET = "ZX2FX7WYTDTYNI23KHA7FN6BX4"

@app.route('/historical-data', methods=['GET'])
def get_historical_data():
    try:
        obj = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        session_data = obj.generateSession(CLIENT_ID, PASSWORD, totp)

        if 'status' in session_data and session_data['status'] == False:
            return jsonify({"error": "Authentication failed"}), 401

        historic_param = {
            "exchange": "NSE",
            "symboltoken": "3045",  # Example: Reliance
            "interval": "ONE_DAY",
            "fromdate": "2024-03-01 09:15",
            "todate": "2024-03-15 15:30"
        }
        historical_data = obj.getCandleData(historic_param)

        return jsonify(historical_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
