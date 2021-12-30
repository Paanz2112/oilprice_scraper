import re
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from utills import *

#web
url = "http://gasprice.kapook.com/gasprice.php#bcp"
options = Options()
options.headless = False


with webdriver.Firefox(executable_path='C:/WebDriver/bin/geckodriver',options=options) as driver:
# with webdriver.Firefox(options=options) as driver:
    
    # Tell driver to open website
    driver.get(url)
    print(driver.title)
    print(datetime.now())
    # wait for data
    time.sleep(20)

    conn,cur = database_connect()
    col = "id SERIAL, brand VARCHAR,oil_type VARCHAR, oil_price FLOAT, scraping_date timestamp with time zone"
    db_operation(cur,"create",col)
    brandlist = ["ptt","bcp","shell","esso","caltex","irpc","pt","susco","pure","suscodealers",]
    
    data = []
    for brand in brandlist:

        ## oil price
        oil_type = driver.find_elements(By.XPATH, f"""//section[contains (@class, 'container')]//article[contains (@class, 'gasprice {brand}')]//ul//li//span""")
        oil_price = driver.find_elements(By.XPATH, f"""//section[contains (@class, 'container')]//article[contains (@class, 'gasprice {brand}')]//ul//li//em""")
        print(f"""                    Oil price from {brand}""")
        for d in range(len(oil_type)):
            print("oil type: ",oil_type[d].text," | ","oil price: ",oil_price[d].text)
            data.append((brand, oil_type[d].text, float(oil_price[d].text),datetime.now().strftime('%Y-%m-%d %H:%M:%S%z')))
    db_operation(cur,"insert",data)

driver.quit()
cur.close()
print('yay')