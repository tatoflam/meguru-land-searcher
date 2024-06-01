import time
import random
from logging import config, getLogger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from const import SEARCH_BASIC_CONDITIONS_SELECT_OPTIONS, SEARCH_ADDRESS_STATION_INFO, SEARCH_BUTTON_XPATH
from scraper import Scraper

logger = getLogger(__name__)

class Search(Scraper):
    
    def input_select_options(self, xpath_select_options_dict):
        # Wait the last element of the dictionary
        last_xpath = list(xpath_select_options_dict.keys())[-1]
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, last_xpath)))       
        
        for xpath, value in xpath_select_options_dict.items():
            select = Select(self.driver.find_element(By.XPATH, xpath))
            select.select_by_visible_text(value)
            logger.info(f'input "{value}" into xpath: {xpath}')
            time.sleep(random.randint(1, 3))
    
    def input_values(self, xpath_values_dict):
        last_xpath = list(xpath_values_dict.keys())[-1]
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, last_xpath)))            

        for xpath, value in xpath_values_dict.items():
            self.driver.find_element(By.XPATH, xpath).send_keys(value)
            logger.info(f'input "{value}" into xpath: {xpath}')
            time.sleep(random.randint(1, 3))

    def search_properties_for_sale(self):
        self.input_select_options(SEARCH_BASIC_CONDITIONS_SELECT_OPTIONS)
        self.input_values(SEARCH_ADDRESS_STATION_INFO)
        self.driver.find_element(By.XPATH, SEARCH_BUTTON_XPATH).click()
        time.sleep(20)
        # TODO: handle popup window for the search result confirmation and click "OK"