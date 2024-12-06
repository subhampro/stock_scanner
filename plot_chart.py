import matplotlib
matplotlib.use('Agg')
import mplfinance as mpf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot_candlestick(data, ticker, company_name):
    try:
        # Clear any existing plots
        plt.close('all')
        
        # Create a BytesIO object to store the image
        buf = BytesIO()
        
        # Create the candlestick chart
        mpf.plot(data, 
                type='candle', 
                style='charles',
                title=f"{company_name} ({ticker})",
                volume=True,
                savefig=buf,
                figsize=(12, 8))
        
        # Return the image bytes
        buf.seek(0)
        return buf
                
    except Exception as e:
        print(f"Error plotting chart for {ticker}: {str(e)}")
        # Create a blank figure if plotting fails
        plt.figure(figsize=(12, 8))
        plt.text(0.5, 0.5, f"Error plotting chart: {str(e)}", 
                ha='center', va='center')
        buf = BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        plt.close()
        return buf

# To install mplfinance, run the following command:
# pip install mplfinance