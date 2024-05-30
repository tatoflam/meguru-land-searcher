import os
from selenium.webdriver.support import expected_conditions as EC
from logging import config, getLogger

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from const import LOGIN_ID_XPATH, LOGIN_PASSWORD_XPATH, LOGIN_GUIDELINE_CHECK_XPATH, \
    LOGIN_BUTTON_XPATH


logger = getLogger(__name__)

def login(driver):
    try:
        login_url = os.environ["LOGIN_URL"]
        login_id = os.environ["ID"]
        login_password = os.environ["PASSWORD"]
         
        driver.get(login_url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, LOGIN_GUIDELINE_CHECK_XPATH)
        )
    )
        
        wait = WebDriverWait(driver, 10)
        if EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH)):
            logger.info('Login is clickable')

        # driver.find_element(By.XPATH, LOGIN_ID_XPATH).send_keys(login_id)

        if EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH)):
            logger.info('Login is clickable')
        driver.find_element(By.XPATH, '//*[@id="__BVID__13"]').send_keys(login_id)
        # driver.find_element(By.XPATH, LOGIN_PASSWORD_XPATH).send_keys(login_password)
        driver.find_element(By.XPATH, '//*[@id="__BVID__16"]').send_keys(login_password)
        # driver.find_element(By.XPATH, LOGIN_GUIDELINE_CHECK_XPATH).click()
        driver.find_element(By.XPATH, '//*[@id="__BVID__20"]').click()
        
        driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()
        logger.info('Login completed')
    except NoSuchElementException as e:
        logger.error("Element not found")
        raise e
    except TimeoutError as e:
        logger.error("Timeout error occurred")
        raise e
    except Exception as e:
        logger.error("Timeout error occurred")
        raise e

def logoff(driver):
    try: 
        if EC.element_to_be_clickable((By.XPATH, LOGOFF_XPATH)):
            logger.info('Logoff is clickable')

        driver.find_element(By.XPATH, LOGOFF_XPATH).click()
        logger.info('Logoff completed')
    except NoSuchElementException as e:
        logger.error("Element not found")
        raise e
    except TimeoutError as e:
        logger.error("Timeout error occurred")
        raise e