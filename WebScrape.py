import requests
import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from slack_sdk import WebClient

def DatabaseTest():
    # Counting the number of documents in the collection
    number_of_jobs = jobs_collection.count_documents({})
    print(f'Number of jobs in the collection: {number_of_jobs}')

    #Checking if there are any documents in the collection
    if number_of_jobs > 0:
        print("Jobs were successfully inserted into the database")
    else:
        print("No jobs were inserted into the database")

# Wish to only run for 30 seconds
start_time = time.time()

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.job_db  # database name: job_db
jobs_collection = db.jobs # collection name: jobs

# Connect to slack channel
slack_client = WebClient(token='sunt-1839578395720-3893929450644-g7vxF971tArBsKNmn3JusVTB')
channel_id = '#shift-notifier' # 'channel name' or you can use the channel id

# Establish connection
url = 'www.google.com'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Set the driver to maximum zoom, because later I need to read all html the code doesn't let me scrape/see
driver.get('chrome://settings/')
driver.execute_script('chrome.settingsPrivate.setDefaultZoom(.25);')

# Navigate to the site
driver.get(url)
print(driver.title)
print(driver.current_url)

# Find html for login
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "signOnButtonSpan")

# Auto login
username.send_keys("USERNAME") # username
password.send_keys("PASSWORD") # password
login_button.click()

# Find CESE tab at the top, and click on it
cese_element = driver.find_element(By.XPATH, '//a[@data-original-title="ShiftBoard"]')
cese_element.click()

# Reconnect to full report
full_report = 'www.google.com'
driver.get(full_report)

# Find the table, loop through each element in said table
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tableBody")))

# Define field names for key:value pair
field_names = ["field1", "field2", "field3", "field4", "field5", "field6", "field7", "field8"]

for row in table.find_elements(By.TAG_NAME,"tr"):
    cells = row.find_elements(By.TAG_NAME,"td")
    data = [cell.text for cell in cells]

    # Only want requests with this day. 
    if len(data) == 8 and 'Tuesday' in data:
        # Create a unique ID with the employee name, employee message, and the date:
        unique_id = data[5] + data[3] + data[4] 

        # Combine field data (using zip) and set id
        document = dict(zip(field_names, data))
        document["_id"] = unique_id

        # Check if in mongodb, and if not, insert it into the database.
        if jobs_collection.find_one({"_id": unique_id}) is None:
            # Use the $push operator to add the elements of the list to the array field
            jobs_collection.update_one({"_id": unique_id}, {"$set": document}, upsert=True)
            print(data)
            #Slack API bot sending out a notification of a unique entry.
            # New job posted by John Smith! Message: "Message me!"
            slack_client.chat_postMessage(channel=channel_id, text="New job posted by " + data[3] + "! Message: " + data[4] + " Date: " + data[5])

# DatabaseTest() 

# Quit after 30 seconds
elapsed_time = time.time() - start_time
if elapsed_time >= 30:
    driver.quit()
