import requests
import unittest
from bs4 import BeautifulSoup
from pymongo import MongoClient

class TestUrlConnection(unittest.TestCase):
    def test_url_connection():
        url = 'https://chatgpt-website-nick-white.vercel.app/'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        print(response.headers)


TestUrlConnection.test_url_connection()

# Connect to the MongoDB database
client = MongoClient()
db = client.job_db  # database name: job_db
jobs_collection = db.jobs # collection name: jobs

# Establish connection, then parse the text
url = 'https://chatgpt-website-nick-white.vercel.app/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

job_titles = soup.find_all('h3', {'class': 'job-title'})

for title in job_titles:
    job_title = title.text.strip()
    print(job_title)
    # Check if the job already exists in the database
    if not jobs_collection.find_one({'title': job_title}):
        # Insert the job into the database
        jobs_collection.insert_one({'title': job_title})
        print(f'{job_title} added to the database')
    else:
        print(f'{job_title} already exists in the database')
