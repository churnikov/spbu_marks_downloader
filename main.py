import time
import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from config import *

### UTILS ###
def wait_for(condition_function):
  start_time = time.time()
  while time.time() < start_time + 3:
    if condition_function():
      return True
    else:
      time.sleep(0.1)
  raise Exception(
   'Timeout waiting for'
  )

class wait_for_page_load(object):

  def __init__(self, browser):
    self.browser = browser

  def __enter__(self):
    self.old_page = self.browser.find_element_by_tag_name('html')

  def page_has_loaded(self):
    new_page = self.browser.find_element_by_tag_name('html')
    return new_page.id != self.old_page.id

  def __exit__(self, *_):
    wait_for(self.page_has_loaded)

### Loading google chrome driver.
### Might need to set absolute path

driver = webdriver.Chrome('chromedriver')

driver.get("https://my.spbu.ru/Login.aspx?ReturnUrl=%2f")

### Filling login ###

login_x_path='//*[contains(@id, \'xaf_dviUserName_Edit_I\')]'
elem = driver.find_element_by_xpath(login_x_path)
elem.send_keys(LOGIN)

### Filling password ###

password_x_path='//*[contains(@id, \'xaf_dviPassword_Edit_I\')]'
elem = driver.find_element_by_xpath(password_x_path)
elem.send_keys(PASSWORD)

### Loading main page ###

with wait_for_page_load(driver):
    elem.send_keys(Keys.RETURN)

elem = driver.find_element_by_xpath('//*[@id="Vertical_NC_NB_GHC0"]/span')
elem.click()

elem = driver.find_element_by_xpath('//*[@id="Vertical_NC_NB_I0i2_"]/span')
elem.click()

### Time to load page with marks ###
time.sleep(3)

move_to = driver.find_element_by_xpath('//*[@id="Vertical_mainMenu_Menu_DXI1_"]')
click_on = driver.find_element_by_xpath('//*[@id="Vertical_mainMenu_Menu_DXI1_T"]/span[1]')
ActionChains(driver).move_to_element(move_to).click(click_on).perform()

### Close Chrome ###

driver.close()

### If your internet connection is slow, set larger number ###

time.sleep(5)

### Set path, where Chrome would save .csv ###

with open('path/to/downloads/Оценка.csv', 'r') as f:
    dtf = pd.read_csv(f, sep=';')
    print(dtf)

os.remove('path/to/downloads/Оценка.csv')
