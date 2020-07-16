import requests
import math
from bs4 import BeautifulSoup

class race:

    BASE_URL = 'https://race.netkeiba.com/'

    def __init__(self, race_endpoints=[]):
        race_endpoints = race_endpoints

    def fetch(self, race_id):
        html = requests.get('https://race.netkeiba.com/race/result.html?race_id=' + race_id + '&rf=race_submenu')
        return BeautifulSoup(html.content, 'lxml')

    def race_result(self, race_id):
        soup = self.fetch(race_id)
        result_table_soup = soup.find("table", {"class": 'RaceTable01 RaceCommon_Table ResultRefund Table_Show_All'})
        col_num = 15
        rows = []
        row = []
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
                row = []
        return rows

    def payback(self, race_id):
        soup = self.fetch(race_id)
        pay_table_souplen = soup.findAll("table", {"class": 'Payout_Detail_Table'})
        paybacks = []
        for sub_pay_table in pay_table_souplen:
            for col in sub_pay_table.find("tbody").findAll(["tr", "td"]):
                if (col['class'] == ['Tansho']):
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Fukusho']):
                    paybacks.extend(col.find(class_='Payout').text.replace(',', '').strip().split('円')[:3])
                if (col['class'] == ['Wakuren']):
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Umaren']):
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Wide']):
                    paybacks.extend(col.find(class_='Payout').text.replace(',', '').strip().split('円')[:3])
                if (col['class'] == ['Umatan']):
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Fuku3']):
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
                if (col['class'] == ['Tan3']):
                    paybacks.append(col.find(class_='Payout').text.replace(',', '').strip('円'))
        return paybacks

    def raptime(self, race_id):
        soup = self.fetch(race_id)
        raptime_table_souplen = soup.find("table", {"class": 'RaceCommon_Table Race_HaronTime'})
        raptimes_list = ['100m', '200m', '300m', '400m', '500m', '600m', '700m', '800m', '900m',
                         '1000m', '1100m', '1200m', '1300m', '1400m', '1500m', '1600m', '1700m',
                         '1800m', '1900m', '2000m', '2100m', '2200m', '2300m', '2400m', '2500m', '2600m']
        kyoriS = list(map(lambda y: y.text, raptime_table_souplen.find(class_='Header').findAll('th')))
        timeS = list(map(lambda y: y.text, raptime_table_souplen.find(class_='HaronTime').findAll('td')))
        raptimes = [None] * len(raptimes_list)
        for kyori, time in zip(kyoriS, timeS):
            raptimes[raptimes_list.index(kyori)] = time
        return raptimes

if __name__ == '__main__':
    def __test():
        racer = race()
        race_id = '202009040202'
        print(racer.race_result(race_id) != None)
        print(racer.payback(race_id) != None)
        print(racer.raptime(race_id) != None)

    __test()