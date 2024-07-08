import time
import random
from logging import config, getLogger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from const import SEARCH_BASIC_CONDITIONS_SELECT_OPTIONS, SEARCH_ADDRESS_STATION_INFO, \
    SEARCH_BUTTON_XPATH, SEARCH_DAYS_RADIO_BUTTONS, SEARCH_ONE_TOUCH_OPTIONS, LOAD_ONE_TOUCH_OPTIONS
from scraper import Scraper

logger = getLogger(__name__)

class Search(Scraper):
    
    def input_select_options(self, xpath_select_options_dict):
        # Wait the last element of the dictionary
        last_xpath = list(xpath_select_options_dict.keys())[-1]
        logger.info(f"waiting last_xpath: {last_xpath}")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, last_xpath)))       
        
        for xpath, value in xpath_select_options_dict.items():
            select = Select(self.driver.find_element(By.XPATH, xpath))
            select.select_by_visible_text(value)
            logger.info(f'input "{value}" into xpath: {xpath}')
            # time.sleep(random.randint(1, 3))
    
    def input_values(self, xpath_values_dict):
        last_xpath = list(xpath_values_dict.keys())[-1]
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, last_xpath)))            

        for xpath, value in xpath_values_dict.items():
            self.driver.find_element(By.XPATH, xpath).send_keys(value)
            logger.info(f'input "{value}" into xpath: {xpath}')
            # time.sleep(random.randint(1, 3))
            
    def input_radio_buttons(self, xpath_radio_buttons):
        last_xpath = list(xpath_radio_buttons.keys())[-1]
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, last_xpath))) 
            # self.driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset - 100);", last_xpath)
        
        for xpath in xpath_radio_buttons.keys():
            print(xpath)
            radio_button = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].click();", radio_button)

    def select_modal_ok(self):
        wait = WebDriverWait(self.driver, 20) 
        try:            
            modal_present = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.modal.show')))
            logger.info("modal presented")
            
            # Wait for the modal to be visible
            modal_visible = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.modal.show')))
            logger.info("modal visible")
            
            # Locate the "OK" button within the modal
            ok_button = modal_visible.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
            # Click the "OK" button
            ok_button.click()
            time.sleep(5)
            
            logger.info("OK button clicked successfully.")
        except Exception as e:
            print(f"Exception: {e}")
            raise e        

    def search_properties_for_sale(self):

        self.input_select_options(SEARCH_BASIC_CONDITIONS_SELECT_OPTIONS)
        self.input_values(SEARCH_ADDRESS_STATION_INFO)
        self.input_radio_buttons(SEARCH_DAYS_RADIO_BUTTONS)
        
        self.driver.find_element(By.XPATH, SEARCH_BUTTON_XPATH).click()
        logger.info("Search button was clicked")
        
        self.select_modal_ok()        
        time.sleep(5)
        
    def search_properties_for_sale_from_menu(self):
        wait = WebDriverWait(self.driver, 10)
        
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/a/span[1]')))
            display_search_condition = self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/a/span[1]')
            display_search_condition.click()
                    
            self.input_select_options(SEARCH_ONE_TOUCH_OPTIONS)
            wait.until(EC.presence_of_element_located((By.XPATH, LOAD_ONE_TOUCH_OPTIONS)))
            load_button = self.driver.find_element(By.XPATH, LOAD_ONE_TOUCH_OPTIONS)
            load_button.click()
            
            self.select_modal_ok()
            
            self.driver.find_element(By.XPATH, SEARCH_BUTTON_XPATH).click()
            logger.info("Search button was clicked")
                
        except Exception as e:
            print(f"Exception: {e}")
            raise e
        
        time.sleep(3)
