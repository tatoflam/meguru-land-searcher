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

# //*[@id="__layout"]/div/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/button
MAINMENU_SEARCH_PROPERTIES_BUTTON_XPATH = '//*[@id="__layout"]/div/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/button'

# 売買検索条件入力 基本条件
SEARCH_BASIC_CONDITIONS_SELECT_OPTIONS = {
    '//*[@id="__BVID__256"]':'売土地', # 物件種別1
    '//*[@id="__BVID__259"]':'売地', # 物件種目1
    '//*[@id="__BVID__262"]':'底地権', # 物件種目2
    '//*[@id="__BVID__265"]':'売一戸建', # 物件種別2
    '//*[@id="__BVID__268"]':'中古戸建' # 物件種目1
}
# 所在地・沿線
SEARCH_ADDRESS_STATION_INFO = {
    '//*[@id="__BVID__309"]':'東京都', # 都道府県
    '//*[@id="__BVID__313"]':'２３区' # 所在地名1
}

SEARCH_BUTTON_XPATH = '//*[@id="__layout"]/div/div[2]/div/div/div/div/div[4]/button'