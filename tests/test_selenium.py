import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DjangoAppTests(unittest.TestCase):
    def setUp(self):
        # Initialize Selenium WebDriver (replace 'chromedriver' with the path to your WebDriver executable)
        self.driver = webdriver.Chrome('C:\Program Files\chromedriver.exe')
        self.driver.implicitly_wait(10)  # Implicit wait for 10 seconds

    def tearDown(self):
        # Close the browser window
        self.driver.quit()

    def test_login_and_navigation(self):
        # Open the login page
        self.driver.get('http://localhost:8000/login/')

        # Find the username and password input fields and submit button
        username_field = self.driver.find_element_by_name('username')
        password_field = self.driver.find_element_by_name('password')
        submit_button = self.driver.find_element_by_xpath("//input[@type='submit']")

        # Enter login credentials
        username_field.send_keys('your_username')
        password_field.send_keys('your_password')

        # Submit the login form
        submit_button.click()

        # Wait for the dashboard page to load
        WebDriverWait(self.driver, 10).until(EC.url_contains('dashboard'))

        # Assert that the dashboard page is loaded
        self.assertIn('dashboard', self.driver.current_url)

        # Example: Navigate to another page (replace '/profile/' with the URL of the page you want to navigate to)
        self.driver.get('http://localhost:8000/profile/')

        # Example: Assert that the profile page is loaded
        WebDriverWait(self.driver, 10).until(EC.url_contains('profile'))
        self.assertIn('profile', self.driver.current_url)

if __name__ == '__main__':
    unittest.main()