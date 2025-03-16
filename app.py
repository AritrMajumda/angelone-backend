from flask import Flask, jsonify, request
from SmartApi import SmartConnect
import pyotp
import datetime

app = Flask(__name__)

# Angel One Credentials
API_KEY = "Ex19gQKe"
CLIENT_ID = "AAAJ462953"
MPIN = "0109"  # Use MPIN instead of Password
TOTP_SECRET = "ZX2FX7WYTDTYNI23KHA7FN6BX4"

# Generate TOTP for login
totp = pyotp.TOTP(TOTP_SECRET).now()

# Authenticate with Angel One using MPIN
obj = SmartConnect(api_key=API_KEY)
data = obj.generateSession(CLIENT_ID, password=MPIN, totp=totp)
# Debug: Print login response
print("Login Response:", data)

# Check for login failure
if data is None or 'data' not in data or 'refreshToken' not in data['data']:
    raise Exception("Login failed! Check API credentials, MPIN, or TOTP.")

# Step 2: Use refreshToken to get Access Token
refresh_token = data['data']['refreshToken']
session_data = obj.generateSession(refresh_token)

if session_data is None or 'data' not in session_data or 'jwtToken' not in session_data['data']:
    raise Exception("Session creation failed! Check refresh token.")

AUTH_TOKEN = session_data['data']['jwtToken']

@app.route('/')
def home():
    return jsonify({"message": "Angel One API is working!"})

@app.route('/historical-data', methods=['GET'])
def historical_data():
    try:
        symbol_token = request.args.get('symbol_token', '3045')  # Default: RELIANCE
        exchange = request.args.get('exchange', 'NSE')
        interval = request.args.get('interval', 'ONE_MINUTE')  

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
