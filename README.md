# AI-Powered Stock Market Analysis & Recommendation System

This application provides stock market analysis and recommendations based on user-defined strategies. It leverages a Large Language Model (LLM) to process financial data and web intelligence, offering a comprehensive overview for investment decisions.

---

## Functional Overview

The application provides a simple web interface where you can:

1.  **Select an Investment Strategy:** Choose from a list of pre-defined strategies, such as Momentum Investing, Value Investing, or News-Based Sentiment Analysis.
2.  **Select a Data Provider:** Choose to fetch financial data from either **TrueData** or **RapidAPI**.
3.  **Provide Inputs:** The UI dynamically generates a form based on the selected strategy, asking for relevant inputs like stock symbols, date ranges, or financial metric thresholds.
4.  **Get AI-Powered Analysis:** The backend, powered by a LangChain agent, takes your inputs, gathers real-time financial data and web intelligence (news, sentiment), and uses a Google Gemini LLM to generate a stock recommendation (BUY, SELL, or HOLD) with a detailed justification.

This tool helps bridge the gap between raw data and actionable insights, allowing users to get a quick, AI-driven second opinion on their investment ideas.

---

## Technical Deep Dive

This project is built on a modern Python stack, integrating a web interface with a powerful AI backend.

### Tech Stack

*   **Backend:** Python, Flask
*   **AI Framework:** LangChain
*   **LLM:** Google Gemini 2.5 Flash
*   **Financial Data:** 
    *   TrueData WebSocket (`truedata-ws`)
    *   RapidAPI (`indian-stock-exchange-api2`)
*   **Web Search:** SerpAPI (`google-search-results`)
*   **Environment Management:** `python-dotenv`
*   **Package Installation:** `uv`

### How It Works

The application follows a simple request-response flow:

1.  **UI Interaction:** The user selects a strategy, data provider, and inputs parameters in the browser.
2.  **API Call:** The frontend sends a POST request to the Flask backend at the `/api/analyze` endpoint.
3.  **Agent Invocation:** The Flask server calls the `analyze_stock` function, which invokes the LangChain agent with a detailed prompt containing the user's strategy, parameters, and selected data provider.
4.  **Tool Execution:** The agent uses its tools (`GetFinancialData` and `SerpAPISearch`) to gather the necessary data. The `GetFinancialData` tool is dynamically configured to use the selected data provider.
5.  **LLM Synthesis:** The agent sends the collected data to the Gemini LLM for analysis and recommendation generation.
6.  **Response to UI:** The final analysis is sent back to the UI and displayed to the user.

### The Agent & Tools

The core of the backend is a **LangChain agent**. This agent is designed to make decisions and use a set of tools to accomplish its goals. The tools are:

*   **`GetFinancialData`:** A dynamic tool that can connect to either the TrueData service or RapidAPI to fetch real-time or historical financial data for a given stock.
*   **`SerpAPISearch`:** Uses SerpAPI to perform web searches for news, sentiment analysis, and geopolitical information related to the stock.

---

## Installation & Setup

This project uses `uv` for fast and efficient package management and execution.

### 1. Prerequisites

*   Python 3.8+
*   `uv` installed (`pip install uv`)

### 2. Configure Environment

1.  Rename the `.env.example` file to `.env` (if you haven't already).
2.  Open the `.env` file and fill in your API keys and credentials for Google (Gemini), TrueData, SerpAPI, and RapidAPI.

### 3. Install Dependencies

Create a virtual environment and install the required packages using `uv`:

```bash
# Create the virtual environment
uv venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 4. Run the Application

With the virtual environment activated, run the application using `uv`:

```bash
uv run python run.py
```

The application will be available at `http://127.0.0.1:5000`.

### Using a Specific Data Provider

To use a specific data provider, simply select it from the **"Select Data Provider"** dropdown menu in the web interface before clicking the "Analyze" button. The application will automatically use the selected provider to fetch the financial data.