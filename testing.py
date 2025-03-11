from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("invalid_user")

class TestLoginRegister(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "http://localhost:8000"
        
    def test_valid_login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login.php")
        
        # Input valid credentials
        driver.find_element(By.NAME, "username").send_keys("aliya")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.find_element(By.NAME, "submit").click()
        
        # Assert redirect to index.php
        self.assertEqual(driver.current_url, f"{self.base_url}/index.php")

    def test_invalid_login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login.php")
        
        # Input invalid credentials
        driver.find_element(By.NAME, "username").send_keys("invalid_user")
        driver.find_element(By.NAME, "password").send_keys("wrong_pass")
        driver.find_element(By.NAME, "submit").click()
        
        # Assert error message
        error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Login User Gagal !!")

    def test_valid_registration(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Fill registration form
        driver.find_element(By.NAME, "name").send_keys("Test User1")
        driver.find_element(By.NAME, "email").send_keys("test@test1.com")
        driver.find_element(By.NAME, "username").send_keys("testuser1")
        driver.find_element(By.NAME, "password").send_keys("password1231")
        driver.find_element(By.NAME, "repassword").send_keys("password1231")
        driver.find_element(By.NAME, "submit").click()
        
        # Assert redirect to index.php
        self.assertEqual(driver.current_url, f"{self.base_url}/index.php")

    def test_password_mismatch_registration(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Fill form with mismatched passwords
        driver.find_element(By.NAME, "name").send_keys("Test User")
        driver.find_element(By.NAME, "email").send_keys("test@test.com")
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "repassword").send_keys("password456")
        driver.find_element(By.NAME, "submit").click()
        
        # Assert error message
        error_message = driver.find_element(By.CLASS_NAME, "text-danger").text
        self.assertEqual(error_message, "Password tidak sama !!")

    def tearDown(self):
        self.driver.quit()

class DatabaseStub:
    def __init__(self):
        self.users = {
            'aliya': {
                'password': '123',
                'email': 'nisrinaahana@gmail.com'
            }
        }
    
    def check_user(self, username):
        return username in self.users
    
    def verify_password(self, username, password):
        if username in self.users:
            return password == self.users[username]['password']
        return False

if __name__ == "__main__":
    unittest.main()
