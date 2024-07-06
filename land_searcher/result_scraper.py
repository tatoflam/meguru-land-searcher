import time
import random
from logging import config, getLogger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

from const import RESULT_PAGING_BUTTON, RESULT_PAGING_DISABLED, RESULT_PAGING_UL
from scraper import Scraper

logger = getLogger(__name__)

class SearchResult(Scraper):
    
    def result_paging(self):
        wait = WebDriverWait(self.driver, 5)
        page = 1
        while True:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'p-table-body')))
            table_body = self.driver.find_element(By.CLASS_NAME, 'p-table-body')

            # Find all rows in the table body
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'p-table-body-row')))
            rows = table_body.find_elements(By.CLASS_NAME, 'p-table-body-row')
            logger.info(f"result paging: {page} has {len(rows)} entries")

            # Scrape data
            data = []
            for row in rows:
                cells = row.find_elements(By.CLASS_NAME, 'p-table-body-item')
                row_data = [cell.text for cell in cells]
                logger.info(row_data)
                data.append(row_data)
                
            # TODO need sleep, or wait for the class attribute in the next page. 
            time.sleep(2)
                        
            try: 
#                wait.until(EC.presence_of_element_located((By.XPATH, RESULT_PAGING_BUTTON)))
#                paging_button = self.driver.find_element(By.XPATH, RESULT_PAGING_BUTTON)

                wait.until(EC.presence_of_element_located((By.XPATH, RESULT_PAGING_UL)))
                parent_element = self.driver.find_element(By.XPATH, RESULT_PAGING_BUTTON)
                li_elements = parent_element.find_elements(By.TAG_NAME, 'li')
                # Get last element
                last_li_element = li_elements[-1]
                paging_button = last_li_element.find_element(By.TAG_NAME, 'button')

                class_value = paging_button.get_attribute('class')
                if 'disabled' not in  class_value:
                    paging_button.click() 
                else: 
                    break
                page +=1
                if page >= 10:
                    break
            except TimeoutException as e:
                try: 
                    paging_disabled = self.driver.find_element(By.XPATH, RESULT_PAGING_DISABLED)
                    if 'disabled' in paging_disabled.get_attribute('class'):
                        break
                except Exception as e:
                    raise e                    

            except Exception as e:
                print(f"Exception: {e}")
                raise e
        
        logger.info(f"The result paging ended on the page {page}")
