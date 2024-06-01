import time
import random
class Scraper():
    '''A super class for scraping process. The constructor works whenever the sub class is initialized'''
    def __init__(self, driver):
        # set driver on initialize constructor
        self.driver = driver
        
        # sleep random integer value for pretending human operation
        time.sleep(random.randint(2, 7))
        