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
    '//*[@id="__BVID__265"]':'売土地', # 物件種別1
}
# 所在地・沿線
SEARCH_ADDRESS_STATION_INFO = {
    '//*[@id="__BVID__318"]':'東京都', # 都道府県
    '//*[@id="__BVID__322"]':'２３区' # 所在地名1
}
# その他検索項目(在庫のみ)
SEARCH_DAYS_RADIO_BUTTONS = {
    '/html/body/div[1]/div/div/div[1]/div[1]/div/div[10]/div/div[3]/div[1]/div/div[2]/div/div/div/div[6]/input':'', # 登録年月日
    '/html/body/div[1]/div/div/div[1]/div[1]/div/div[10]/div/div[3]/div[2]/div/div[2]/div/div/div/div[6]/input':'', # 
}
# 検索条件の選択・保存 (ワンタッチ検索)
SEARCH_ONE_TOUCH_OPTIONS = {
    '/html/body/div[1]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/select':'01:　売土地２３区前日', # 保存した検索条件の選択
}
# 検索条件の選択・保存 (ワンタッチ検索) # 読み込みボタン
LOAD_ONE_TOUCH_OPTIONS = '//*[@id="__layout"]/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/button'

SEARCH_BUTTON_XPATH = '//*[@id="__layout"]/div/div[2]/div/div/div/div/div[4]/button'

RESULT_PAGING_BUTTON = '/html/body/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div[1]/ul/li[7]/button'

RESULT_PAGING_UL = '/html/body/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div[1]/ul'

RESULT_PAGING_DISABLED = '/html/body/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div[1]/ul/li[7]'