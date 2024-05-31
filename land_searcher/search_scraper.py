import time
from logging import config, getLogger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from const import MAINMENU_SEARCH_PROPERTIES_BUTTON_XPATH
from scraper import Scraper

logger = getLogger(__name__)

class Search(Scraper):
    def search_properties_for_sale(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, None)))
        self.driver.find_element(By.XPATH, None).click()
        time.sleep(20)