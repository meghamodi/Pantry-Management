from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .app import main
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


import mysql.connector as mysql


def scan_and_insert():
    # Scraping barcode scanner from the website, automating it using selenium
    print("📷 Launching scanner...")
    product_id = main()
    print("productid",product_id)
    if not product_id or product_id.strip() == "":
        print("⚠️ No barcode detected.")
        return None, "No barcode detected"
    chrome_options = Options()
    chrome_options.binary_location = "/Users/meghamodi/Downloads/chrome-mac-arm64-2/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"


    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service,  options=chrome_options)
    try:
        url = f"https://world.openfoodfacts.org/product/{product_id}"
        print("🧪 Product page URL:", url)
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        product_details = wait.until(EC.presence_of_element_located((
        By.XPATH, "//*[@id='product']/div/div/div[2]/div/div[2]/h2"
    ))) 
        product = product_details.text.strip()
        print("✅ Scraped product:", product)
    #     driver.quit()
    #     return product_id, product

        
    
        mySql_insert_query = "INSERT INTO pantry (item_barcode,item_name) VALUES (%s, %s)"
        values = (product_id, product)
        # Connectivity to the database
        connection = mysql.connect(host="localhost",
                        user="root",
                        passwd="",
                        db="inventory")
        cursor = connection.cursor()
        print(mySql_insert_query)

        # executing the query with values
        cursor.execute(mySql_insert_query, values)
        connection.commit()
        print("✅ Inserted:", values)

        print(cursor.rowcount, "record inserted")
    except Exception as e:
        print("❌ Failed to scrape product details:", str(e))
        driver.quit()
        return product_id, f"Error scraping product: {str(e)}"