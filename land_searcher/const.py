import os

BASE_DIR = os.path.dirname(__file__)
LOGGING_CONF = os.path.join(BASE_DIR, 'config/logging.json')

LOGIN_ID_XPATH = '/html/body/div[1]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div[2]/input'
LOGIN_PASSWORD_XPATH = '/html/body/div[1]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div/div[2]/input'
LOGIN_GUIDELINE_CHECK_XPATH = '/html/body/div[1]/div/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/input'
LOGIN_BUTTON_XPATH = '/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/button'