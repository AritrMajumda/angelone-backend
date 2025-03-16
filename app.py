from flask import Flask, jsonify, request
from SmartApi import SmartConnect  # Angel One SmartAPI
import pyotp
import datetime

app = Flask(__name__)

# Replace with your actual Angel One credentials
API_KEY = "Ex19gQKe"
CLIENT_ID = "AAAJ462953"
PASSWORD = "Ayantika@1"
TOTP_SECRET = "ZX2FX7WYTDTYNI23KHA7FN6BX4"  # This must be set manually

# Generate TOTP for login
totp = pyotp.TOTP(TOTP_SECRET).now()

# Authenticate with Angel One
obj = SmartConnect(api_key=API_KEY)
data = obj.generateSession(CLIENT_ID, PASSWORD, totp)
AUTH_TOKEN = data['data']['jwtToken']

data = obj.generateSession(CLIENT_ID, PASSWORD, totp)

# Print the API response for debugging
print("Login Response:", data)

# Check if login was successful
if data is None or 'data' not in data:
    raise Exception("Login failed! Check API key, client ID, password, or TOTP.")

@app.route('/')
def home():
    return jsonify({"message": "Angel One API is working!"})

@app.route('/historical-data', methods=['GET'])
def historical_data():
    try:
        symbol_token = request.args.get('symbol_token', '3045')  # Default: RELIANCE
        exchange = request.args.get('exchange', 'NSE')
        interval = request.args.get('interval', 'ONE_MINUTE')  # Other: 'FIVE_MINUTE', 'DAY'
        
        to_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        from_date = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')

        historic_data = obj.getCandleData(
            token=symbol_token, exchange=exchange, interval=interval,
            fromdate=from_date, todate=to_date
        )

        return jsonify(historic_data)
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
