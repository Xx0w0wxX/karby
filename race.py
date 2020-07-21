import requests
import math
from bs4 import BeautifulSoup

class race:

    BASE_URL = 'https://race.netkeiba.com/'

    def __init__(self, race_endpoints=[]):
        race_endpoints = race_endpoints
        self.result_columns = ['race_id', '着順', '枠', '馬番', '馬名', '性齢', '斤量', '騎手', 'タイム', '着差', '人気', '単勝オッズ', '後3F', 'コーナー通過順', '厩舎', '馬体重(増減)']
        self.payback_columns = ['race_id', '単勝', '複勝1', '複勝2', '複勝3', '枠連', '馬連', 'ワイド1', 'ワイド2', 'ワイド3', '馬単', '3連複', '3連単']
        self.elements = []
        self.raptimes_list = [
            'race_id',
            '100m', '200m', '300m', '400m', '500m', '600m', '700m', '800m', '900m',
            '1000m', '1100m', '1200m', '1300m', '1400m', '1500m', '1600m', '1700m',
            '1800m', '1900m', '2000m', '2100m', '2200m', '2300m', '2400m', '2500m', '2600m'
        ]

    def fetch(self, race_id):
        html = requests.get('https://race.netkeiba.com/race/result.html?race_id=' + race_id + '&rf=race_submenu')
        return BeautifulSoup(html.content, 'lxml')

    def race_result(self, race_id):
        soup = self.fetch(race_id)
        result_table_soup = soup.find("table", {"class": 'RaceTable01 RaceCommon_Table ResultRefund Table_Show_All'})
        col_num = 15
        rows = []
        row = [race_id]
        for col in result_table_soup.find("tbody").findAll(["tr", "td"]):
            if (list(set(['FirstDisplay', 'HorseList']) & set(col['class']))):
                continue
            row.append(col.text.strip())
            # TODO
            # ここで騎手と馬のクロールを流す
            # if (col['class'] == ['Jockey']):
            # print(col.find('a')['href'])
            # if (col['class'] == ['Horse_Info']) and (col.find('a') != None):
            # print(col.find('a')['href'])
            if (col['class'] == ['Weight']):
                rows.append(row)
                row = [race_id]
        return rows

    def payback(self, race_id):
        soup = self.fetch(race_id)
        pay_table_souplen = soup.findAll("table", {"class": 'Payout_Detail_Table'})
        paybacks = [race_id]
        for sub_pay_table in pay_table_souplen:
            for col in sub_pay_table.find("tbody").findAll(["tr"]):
                if (col['class'] == ['Tansho']):
                    self.elements.append('-'.join([el.text for el in col.findAll('div') if el.text != '']))
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Fukusho']):
                    self.elements.extend([el.text for el in col.findAll('div') if el.text != ''])
                    paybacks.extend(col.find(class_='Payout').text.replace(',', '').strip().split('円')[:3])
                if (col['class'] == ['Wakuren']):
                    self.elements.append('-'.join([el.text for el in col.findAll('span')][:2]))
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Umaren']):
                    self.elements.append('-'.join([el.text for el in col.findAll('span')][:2]))
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Wide']):
                    self.elements.extend(['-'.join([el.text for el in col.findAll('span')][:6][i::3]) for i in range(3)])
                    paybacks.extend(col.find(class_='Payout').text.replace(',', '').strip().split('円')[:3])
                if (col['class'] == ['Umatan']):
                    self.elements.append('-'.join([el.text for el in col.findAll('span')][:2]))
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Fuku3']):
                    self.elements.append('-'.join([el.text for el in col.findAll('span')][:3]))
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Tan3']):
                    self.elements.append('-'.join([el.text for el in col.findAll('span')][:3]))
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
        return paybacks

    def raptime(self, race_id):
        soup = self.fetch(race_id)
        raptime_table_souplen = soup.find("table", {"class": 'RaceCommon_Table Race_HaronTime'})
        kyoriS = list(map(lambda y: y.text, raptime_table_souplen.find(class_='Header').findAll('th')))
        timeS = list(map(lambda y: y.text, raptime_table_souplen.find(class_='HaronTime').findAll('td')))
        raptimes = [race_id]
        raptimes.extend([None] * (len(self.raptimes_list)-1))
        for kyori, time in zip(kyoriS, timeS):
            raptimes[self.raptimes_list.index(kyori)] = time
        return raptimes