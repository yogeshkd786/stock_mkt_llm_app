
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import json
import os
from app.stock_analyzer import analyze_stock

app = Flask(__name__, template_folder=os.path.abspath('d:/MyVault/CodeGuru/ACP/stock_mkt_llm_app/templates'), static_folder=os.path.abspath('d:/MyVault/CodeGuru/ACP/stock_mkt_llm_app/static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/strategies')
def get_strategies():
    schema_path = os.path.abspath('d:/MyVault/CodeGuru/ACP/stock_mkt_llm_app/config/strategy_schema.json')
    with open(schema_path, 'r') as f:
        strategies = json.load(f)
    return jsonify(strategies)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    strategy_id = data.get('strategy')
    params = data.get('params')
    provider = data.get('provider', 'rapidapi') # Default to rapidapi if not provided
    
    if not strategy_id or not params:
        return jsonify({"error": "Missing strategy or parameters"}), 400
        
    result = analyze_stock(strategy_id, params, provider)
    return jsonify(result)

