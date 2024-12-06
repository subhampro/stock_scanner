import matplotlib
matplotlib.use('Agg')
# Configure matplotlib to use a non-interactive backend
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import mplfinance as mpf
from io import BytesIO
import base64

def plot_candlestick(data, ticker, company_name):
    try:
        # Set style configuration for dark theme
        mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350',
                                edge='inherit',
                                wick='inherit',
                                volume='in',
                                ohlc='inherit')
        s = mpf.make_mpf_style(marketcolors=mc, 
                              gridstyle='', 
                              facecolor='#0d1117',
                              figcolor='#0d1117',
                              y_on_right=True)
        
        # Create figure
        buf = BytesIO()
        
        # Create the candlestick chart with adjusted parameters
        fig, _ = mpf.plot(data, 
                         type='candle',
                         style=s,
                         title=f'\n{company_name} ({ticker})',
                         volume=True,
                         returnfig=True,
                         figsize=(12, 8),
                         tight_layout=True)
        
        # Save to buffer
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#0d1117')
        plt.close(fig)
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Error plotting chart for {ticker}: {str(e)}")
        # Create error figure
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0d1117')
        ax.text(0.5, 0.5, f"Error plotting chart: {str(e)}", 
                ha='center', va='center', color='white')
        ax.set_facecolor('#0d1117')
        buf = BytesIO()
        fig.savefig(buf, format='png', facecolor='#0d1117')
        plt.close(fig)
        buf.seek(0)
        return buf

# To install mplfinance, run the following command:
# pip install mplfinance