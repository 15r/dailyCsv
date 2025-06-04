import requests
from datetime import date, datetime, timedelta
import os
import logging
import zipfile
import io
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import gzip

def fetch_data(source_url, file_url, expected_files=None, id_name=None):
    try:
        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0'})
        s.get(source_url)
        source_response = s.get(f'{file_url}')

        if source_response.status_code == 200:
            if file_url.endswith(".zip"):
              file_response = s.get(file_url)
              file_name = os.path.basename(file_url)

              if file_response.status_code == 200:
                  year_folder = os.path.join(save_folder)  # Create a subdirectory for the year
                  os.makedirs(year_folder, exist_ok=True)

                  with zipfile.ZipFile(io.BytesIO(file_response.content), 'r') as zip_ref:
                      extracted_files = zip_ref.namelist()

                      for file in extracted_files:
                          if expected_files is None or file in expected_files:
                              with zip_ref.open(file) as file_in_zip:
                                  with open(os.path.join(year_folder, id_name), 'wb') as output_file:
                                      output_file.write(file_in_zip.read())
                              print(f"Saved - {file}")
              else:
                  logging.error(f"Error processing Zip {source_url}: Zip not found.")
                  print(f"{file_name}")
            else:
              file_response = s.get(file_url)
              file_name = os.path.basename(file_url)

              if file_response.status_code == 200:
                  year_folder = os.path.join(save_folder)  # Create a subdirectory for the year
                  os.makedirs(year_folder, exist_ok=True)

                  # Save the CSV file
                  csv_file_path = os.path.join(year_folder, id_name)
                  with open(csv_file_path, 'wb') as output_file:
                      output_file.write(file_response.content)
                  print(f"Saved - {file_name}")
              else:
                  logging.error(f"Error processing URL {source_url}: URL not found.")
                  print(f"{file_name}")
        else:
            logging.error(f"Error processing URL {source_url}: URL not found.")
            print(f"{file_url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error processing source {source_url}: {str(e)}")
        print(f"{source_url}")

def fetch_symbol_column(url):
    login_url = "https://www.nseindia.com/market-data/live-equity-market"
    s.get(login_url)

    encoded_url = quote(url)
    response = s.get(f'https://amzn-in.web.app/{encoded_url}.json')

    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            symbol_column = df['symbol']
            return symbol_column


def find_latest_nse_date(start_date, max_retries=2):
    current_date = start_date

    for attempt in range(max_retries):
        response = s.get(f'https://api.upstox.com/v2/market/timings/{current_date}')

        if response.status_code == 200:
            data = response.json().get("data", [])
            for market in data:
                if market.get("exchange") == "NSE":
                    return current_date  # Found NSE
        else:
            print(f"⚠️ Failed to retrieve data for {current_date}: {response.status_code}")

        # Try previous day
        current_date -= timedelta(days=1)

    # If we exhausted retries
    print("❌ NSE data not found within retry limit.")
    return None

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0'})

login_url = "https://www.nseindia.com/market-data/live-equity-market"
s.get(login_url)

# Start from yesterday
yesterday = date.today()
zipDate = find_latest_nse_date(yesterday, max_retries=5)
nseName = zipDate.strftime("%Y%m%d")

sources = {
    "NSE Equities": {
        "source_url": "https://www.nseindia.com/all-reports",
        "file_url": f"https://amzn-in.web.app/BhavCopy_NSE_CM_0_0_0_{nseName}_F_0000.csv.zip",
        "expected_files": [f"BhavCopy_NSE_CM_0_0_0_{nseName}_F_0000.csv"],
        "file_name": "nse.csv",
    },
    "NSE Derivatives": {
        "source_url": "https://www.nseindia.com/all-reports-derivatives",
        "file_url": f"https://amzn-in.web.app/BhavCopy_NSE_FO_0_0_0_{nseName}_F_0000.csv.zip",
        "expected_files": [f"BhavCopy_NSE_FO_0_0_0_{nseName}_F_0000.csv"],
        "file_name": "nfo.csv",
    },
    "BSE Equities": {
        "source_url": "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx",
        "file_url": f"https://amzn-in.web.app/BhavCopy_BSE_CM_0_0_0_{nseName}_F_0000.csv",
        "expected_files": [f"BhavCopy_BSE_CM_0_0_0_{nseName}_F_0000.csv"],
        "file_name": "bse.csv",
    },
    "ISIN": {
        "source_url": "https://www.nseindia.com/market-data/securities-available-for-trading",
        "file_url": f"https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv",
        "expected_files": [f"EQUITY_L.csv"],
        "file_name": "isin.csv",
    },
}

# Configure
logging.basicConfig(level=logging.INFO)
save_folder = "data/csv/daily"
os.makedirs(save_folder, exist_ok=True)
error_file = os.path.join('data', 'error_nse_log.csv')

# Fetch data for each source
for source_name, source_info in sources.items():
    fetch_data(source_info["source_url"], source_info["file_url"], source_info["expected_files"], source_info["file_name"])

urls = ['NIFTY 500', 'NIFTY 50', 'SECURITIES IN F&O', 'NIFTY ALPHA 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY AUTO', 'NIFTY BANK', 'NIFTY ENERGY', 'NIFTY FIN SERVICE', 'NIFTY FMCG', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY PHARMA', 'NIFTY PSU BANK', 'NIFTY PVT BANK', 'NIFTY REALTY', 'NIFTY MIDCAP 100', 'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100', 'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200', 'NIFTY FINANCIAL SERVICES 25-50', 'NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE', 'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR', 'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15', 'NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30', 'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30', 'NIFTY200 QUALITY 30', 'NIFTY ALPHA LOW-VOLATILITY 30', 'NIFTY200 MOMENTUM 30']

data_frames = []

with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
    symbol_columns = executor.map(fetch_symbol_column, urls)

for url, symbol_column in zip(urls, symbol_columns):
    if symbol_column is not None:
        data_frames.append((url, symbol_column))

if data_frames:
    combined_df = pd.DataFrame({url: symbols for url, symbols in data_frames})
    combined_df = combined_df.apply(lambda col: col.sort_values().reset_index(drop=True))
    combined_df.to_csv('data/csv/daily/indices.csv', index=False)
    print("Saved - indices.csv")
else:
    print("No data fetched from any URL.")

try:
    df = pd.read_csv('data/csv/daily/nfo.csv')
    filtered_df = df[df['FinInstrmNm'].str.endswith('FUT')]
    filtered_df.to_csv('data/csv/daily/nfo.csv', index=False)
    print("Saved - nfo.csv")
except Exception as e:
    print(f"An error occurred: {e}")

upstoxSession = requests.Session()
upstox_doc = upstoxSession.get("https://upstox.com/developer/api-documentation/instruments")
upstox_csv = upstoxSession.get("https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz", stream=True)
if upstox_csv.status_code == 200:
    with gzip.open(upstox_csv.raw, 'rb') as f:
        big_df = pd.read_json(f)
        filtered_df = big_df[big_df['instrument_type'].isin(['FUT'])]
        filtered_da = filtered_df[["segment","exchange","isin","instrument_type","instrument_key","exchange_token","trading_symbol","expiry","asset_symbol","underlying_symbol","asset_key","underlying_key"]]
        filtered_da.to_csv('data/csv/daily/up_fo.csv', index=False)
        print(f"Saved - up_fo.csv")
else:
    print(f"Failed to download file. Status Code: {upstox_csv.status_code}")
