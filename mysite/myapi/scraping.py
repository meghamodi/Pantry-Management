from selenium import webdriver
from .app import main
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import mysql.connector as mysql

# Connectivity to the database
connection = mysql.connect(host="localhost",
                     user="root",
                     passwd="modimac123+",
                     db="inventory")

barcode_text = ""
driver = webdriver.Chrome('/usr/local/bin/chromedriver')
# Scraping barcode scanner from the website, automating it using selenium
product_id = main()
print("product_id",product_id)
driver.implicitly_wait(3)
driver.get("https://www.barcodelookup.com/{}".format(product_id))
driver.implicitly_wait(2)
product_details = driver.find_element(By.XPATH,"//*[@id='product']/section[2]/div[1]/div/div/div[2]/h4")
product = product_details.text
print("product_name",product)

driver.quit()
mySql_insert_query = "INSERT INTO pantry (item_barcode,item_name) VALUES (%s, %s)"
values = (product_id, product)

cursor = connection.cursor()
print(mySql_insert_query)

# executing the query with values
cursor.execute(mySql_insert_query, values)
connection.commit()

print(cursor.rowcount, "record inserted")