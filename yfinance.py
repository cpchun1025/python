from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Stock Data API! Use /stock?ticker=<symbol> to get stock data."

@app.route('/stock', methods=['GET'])
def get_stock_data():
    # Get the stock ticker from the query parameter
    ticker = request.args.get('ticker')
    
    if not ticker:
        return jsonify({"error": "Please provide a stock ticker symbol using '?ticker=<symbol>'"}), 400
    
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)

        # Get basic stock information (like current price and company info)
        stock_info = stock.info
        if not stock_info:
            return jsonify({"error": f"No data found for ticker: {ticker}"}), 404
        
        # Get the stock's historical price data (last 5 days)
        history = stock.history(period="5d").reset_index()

        # Convert historical data to a list of dictionaries for JSON serialization
        history_data = history.to_dict(orient='records')

        # Create a response object
        response = {
            "symbol": stock_info.get('symbol'),
            "longName": stock_info.get('longName'),
            "currentPrice": stock_info.get('currentPrice'),
            "marketCap": stock_info.get('marketCap'),
            "sector": stock_info.get('sector'),
            "currency": stock_info.get('currency'),
            "historicalData": history_data
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)