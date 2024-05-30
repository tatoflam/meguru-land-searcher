
import argparse
import os
import json
from logging import config, getLogger
from dotenv import load_dotenv

from const import LOGGING_CONF
from auth import login, logoff
from driver import get_webdriver

config_dict = None
with open(LOGGING_CONF, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

def run():
    # Parse parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_date', type=int, default=3,
                        help='specify number of date as a parameter. Default is 3 (days)')
    args = parser.parse_args()
    print(args.num_date)
    
    load_dotenv()
    driver = get_webdriver()
    login(driver)

if __name__ == "__main__":
    run()