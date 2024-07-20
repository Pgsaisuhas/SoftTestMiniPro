import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import unittest

def load_config():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config['DEFAULT']

def setup_driver():
    return webdriver.Chrome()

def generate_unique_email():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{timestamp}@gmail.com"

class TestUserRegistration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.driver = setup_driver()
        cls.driver.get(cls.config['base_url'])
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("WebDriver session ended")

    def test_1_register_user(self):
        print("\nTesting user registration...")
        self.driver.find_element(By.XPATH, "//a[@title='My Account']").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "input-firstname").send_keys("John")
        self.driver.find_element(By.ID, "input-lastname").send_keys("Doe")
        self.driver.find_element(By.ID, "input-email").send_keys(generate_unique_email())
        self.driver.find_element(By.ID, "input-telephone").send_keys("1234567890")
        self.driver.find_element(By.ID, "input-password").send_keys("password123")
        self.driver.find_element(By.ID, "input-confirm").send_keys("password123")
        self.driver.find_element(By.NAME, "agree").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//input[@value='Continue']").click()
        time.sleep(2)

        success_text = self.driver.find_element(By.XPATH, "//div[@id='content']/h1").text
        self.assertEqual(success_text, "Your Account Has Been Created!")
        print("User registration successful")
        time.sleep(2)

if __name__ == "__main__":
    unittest.main()
