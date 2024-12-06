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
        plt.close('all')  # Clear any existing plots
        
        # Set up dark theme colors
        mc = mpf.make_marketcolors(
            up='#26a69a', down='#ef5350',
            edge='inherit', wick='inherit',
            volume='in', ohlc='inherit'
        )
        s = mpf.make_mpf_style(
            base_mpf_style='dark',
            marketcolors=mc,
            gridstyle='',
            facecolor='#0d1117',
            figcolor='#0d1117',
            gridcolor='#30363d'
        )
        
        # Plot to memory
        buf = BytesIO()
        fig, _ = mpf.plot(
            data,
            type='candle',
            style=s,
            title=f'\n{company_name} ({ticker})',
            volume=True,
            returnfig=True,
            figsize=(12, 8),
            tight_layout=True,
            panel_ratios=(3, 1)
        )
        
        # Save and return
        fig.patch.set_facecolor('#0d1117')
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#0d1117')
        plt.close(fig)
        buf.seek(0)
        return buf
        
    except Exception as e:
        print(f"Error plotting {ticker}: {str(e)}")
        return None

# To install mplfinance, run the following command:
# pip install mplfinance