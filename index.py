import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/"
}
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20NEXT%2050"

with requests.Session() as session:
    # This first request is necessary to set cookies
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    print(response.text)  # This is the JSON data
