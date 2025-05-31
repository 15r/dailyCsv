from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Visit the homepage first to set cookies
driver.get("https://www.nseindia.com")
time.sleep(2)  # Wait for cookies to be set

# Set headers (User-Agent is especially important)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

# Now access the API endpoint
api_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20NEXT%2050"
driver.get(api_url)

# The response will be in page_source (since it's JSON, just print it)
print(driver.page_source)

driver.quit()
