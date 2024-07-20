import csv
import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config['DEFAULT']

def load_test_data():
    with open('data/test_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def setup_driver():
    return webdriver.Chrome()

def test_product_search_and_details():
    config = load_config()
    test_data = load_test_data()
    driver = setup_driver()

    try:
        driver.get(config['base_url'])
        print(f"Navigated to {config['base_url']}")
        time.sleep(2)

        for data in test_data:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search"))
            )
            search_box.clear()
            time.sleep(1)
            search_box.send_keys(data['product_name'])
            time.sleep(1)
            search_box.send_keys(Keys.RETURN)
            print(f"Searched for product: {data['product_name']}")
            time.sleep(2)

            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-thumb"))
            )
            assert result, f"No results found for {data['product_name']}"
            print(f"Search results found for {data['product_name']}")

            product_title = result.find_element(By.CSS_SELECTOR, ".caption h4 a").text
            assert data['product_name'].lower() in product_title.lower(), f"Expected product not found: {data['product_name']}"
            print(f"Product '{product_title}' matches the search term '{data['product_name']}'")

            # Click on the product to go to its detail page
            result.find_element(By.CSS_SELECTOR, ".caption h4 a").click()
            time.sleep(2)

            # Image browsing for iPhone only
            if data['product_name'].lower() == 'iphone':
                # Click on the main product image to open the image gallery
                main_image = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".thumbnails > li:first-child > a"))
                )
                main_image.click()
                time.sleep(2)

                # Click the "Next" button 5 times
                for i in range(5):
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mfp-arrow.mfp-arrow-right"))
                    )
                    next_button.click()
                    time.sleep(1)
                    print(f"Clicked 'Next' button: {i+1} of 5 times")

                # Close the image gallery
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mfp-close"))
                )
                close_button.click()
                time.sleep(2)

            # Add to cart
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "button-cart"))
            )
            add_to_cart_button.click()
            time.sleep(2)

            # Verify product added to cart
            success_alert = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
            )
            assert "Success: You have added" in success_alert.text
            print(f"Successfully added {product_title} to cart")

            # Open the cart page
            cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#cart > button"))
            )
            cart_button.click()
            time.sleep(1)

            view_cart_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "p.text-right > a:nth-child(1)"))
            )
            view_cart_link.click()
            time.sleep(2)

            # Verify we're on the cart page
            assert "Shopping Cart" in driver.title
            print("Successfully opened the cart page")

            # Go back to home page for next search
            driver.get(config['base_url'])
            time.sleep(2)

        print("All tests passed successfully!")

    except Exception as e:
        print(f"Test failed: {str(e)}")

    finally:
        input("Press Enter to close the browser...")
        driver.quit()
        print("WebDriver session ended")

if __name__ == "__main__":
    test_product_search_and_details()