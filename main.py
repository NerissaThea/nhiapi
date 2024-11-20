from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Bật CORS để bỏ qua mọi chính sách kiểm tra
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://jbiz.vercel.app"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Middleware thêm các tiêu đề CORS vào mọi phản hồi
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"]
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"]
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Endpoint chính để test API
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "CORS is completely bypassed. API is running!"})

# Endpoint trả về dữ liệu giao dịch mẫu
@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address is required"}), 400

    # Dữ liệu giao dịch mẫu
    transactions = [
        {"from": "0xABC123", "to": "0xDEF456", "amount": 1.23, "hash": "0xHASH1"},
        {"from": "0xGHI789", "to": "0xJKL012", "amount": 2.34, "hash": "0xHASH2"}
    ]

    return jsonify({"transactions": transactions}), 200

# Xử lý preflight requests (OPTIONS)
@app.route("/api/transactions", methods=["OPTIONS"])
def options_transactions():
    response = jsonify({"message": "Preflight request successful"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"]
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"]
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
