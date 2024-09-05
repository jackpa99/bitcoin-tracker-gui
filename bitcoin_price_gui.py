import requests
import tkinter as tk
from time import sleep
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(filename='bitcoin_price.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'bitcoin' in data and 'usd' in data['bitcoin']:
                return data['bitcoin']['usd']
            else:
                logging.error(f"Missing 'bitcoin' or 'usd' key in response: {data}")
                return None
        else:
            logging.error(f"HTTP Error: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def update_price_label():
    price = get_bitcoin_price()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if price is not None:
        price_label.config(text=f"Bitcoin Price: ${price}\nRetrieved at: {current_time}")
    else:
        price_label.config(text=f"Error fetching price\nLast attempt: {current_time}")
    
    root.after(10000, update_price_label)

def on_closing():
    logging.info("Application closed by user.")
    root.destroy()  # This will properly close the tkinter window and stop the app

root = tk.Tk()
root.title("Bitcoin Price Tracker")

price_label = tk.Label(root, text="Bitcoin Price: Loading...", font=("Helvetica", 24))
price_label.pack(pady=20)

# Call the on_closing function when the window is closed
root.protocol("WM_DELETE_WINDOW", on_closing)

update_price_label()

root.mainloop()
