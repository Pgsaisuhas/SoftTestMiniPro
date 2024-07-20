# SoftTestMiniPro

E-commerce Product Search Test
This project contains automated tests for the product search functionality of the TutorialsNinja demo e-commerce website.
Setup

Install Python 3.7 or higher.
Install the required packages:
Copypip install -r requirements.txt

Download and install the appropriate ChromeDriver for your system and ensure it's in your PATH.

Running the tests
To run the tests, execute the following command from the project root directory:
Copypython tests/test_product_search.py
Configuration

The base URL for the website is configured in config/config.ini.
Test data (product names to search for) is stored in data/test_data.csv.

Adding more tests
To add more product search tests, simply add new rows to the data/test_data.csv file with the product names you want to search for.