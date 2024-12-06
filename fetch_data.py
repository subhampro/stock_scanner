from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta
import requests

def get_all_nse_stocks():
    try:
        urls = [
            "https://archives.nseindia.com/content/equities/EQUITY_L.csv",
            "https://www1.nseindia.com/content/equities/EQUITY_L.csv"
        ]
        
        for url in urls:
            try:
                df = pd.read_csv(url)
                if not df.empty:
                    return [f"{symbol}.NS" for symbol in df['SYMBOL'].tolist()]
            except:
                continue
                
        return []
    except:
        return []

def fetch_all_tickers(exchange_filter="NSE"):
    try:
        url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
        params = {
            "formatted": "true",
            "lang": "en-US",
            "region": "IN",
            "scrIds": "all_stocks_with_earnings_estimates",
            "count": 250
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers)
        json_data = json.loads(response.text)
        
        stocks = []
        if (json_data 
            and 'finance' in json_data 
            and 'result' in json_data['finance'] 
            and json_data['finance']['result']
            and 'quotes' in json_data['finance']['result'][0]):
            
            quotes = json_data['finance']['result'][0]['quotes']
            
            if exchange_filter.upper() == "NSE":
                stocks = [q['symbol'] for q in quotes if '.NS' in q['symbol'] and not any(x in q['symbol'] for x in ['NIFTY', 'SENSEX', 'BANKNIFTY'])]
            else:  # ALL
                stocks = [q['symbol'] for q in quotes if '.NS' in q['symbol'] or '.BO' in q['symbol']]

        if len(stocks) < 100 and exchange_filter.upper() == "NSE":
            nse_stocks = get_all_nse_stocks()
            if nse_stocks:
                return nse_stocks
        
        return stocks if stocks else [
            # New Age Tech & Digital
            "ZOMATO.NS", "NYKAA.NS", "PAYTM.NS", "DELHIVERY.NS",
            # IT & Software
            "PERSISTENT.NS", "LTTS.NS", "COFORGE.NS", "HAPPSTMNDS.NS",
            # Pharma & Healthcare
            "ALKEM.NS", "TORNTPHARM.NS", "AUROPHARMA.NS", "BIOCON.NS",
            # Manufacturing & Industrial
            "DIXON.NS", "AMBER.NS", "POLYCAB.NS", "VGUARD.NS", "BLUESTARCO.NS",
            # Financial Services
            "MUTHOOTFIN.NS", "CHOLAFIN.NS", "MANAPPURAM.NS", "MASFIN.NS",
            # Chemical & Materials
            "CLEAN.NS", "DEEPAKFERT.NS", "AARTIIND.NS", "ALKYLAMINE.NS", "GALAXYSURF.NS",
            # Consumer & Retail
            "VSTIND.NS", "RADICO.NS", "METROPOLIS.NS", "RELAXO.NS",
            # Infrastructure & Real Estate
            "OBEROIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS", "SOBHA.NS",
            # Energy & Utilities
            "TATAPOWER.NS", "TORNTPOWER.NS",
            # Others
            "LXCHEM.NS", "KIMS.NS", "CAMPUS.NS", "MEDPLUS.NS", "LATENTVIEW.NS"
        ]
    except Exception as e:
        print(f"Error fetching stock list: {e}")
        if exchange_filter.upper() == "NSE":
            nse_stocks = get_all_nse_stocks()
            return nse_stocks if nse_stocks else []
        return []

def fetch_stock_data(ticker, interval='1h'):
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Get real-time data
        data = stock.history(period="1mo", interval=interval)
        if data.empty:
            return pd.DataFrame()
            
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def get_company_name(ticker):
    try:
        symbol = ticker.replace('.NS', '')
        url = f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        company_name = soup.find('h2').text.strip()
        return company_name
    except:
        return ticker.replace('.NS', '')