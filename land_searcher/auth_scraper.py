import os
import time
from selenium.webdriver.support import expected_conditions as EC
from logging import config, getLogger

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from const import LOGIN_ID_XPATH, LOGIN_PASSWORD_XPATH, LOGIN_GUIDELINE_CHECK_XPATH, \
    LOGIN_BUTTON_XPATH, LOGOFF_LINK_XPATH, HAMBURGER_MENU_BUTTON_XPATH, \
    LOGOFF_LINK_IN_SEARCH_XPATH, HAMBURGER_MENU_BUTTON_IN_SEARCH_XPATH
from scraper import Scraper

logger = getLogger(__name__)

class Auth(Scraper):

    def login(self):
        login_url = os.environ["LOGIN_URL"]
        login_id = os.environ["ID"]
        login_password = os.environ["PASSWORD"]
        
        self.driver.get(login_url)
        element = WebDriverWait(self.driver, 10).until(
            # EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
            EC.visibility_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
        )
        # if EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH)):
        #    logger.info('Login is clickable')
        logger.info('Login is clickable')
        
        self.driver.find_element(By.XPATH, LOGIN_ID_XPATH).send_keys(login_id)
        self.driver.find_element(By.XPATH, LOGIN_PASSWORD_XPATH).send_keys(login_password)
        
        # For clicking the checkbox, needed to use ActionChain 
        action = ActionChains(self.driver)
        login_guideline_checkbox = self.driver.find_element(By.XPATH, LOGIN_GUIDELINE_CHECK_XPATH)
        action.click(login_guideline_checkbox).perform()
                
        self.driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()
        logger.info('Login completed')

    # TODO: implement logoff function. Need to find the way to toggle the hamburger selector with "show" class
    def logoff(self):
        try: 
            action = ActionChains(self.driver)
            time.sleep(5)
            if EC.element_to_be_clickable((By.XPATH, HAMBURGER_MENU_BUTTON_IN_SEARCH_XPATH)):
                logger.info('hamburger menu is search screen clickable')

                # hamburger_menu_button = driver.find_element(By.XPATH, HAMBURGER_MENU_BUTTON_IN_SEARCH_XPATH)
                #__layout > div > div.p-frame-header > div > div > div.p-frame-navbar-right > button
                # hamburger_menu_button = driver.find_element(By.CSS_SELECTOR, "div.p-frame-navbar-right")
                
                # This fails
                logoff_link = self.driver.find_element(By.XPATH, LOGOFF_LINK_IN_SEARCH_XPATH)
                
                #time.sleep(5)
                #action.click(hamburger_menu_button)
                time.sleep(5)
                action.click(logoff_link)

                #elem=WebDriverWait(driver,5000).until(EC.visibility_of_element_located(
                #    (By.XPATH, "HAMBURGER_MENU_BUTTON_IN_SEARCH_XPATH")))
                # driver.execute_script("arguments[0].scrollIntoView();",elem)

            # elif EC.element_to_be_clickable((By.XPATH, HAMBURGER_MENU_BUTTON_XPATH)):
            else:
                logger.info('hamburger menu clickable')
                
                hamburger_menu_button = self.driver.find_element(By.XPATH, HAMBURGER_MENU_BUTTON_XPATH)
                logoff_link = self.driver.find_element(By.XPATH, LOGOFF_LINK_XPATH)
                time.sleep(5)
                action.click(hamburger_menu_button)
                time.sleep(5)
                action.click(logoff_link)
            
            action.perform()
            
            # driver.find_element(By.XPATH, LOGOFF_LINK_XPATH).click()
            logger.info('Logoff completed')
        except NoSuchElementException as e:
            logger.error("Element not found")
            raise e
        except TimeoutError as e:
            logger.error("Timeout error occurred")
            raise e