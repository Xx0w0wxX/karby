from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import math
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import hydra
from omegaconf import DictConfig


@hydra.main(config_path="config.yaml")
def endpoints_collector(cfg : DictConfig) -> None:

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)
    driver.get('https://db.netkeiba.com/?pid=race_search_detail')

    ## 競走種別
    if cfg.track.dart:
        driver.find_element_by_id('check_track_1').click() # 芝
    if cfg.track.shiba:
        driver.find_element_by_id('check_track_2').click() # ダート
    if cfg.track.syogai:
        driver.find_element_by_id('check_track_3').click() # 障害

    ## 競馬場
    if cfg.jyo.sapporo:
        driver.find_element_by_id('check_Jyo_01').click() # 札幌
    if cfg.jyo.hakodate:
        driver.find_element_by_id('check_Jyo_02').click() # 函館
    if cfg.jyo.hukushima:
        driver.find_element_by_id('check_Jyo_03').click() # 福島
    if cfg.jyo.niigata:
        driver.find_element_by_id('check_Jyo_04').click() # 新潟
    if cfg.jyo.tokyo:
        driver.find_element_by_id('check_Jyo_05').click() # 東京
    if cfg.jyo.nakayama:
        driver.find_element_by_id('check_Jyo_06').click() # 中山
    if cfg.jyo.tyukyo:
        driver.find_element_by_id('check_Jyo_07').click() # 中京
    if cfg.jyo.kyoto:
        driver.find_element_by_id('check_Jyo_08').click() # 京都
    if cfg.jyo.hanshin:
        driver.find_element_by_id('check_Jyo_09').click() # 阪神
    if cfg.jyo.ogura:
        driver.find_element_by_id('check_Jyo_10').click() # 小倉

    ## 馬場状態
    if cfg.baba.ryou:
        driver.find_element_by_id('check_baba_1').click() # 良
    if cfg.baba.yayaomo:
        driver.find_element_by_id('check_baba_2').click() # 稍重
    if cfg.baba.omo:
        driver.find_element_by_id('check_baba_3').click() # 重
    if cfg.baba.huryou:
        driver.find_element_by_id('check_baba_4').click() # 不良

    ## 条件
    if cfg.jouken.onlyhinba:
        driver.find_element_by_id('check_jyoken_1').click() # 牝馬限定
    if cfg.jouken.onlychichinaikokusan:
        driver.find_element_by_id('check_jyoken_2').click() # 父内国産限定
    if cfg.jouken.arabu:
        driver.find_element_by_id('check_jyoken_3').click() # アラブ
    if cfg.jouken.select:
        driver.find_element_by_id('check_jyoken_4').click() # 指定
    if cfg.jouken.mix:
        driver.find_element_by_id('check_jyoken_5').click() # 混合
    if cfg.jouken.tokushi:
        driver.find_element_by_id('check_jyoken_6').click() # 特指
    if cfg.jouken.international:
        driver.find_element_by_id('check_jyoken_7').click() # 国際

    ## 馬齢
    if cfg.barei.ni:
        driver.find_element_by_id('check_barei_11').click() # ２歳
    if cfg.barei.san:
        driver.find_element_by_id('check_barei_12').click() # ３歳
    if cfg.barei.morethansan:
        driver.find_element_by_id('check_barei_13').click() # ３歳以上
    if cfg.barei.morethanyon:
        driver.find_element_by_id('check_barei_14').click() # ４歳以上

    ## 表示件数
    links_num = driver.find_element_by_name('list')
    nums_element = Select(links_num)
    nums_element.select_by_value("100")

    driver.find_element_by_class_name('button').send_keys(Keys.ENTER)


    ####################################################################

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    num_pattern = '\d+'
    total_race_link = re.search(num_pattern, soup.find(id="contents_liquid").find(class_='pager').text.strip().replace(',', '')).group()
    total_search_page = math.ceil(int(total_race_link)/100)

    print('Total Race Endpoints: {}'.format(total_race_link))

    all_race_links = []

    filename = 'out.txt'

    with open(filename, mode='a') as f:
        for i in range(1, total_search_page):
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            pattern = '/race/\d+/'
            for a in soup.find_all('a', href=True):
                if re.search(pattern, a['href']):
                    f.write(a['href'].split('/')[2] + '\n')
                    print('Collect: {}'.format(a['href'].split('/')[2]))
                    all_race_links.append(a['href'].split('/')[2])
            driver.execute_script("paging('{}')".format(i+1))

    return all_race_links
