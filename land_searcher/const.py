import os

BASE_DIR = os.path.dirname(__file__)
LOGGING_CONF = os.path.join(BASE_DIR, 'config/logging.json')

LOGIN_ID_XPATH = '//*[@id="__BVID__13"]'
LOGIN_PASSWORD_XPATH = '//*[@id="__BVID__16"]'
LOGIN_GUIDELINE_CHECK_XPATH = '//*[@id="__BVID__20"]'
LOGIN_BUTTON_XPATH = '//*[@id="__layout"]/div/div/div[3]/div/div[3]/div/button'

HAMBURGER_MENU_BUTTON_XPATH = '//*[@id="__layout"]/div/div/div[2]/div/div/div[3]/button'
LOGOFF_LINK_XPATH = '//*[@id="__layout"]/div/div/div[3]/div[2]/div[2]/div[10]/a'

HAMBURGER_MENU_BUTTON_IN_SEARCH_XPATH = '//*[@id="__layout"]/div/div[3]/div/div/div[3]/button'
LOGOFF_LINK_IN_SEARCH_XPATH = '/html/body/div[1]/div/div/div[4]/div[2]/div[2]/div[17]/a'


MAINMENU_SEARCH_PROPERTIES_BUTTON_XPATH = '//*[@id="__layout"]/div/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/button'