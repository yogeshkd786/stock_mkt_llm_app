import os
import json
import http.client
import functools
from urllib.parse import quote
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.utilities import SerpAPIWrapper
from truedata_ws.websocket.TD import TD

# --- Initialization ---

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# Initialize TrueData client
td_user = os.environ.get("TRUEDATA_USERNAME")
td_pass = os.environ.get("TRUEDATA_PASSWORD")
td_client = None


# --- LangChain Tools ---

def get_financial_data(symbol: str, provider: str) -> str:
    """
    Fetches financial data for a given stock symbol.
    The symbol should be the stock symbol (e.g., 'RELIANCE').
    """
    print(f"Fetching data for {symbol} using {provider}")

    if provider == 'truedata':
        if td_user and td_pass:
            try:
                td_client = TD(td_user, td_pass)
            except Exception as e:
                print(f"Warning: TrueData client failed to initialize: {e}")
        if not td_client:
            return "TrueData client is not initialized. Please check your credentials."
        try:
            historical_data = td_client.get_historic_data(symbol, duration='1 M')
            return json.dumps(historical_data)
        except Exception as e:
            return f"Error fetching data from TrueData: {e}"

    elif provider == 'rapidapi':
        try:
            conn = http.client.HTTPSConnection("indian-stock-exchange-api2.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY"),
                'x-rapidapi-host': "indian-stock-exchange-api2.p.rapidapi.com"
            }
            # Note: The RapidAPI endpoint seems to have limited functionality in the provided example.
            # This is a simplified implementation based on the example.
            conn.request("GET", f"/historical_data?stock_name={quote(symbol)}&period=1m&filter=price", headers=headers)
            res = conn.getresponse()
            data = res.read()
            return data.decode("utf-8")
        except Exception as e:
            return f"Error fetching data from RapidAPI: {e}"

    else:
        return f"Unknown data provider: {provider}"


search = SerpAPIWrapper()

def run_serpapi_and_print(query: str) -> str:
    """Wrapper for SerpAPI to print a message before execution."""
    print("\nExecuting SerpAPI search...\n")
    return search.run(query)

# --- Main Analysis Function ---

def analyze_stock(strategy_id: str, params: dict, provider: str) -> dict:
    """
    Analyzes a stock based on the selected strategy using a LangChain agent.
    """
    print(f"Analyzing with strategy '{strategy_id}', params {params}, and provider {provider}")

    symbol = params.get("symbol")
    if not symbol:
        return {"error": "Stock symbol not found in parameters."}

    # Dynamically create the financial data tool with the selected provider
    get_financial_data_tool = Tool(
        name="GetFinancialData",
        func=lambda _: get_financial_data(symbol=symbol, provider=provider),
        description=f"Useful for getting real-time or historical financial data for the specified stock symbol from the {provider} provider.",
    )

    tools = [
        get_financial_data_tool,
        Tool(
            name="SerpAPISearch",
            func=run_serpapi_and_print,
            description="Useful for searching the web for news, sentiment analysis, and geopolitical information related to a stock using SerpAPI.",
        ),
    ]

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    # Create a detailed prompt for the agent
    prompt = f"""
    Analyze the stock(s) based on the following investment strategy using the {provider} data provider:

    Strategy: {strategy_id}
    Parameters: {json.dumps(params)}

    Your task is to act as an expert financial analyst. Follow these steps:
    1.  Use the 'GetFinancialData' tool to fetch the latest financial data for the stock(s).
    2.  Use the 'SerpAPISearch' tool to find recent news, market sentiment, and any relevant geopolitical events.
    3.  Synthesize the financial data and the qualitative information from your web search.
    4.  Based on your analysis, provide a clear recommendation (BUY, SELL, or HOLD).
    5.  Provide a concise justification for your recommendation, referencing the data and news you found.

    Begin your analysis now.
    """

    try:
        result = agent.run(prompt)
        response = {
            "strategy": strategy_id,
            "parameters": params,
            "provider": provider,
            "recommendation": "HOLD", # Default
            "justification": result,
        }
        if "BUY" in result.upper():
            response["recommendation"] = "BUY"
        elif "SELL" in result.upper():
            response["recommendation"] = "SELL"

        return response

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return {"error": str(e)}
