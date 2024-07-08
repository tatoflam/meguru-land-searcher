import time
import random
from logging import config, getLogger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from const import RESULT_PAGING_UL, P_TABLE_HEADER, P_TABLE_HEADER_ITEM, P_TABLE_BODY, P_TABLE_BODY_ROW, P_TABLE_BODY_ITEM
from scraper import Scraper

logger = getLogger(__name__)

class SearchResult(Scraper):
    
    def get_paging_button(self):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, RESULT_PAGING_UL)))
        parent_element = self.driver.find_element(By.XPATH, RESULT_PAGING_UL)
        li_elements = parent_element.find_elements(By.TAG_NAME, 'li')
        # Get last element
        last_li_element = li_elements[-1]
        paging_button = last_li_element.find_element(By.TAG_NAME, 'button')
        return last_li_element, paging_button
    
    
    def result_paging(self):
        last_li_element, paging_button = self.get_paging_button()
        
        wait = WebDriverWait(self.driver, 15)
        page = 1
        data = []

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, P_TABLE_HEADER)))
        table_header = self.driver.find_element(By.CLASS_NAME, P_TABLE_HEADER)
        
        # Find row in the table header
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, P_TABLE_HEADER_ITEM)))
        header_items = table_header.find_elements(By.CLASS_NAME, P_TABLE_HEADER_ITEM)
        header_row = [cell.text for cell in header_items]
        
        # Get blank indices for header and rows processing
        blank_indices = [index for index, value in enumerate(header_row) if value == '']
        header_values = [value for index, value in enumerate(header_row) if index not in blank_indices]

        logger.info(header_values)
        data.append(header_values)

        while True:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, P_TABLE_BODY)))
            table_body = self.driver.find_element(By.CLASS_NAME, P_TABLE_BODY)

            # Find all rows in the table body
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, P_TABLE_BODY_ROW)))            
            rows = table_body.find_elements(By.CLASS_NAME, P_TABLE_BODY_ROW)
            logger.info(f"result paging: {page} has {len(rows)} entries")

            # Scrape data
            for row in rows:
                cells = row.find_elements(By.CLASS_NAME, P_TABLE_BODY_ITEM)
                row_data = [cell.text for index, cell in enumerate(cells) if index not in blank_indices]
                logger.debug(row_data)
                data.append(row_data)
                
            time.sleep(2)
                        
            try: 
                class_value = paging_button.get_attribute('class')
                logger.debug(logger.info(class_value))
                if 'disabled' not in  class_value:
                    paging_button.click()
                    logger.info("clicked paging button")
                    # In the loop, the same element is stored in the previous process. Therefore it's necessary to wait without any conditions. 
                    time.sleep(10)

                else: 
                    logger.info("The end of the paging link. Ending the scraping process")
                    break
                page +=1
                # per page 50 x 10 (500 entries is upper limit)
                if page >= 10:
                    break
            except StaleElementReferenceException as e:
                if 'disabled' in last_li_element.get_attribute('class'):
                    logger.info("The end of the paging link. Ending the scraping process")
                    break
            except TimeoutException as e:
                try: 
                    if 'disabled' in last_li_element.get_attribute('class'):
                        logger.info("The end of the paging link. Ending the scraping process")
                        break
                except Exception as e:
                    raise e                    
            except Exception as e:
                logger.error(f"Exception: {e}")
                raise e
        
        logger.info(f"The result paging ended on the page {page}")
        return data
