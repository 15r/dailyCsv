from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.nseindia.com")
    time.sleep(5)  # Wait for the page to load and cookies to set

    # Now download the file directly with cookies from the browser
    cookies = driver.get_cookies()
    cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

    url = 'https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_20250526_F_0000.csv.zip'
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Cookie', cookie_header)
    urllib.request.urlretrieve(url, 'BhavCopy_20250526.zip')

    print("✅ Download completed with Selenium cookies!")

finally:
    driver.quit()
