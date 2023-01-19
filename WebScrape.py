import requests
from bs4 import BeautifulSoup

url = 'https://www.indeed.com/jobs?q=software+developer&l=New+York'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

job_titles = soup.find_all('a', {'class': 'jobtitle'})

for title in job_titles:
    print(title.text)
