import unittest
import requests

class TestUrlConnection(unittest.TestCase):
    def test_url_connection(self):
        url = 'https://chatgpt-website-nick-white.vercel.app/'
        # When given a login:
        # payload = {'username': 'myusername', 'password': 'mypassword'}
        # response = requests.post(login_url, data=payload)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        print(response.headers)

if __name__ == '__main__':
    unittest.main()
