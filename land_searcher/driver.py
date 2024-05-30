import platform
import traceback
from logging import getLogger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
# from slackweb import Slack

logger = getLogger(__name__)

def get_webdriver():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless") 

    if platform.system() == "Linux" and \
        (platform.machine() == "armv6l" or \
        platform.machine() == "armv7l"):  
        # if raspi 32 bit
        options.BinaryLocation = ("/usr/bin/chromium-browser")
        service = Service("/usr/bin/chromedriver")
        logger.info('Using local chromedriver') 
    else:
        # if not raspi, using Chrome
        service = Service(ChromeDriverManager().install()) 
        logger.info('Using chromedriver installed by ChromeDriverManager')
    
    try: 
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("Got webdriver")
        return driver
    except WebDriverException as e:
        logger.error('WebDriverException occurred', e)
        stack_trace = traceback.format_exc()
        logger.error(stack_trace)
#        slack.notify(text = 'An error is raised on searching land :%s \n %s'
#                        % (status, stack_trace)
#        )
    except Exception as e:
        logger.error("An exception occurred:", e)
        stack_trace = traceback.format_exc()
        logger.error(stack_trace)
#        slack.notify(text = 'An error is raised on searching land :%s \n %s'
#                        % (status, stack_trace)
#        )    
    