# Setup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Visit homepage to set cookies
driver.get("https://www.nseindia.com")
# Optional: sleep for 2 seconds

# Set User-Agent (to mimic real browser)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": "Mozilla/5.0 ..."
})

# Visit API endpoint
driver.get("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20NEXT%2050")
print(driver.page_source)  # This is the JSON data

driver.quit()
