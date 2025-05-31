from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Correct Service-based initialization for Selenium 4+
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Visit homepage to set cookies/session
driver.get("https://www.nseindia.com")
time.sleep(2)  # Let cookies/session load

# Set a modern User-Agent to mimic a real browser
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

# Visit API endpoint and print JSON response
api_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20NEXT%2050"
driver.get(api_url)
print(driver.page_source)

driver.quit()
