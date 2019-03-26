import time
import os
import argparse
import json
import logging
import platform

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

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

logger = logging.getLogger('Marks_downloader')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

parser = argparse.ArgumentParser()
parser.add_argument('--config_path', default='config.json')
args = parser.parse_args()

logger.debug('reading config')
with open(args.config_path, 'r') as f:
    params = json.load(f)

sleep_time = params['sleep_time']

if platform.system() in ('Darwin', 'Linux'):
    save_dir = dlPth=os.path.join(os.getenv('HOME'), 'Downloads')
    driver_path = params['driver_path'] or os.path.join(os.path.abspath(__file__).split('/')[:-1], 'chromedriver')
else:
    raise RuntimeError(f'{platform.system()} is not supported')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'download.default_directory={save_dir}')
with webdriver.Chrome(params['driver_path'], options=chrome_options) as driver:

    driver.get("https://my.spbu.ru/Login.aspx?ReturnUrl=%2f")

    logger.debug('Filling login')

    login_x_path='//*[contains(@id, \'xaf_dviUserName_Edit_I\')]'
    elem = driver.find_element_by_xpath(login_x_path)
    elem.send_keys(params['login'])

    logger.debug('Filling password')

    password_x_path='//*[contains(@id, \'xaf_dviPassword_Edit_I\')]'
    elem = driver.find_element_by_xpath(password_x_path)
    elem.send_keys(params['password'])

    logger.debug('Loading main page')

    with wait_for_page_load(driver):
        elem.send_keys(Keys.RETURN)

    logger.debug('Getting marks page')
    elem = driver.find_element_by_xpath('//*[@id="Vertical_NC_TL_N2"]')
    elem.click()

    time.sleep(sleep_time)

    logger.debug('Switching languages')
    elem = driver.find_element_by_xpath('//*[@id="Vertical_SAC_Menu_ITCNT0_xaf_a0_Cb_I"]')
    elem.click()

    time.sleep(sleep_time)
    elem = driver.find_element_by_xpath('//*[@id="Vertical_SAC_Menu_ITCNT0_xaf_a0_Cb_DDD_L_LBI1T0"]')
    elem.click()
    time.sleep(sleep_time)

    logger.debug('Downloaing marks')
    action = ActionChains(driver)
    move_to = driver.find_element_by_xpath('//*[@id="Vertical_mainMenu_Menu_DXI3_P"]')
    click_on = driver.find_element_by_xpath('//*[@id="Vertical_mainMenu_Menu_DXI2_"]')
    action.move_to_element(move_to).perform()
    time.sleep(sleep_time)
    action.move_to_element(click_on).perform()
    click_on.click()

    time.sleep(sleep_time)

marks_path = os.path.join(save_dir, params['marks_file_name'])

with open(marks_path, 'r') as f:
    dtf = pd.read_csv(f, sep=';')
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.max_colwidth', 100):
        print(dtf)

os.remove(marks_path)
