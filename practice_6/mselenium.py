from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import  time

#options = webdriver.EdgeOptions()
#options.add_argument("--headless")
#options.add_argument("--no-sandbox")
#options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Firefox()

driver.get('https://selenium.dev/')
WebDriverWait(driver, 30)
time.sleep(3)

driver.get('https://selenium.dev/documentation')
#assert 'Selenium' in driver.title
WebDriverWait(driver, 120)
print(driver.title)
time.sleep(3)

elem = driver.find_element(By.ID, 'm-documentationwebdriver')
elem.click()
WebDriverWait(driver, 120)

time.sleep(3)


assert 'WebDriver' in driver.title
print(driver.title)



email_input = driver.find_element(By.XPATH, '//li[@data-bs-original-title="Software Freedom Conservancy"]/a')
print(email_input.get_attribute("href"))

driver.quit()