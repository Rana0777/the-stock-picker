import yfinance as yf
import requests
import gradio as gr
import plotly.graph_objs as go
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "c264a6c96c0f4d35887a2e94a6e7dfc2")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBCAp0lRmckoDpxsTuEnBBslZIPR2BDfF0")

def fetch_company_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A")
        }
    except Exception:
        return {
            "name": "N/A",
            "sector": "N/A",
            "market_cap": "N/A",
            "summary": "N/A"
        }

def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        if hist.empty:
            return None
        return hist
    except Exception:
        return None

def fetch_news(symbol):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&sortBy=publishedAt&pageSize=3"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        summaries = [f"{a['title']} - {a['description']}" for a in articles if a.get('title') and a.get('description')]
        return "\n".join(summaries) if summaries else "No recent news found."
    except Exception:
        return "Error fetching news."

def technical_analysis(hist):
    try:
        closes = hist['Close']
        sma = closes.rolling(window=20).mean()
        rsi = ((closes.diff().apply(lambda x: max(x,0)).rolling(window=14).mean()) /
               (closes.diff().apply(lambda x: abs(x)).rolling(window=14).mean())) * 100
        return f"20-day SMA: {sma.iloc[-1]:.2f}\n14-day RSI: {rsi.iloc[-1]:.2f}"
    except Exception:
        return "Error in technical analysis."

def get_gemini_recommendation(symbol, info, hist, news, analysis, api_key):
    try:
        prompt = f"""
        You are an expert financial analyst. 
        All output must be in English.
        Stock: {symbol}
        Company Info: {info}
        Past 6 months price history: {hist.tail(10).to_dict() if hist is not None else 'N/A'}
        Technical Analysis: {analysis}
        News: {news}
        Based on all this, answer these questions:
        1. Should I pick this stock for investment?
        2. What is its past and future outlook?
        3. Estimate the possible profit (in %) for the next month if I invest now.
        4. Give a clear buy/sell/hold recommendation with reasoning.
        Format your answer in clear English with bullet points and a summary.
        """
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        params = {"key": api_key}
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini API error: {str(e)}"

def plot_chart(hist):
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
        fig.update_layout(title="Stock Price History (6 months)", xaxis_title="Date", yaxis_title="Price")
        return fig
    except Exception:
        return go.Figure()

def stock_insight(symbol):
    symbol = symbol.strip().upper()
    if not symbol:
        return "Please enter a valid stock symbol.", go.Figure()

    info = fetch_company_info(symbol)
    hist = fetch_stock_data(symbol)
    if hist is None:
        return f"Could not fetch data for symbol: {symbol}. Please check the symbol and try again.", go.Figure()
    news = fetch_news(symbol)
    analysis = technical_analysis(hist)
    recommendation = get_gemini_recommendation(symbol, info, hist, news, analysis, GEMINI_API_KEY)
    chart = plot_chart(hist)
    output = (
        f"### 🏢 Company Info\n"
        f"**Name:** {info['name']}\n"
        f"**Sector:** {info['sector']}\n"
        f"**Market Cap:** {info['market_cap']}\n"
        f"**Summary:** {info['summary']}\n\n"
        f"### 📊 Technical Analysis\n{analysis}\n\n"
        f"### 📰 Recent News\n{news}\n\n"
        f"### 🤖 AI Recommendation & Profit Estimate\n{recommendation}"
    )
    return output, chart

with gr.Blocks() as demo:
    gr.Markdown("# 📈 Stock Insight AI (Advanced & Interactive)")
    with gr.Row():
        stock = gr.Textbox(label="Enter Stock Symbol (e.g. AAPL, TSLA)", scale=2)
        btn = gr.Button("Analyze", scale=1)
    result = gr.Markdown()
    chart = gr.Plot()
    btn.click(stock_insight, inputs=stock, outputs=[result, chart])

if __name__ == "__main__":
    demo.launch()