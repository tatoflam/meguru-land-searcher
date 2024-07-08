import time
from logging import config, getLogger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from const import MAINMENU_SEARCH_PROPERTIES_BUTTON_XPATH
from scraper import Scraper

logger = getLogger(__name__)

class Menu(Scraper):    
    def go_search_properties_for_sale(self):
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, MAINMENU_SEARCH_PROPERTIES_BUTTON_XPATH)))
        self.driver.find_element(By.XPATH, MAINMENU_SEARCH_PROPERTIES_BUTTON_XPATH).click()
        logger.info('Main Menu 売買物件検索 clicked')