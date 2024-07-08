
import argparse
import os
import json
from logging import config, getLogger
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException

from const import LOGGING_CONF, SS_FOLDER_ID, GOOGLE_CREDENTIAL_JSON
from driver import Driver
from auth_scraper import Auth
from menu_scraper import Menu
from search_scraper import Search
from result_scraper import SearchResult

from spread_sheet import Spreadsheet

config_dict = None
with open(LOGGING_CONF, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

def run():
    logger.info("land search batch started.")
    # Parse parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_date', type=int, default=3,
                        help='specify number of date as a parameter. Default is 3 (days)')
    args = parser.parse_args()
    print(args.num_date)
    
    try:    
        load_dotenv()

        d = Driver()
        d.setWebDriver()
        driver = d.getWebDriver()
        
        Auth(driver).login()
        Menu(driver).go_search_properties_for_sale()
        Search(driver).search_properties_for_sale_from_menu()
        data = SearchResult(driver).result_paging()
        
        spreadsheet = Spreadsheet(GOOGLE_CREDENTIAL_JSON, data, SS_FOLDER_ID)
        spreadsheet.update()
        
    except NoSuchElementException as e:
        logger.error("Element not found", exc_info=True)
    except TimeoutError as e:
        logger.error("Timeout error occurred", exc_info=True)
    except Exception as e:
        logger.error("An exception occurred", exc_info=True)
    finally:
        try: 
            pass
            # TODO: logoff implementation
            # logoff(driver)
            # logger.info("Logoff completed.")        
        except Exception as e:
            logger.error("land searcher batch failed.", exc_info=True)
        finally:
            logger.info("land search batch finished.")
        
if __name__ == "__main__":
    run()