from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
t = 0

url = 'https://chatgpt-website-nick-white.vercel.app/'
# Prevent site from closing after it loads
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the site
driver.get(url)
print(driver.title)
print(driver.current_url)

# chrome tools keep quitting program;
# infinitely not quit.
while t < 10:
	time.sleep(t)
driver.quit()