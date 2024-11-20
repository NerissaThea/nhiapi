from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import traceback

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://jbiz.vercel.app"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,
        "max_age": 600
    }
})

# Etherscan API configuration
ETHERSCAN_API_KEY = os.getenv("IGVQMMEFYD8K2DK22ZTFV6WK1RH8KP98IS")
ETHERSCAN_API_URL = os.getenv("https://api.etherscan.io/api")

if not ETHERSCAN_API_KEY or not ETHERSCAN_API_URL:
    raise ValueError("ETHERSCAN_API_KEY and ETHERSCAN_API_URL must be set in environment variables")

def fetch_transactions(address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["status"] != "1":
            raise Exception(f"Etherscan API error: {data.get('message', 'Unknown error')}")
        return data["result"]
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise Exception(f"Failed to fetch data from Etherscan: {e}")

@app.errorhandler(Exception)
def handle_error(error):
    print(f"Error occurred: {error}")
    print(traceback.format_exc())
    response = jsonify({
        "error": str(error),
        "status": "error"
    })
    return response, 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://jbiz.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/')
def home():
    return jsonify({"status": "API is running", "version": "1.0"})

@app.route('/api/transactions', methods=['GET', 'OPTIONS'])
def get_transactions():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address parameter is required", "status": "error"}), 400

    try:
        transactions = fetch_transactions(address)
        return jsonify({"transactions": transactions, "status": "success"}), 200
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    print(f"API URL configured as: {ETHERSCAN_API_URL}")
    app.run(debug=True)
