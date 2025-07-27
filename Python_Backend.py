from flask import Flask, render_template, jsonify
from datetime import datetime
from Prediction import prediction_stock_price
import yfinance as yf

app = Flask(__name__)

# Route to serve your frontend
@app.route('/')
def frontend():
    return render_template('FRONTEND.html')  # file should be in templates/FRONTEND.html

# API endpoint to fetch stock data
@app.route("/api/stock/<symbol>", methods=['GET'])
def get_stock_data(symbol):
    print(f"\n[✓] API called with ticker: {symbol}")
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period='1y')

        if history.empty:
            print("[!] No data found.")
            return jsonify({'error': 'No data found'}), 404

        historical_prices = history["Close"].tolist()
        historical_dates = history.index.strftime('%Y-%m-%d').tolist()

        predicted_price = prediction_stock_price(historical_prices)
        current_price = history["Close"][-1]

        response = {
            "symbol": symbol.upper(),
            "current_price": round(float(current_price), 4),
            "predicted_price": round(float(predicted_price), 2),
            "last_updated": datetime.now().strftime('%Y-%m-%d %I:%M %p'),
            "historical_dates": historical_dates,
            "historical_prices": [round(price, 2) for price in historical_prices],
            "error": None
        }

        return jsonify(response)

    except Exception as e:
        print(f"[!!] Error occurred: {e}")
        return jsonify({"error": "Error fetching data", "details": str(e)}), 500

# Entry point
def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
