import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver

def DatabaseTest():
    # Counting the number of documents in the collection
    number_of_jobs = jobs_collection.count_documents({})
    print(f'Number of jobs in the collection: {number_of_jobs}')

    #Checking if there are any documents in the collection
    if number_of_jobs > 0:
        print("Jobs were successfully inserted into the database")
    else:
        print("No jobs were inserted into the database")


# Connect to the MongoDB database
client = MongoClient()
db = client.job_db  # database name: job_db
jobs_collection = db.jobs # collection name: jobs

# Establish connection
url = 'https://chatgpt-website-nick-white.vercel.app/'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the site
driver.get(url)
print(driver.title)
print(driver.current_url)

# init soup for html parsing
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

## implementation details for webscraping in beautiful soup go here
job_locations = soup.find_all("p", {"class": "job-location"})
for location in job_locations:
    print(location.text)

DatabaseTest()

t = 0
# chrome tools keep quitting program;
# infinitely not quit.
while t < 10:
    time.sleep(t)
driver.quit()