from selenium import webdriver
import time
t = 0

url = 'https://chatgpt-website-nick-white.vercel.app/'

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