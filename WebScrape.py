import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

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

# Establish connection, then parse the text
url = 'https://chatgpt-website-nick-white.vercel.app/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

job_titles = soup.find_all("div", {"class": "job"})

for title in job_titles:
    position = title.find("h2", {"class": "job-title"}) # Note:job-title is from the html on *this* site; prepare to change it.
    location = title.find("div", {"class": "job-location"})

    #Check for job and location
    if position and location and "Full Stack Developer" in position.text and "NY" in location.text:
        job_title = position.text.strip()
        job_location = location.text.strip()
        print(f'{job_title} in {job_location}')

        # Check if the job already exists in the database
        if not jobs_collection.find_one({'title': job_title, 'location': job_location}):
            # Insert the job into the database
            jobs_collection.insert_one({'title': job_title, 'location': job_location})
            print(f'{job_title} in {job_location} added to the database')
        else:
            print(f'{job_title} in {job_location} already exists in the database')
    else:
        print("No Matching Job Found")

DatabaseTest()

cards = soup.find_all('div', class_='job-card')
print(response.main)
for card in cards:
    print(card.find("h2", {"class": "job-title"}))