from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get('https://quotes.toscrape.com/scroll')

WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))


body_height = driver.execute_script("return document.body.scrollHeight")


while True:
    driver.execute_script(f"window.scrollTo(0, {body_height});")


    time.sleep(3)
 

    new_height = driver.execute_script("return document.body.scrollHeight")
    print (new_height)
    if new_height == body_height:
        break
    body_height = new_height
    print (body_height)



quotes = driver.find_elements(By.CLASS_NAME,'quote')
print(quotes)
print(f'Количество цитат равно {len(quotes)}')


driver.quit()