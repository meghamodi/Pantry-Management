from django.shortcuts import render
from django.http import HttpResponse
from .app import main
from .scraping import connection
from selenium import webdriver

def barcode_scan(request):
    # Render the barcode scanner HTML page
    return render(request, 'barcode_scan.html')

def scan_and_insert(request):
    # Get the product ID from the barcode scanner
    product_id = main()

    # Scrape the product details from the website using Selenium
    cursor = connection.cursor()
    driver = None
    try:
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        driver.implicitly_wait(3)
        driver.get("https://www.barcodelookup.com/{}".format(product_id))
        driver.implicitly_wait(2)
        product_details = driver.find_element(By.XPATH,"//*[@id='product']/section[2]/div[1]/div/div/div[2]/h4")
        product = product_details.text
    except:
        # Handle any exceptions that occur during scraping
        product = None
    finally:
        if driver:
            driver.quit()

    if product:
        # Insert the product details into the database
        mySql_insert_query = "INSERT INTO pantry (item_barcode,item_name) VALUES (%s, %s)"
        values = (product_id, product)
        cursor.execute(mySql_insert_query, values)
        connection.commit()
        return HttpResponse("Product added to pantry")
    else:
        return HttpResponse("Error scraping product details")

# def barcode_scanner(request):
#     # Get the product ID from the barcode scanner
#     product_id = main()

#     # Scrape the product details from the website using Selenium
#     cursor = connection.cursor()
#     driver = None
#     try:
#         driver = webdriver.Chrome('/usr/local/bin/chromedriver')
#         driver.implicitly_wait(3)
#         driver.get("https://www.barcodelookup.com/{}".format(product_id))
#         driver.implicitly_wait(2)
#         product_details = driver.find_element(By.XPATH,"//*[@id='product']/section[2]/div[1]/div/div/div[2]/h4")
#         product = product_details.text
#     except:
#         # Handle any exceptions that occur during scraping
#         product = None
#     finally:
#         if driver:
#             driver.quit()

#     if product:
#         # Insert the product details into the database
#         mySql_insert_query = "INSERT INTO pantry (item_barcode,item_name) VALUES (%s, %s)"
#         values = (product_id, product)
#         cursor.execute(mySql_insert_query, values)
#         connection.commit()
#         return HttpResponse("Product added to pantry")
#     else:
#         return HttpResponse("Error scraping product details")

