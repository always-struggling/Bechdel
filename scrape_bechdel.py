from bs4 import BeautifulSoup
import requests
import re
import time
import json


class Scrape(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_raw_data(self):
        bechdel_data = self.get_all_bechdel_films()
        self.save_data('raw_bechdel_data', bechdel_data)

    def expand_data(self, bechdel_data):
        l_count = 0
        new_data = []
        for film in bechdel_data:
            try:
                imdb_json = src.get_imdb_info(film['imdb_id'])
            except:
                continue
            imdb_json['Bechdel'] = film['bechdel']
            box_office_info = self.scrape_imdb_box_office(film['imdb_id'])
            imdb_json['Budget'] = self.get_imdb_budget(box_office_info)
            if imdb_json['Budget'] == '':
                pass
                print('no budget')
                continue
            imdb_json['Gross'] = self.get_imdb_gross(box_office_info)
            if imdb_json['Gross'] == '':
                print('no gross')
                continue
            try:
                imdb_json['AwardScore'] = self.fix_award_score(imdb_json['Awards'])
            except:
                imdb_json['AwardScore'] = 0
                new_data.append(imdb_json)
            l_count += 1
            print (l_count)
        data = self.select_fields(new_data)
        self.save_data('bechdel_data2', data)

    def save_data(self, filename, data):
        with open(filename+'.json', 'w') as data_file:
            data_file.write(json.dumps(data))

    def get_all_bechdel_films(self):
        films = []
        for i in range(0, 35):
            films.extend(self.scrape_bechdel_page(i))
            time.sleep(3)
        return [self.get_bechdel_film_info(e) for e in films]

    def scrape_bechdel_page(self, page_no):
        html = requests.get('http://bechdeltest.com/?page=' + str(page_no), headers=self.headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        films = soup.find_all('div', {'class':'movie'})
        return films

    def get_bechdel_film_info(self, film_html):
        title = film_html.find_all('a')[1].text
        imdb_url = film_html.find_all('a')[0].get('href').split('/')[4]
        bechdel = self.fix_bechdel(film_html.find_all('a')[0].find_all('img')[0].get('src'))
        return {'title':title, 'imdb_id':imdb_url, 'bechdel':bechdel}

    def get_imdb_info(self, imdb_id):
        html = requests.get('http://www.omdbapi.com/?i='+ imdb_id
                            #+'&y=&plot=short&r=json'
         , headers=self.headers)
        return json.loads(html.text)

    def scrape_imdb_box_office(self, imdb_id):
        html = requests.get('http://www.imdb.com/title/' + imdb_id + '/business?ref_=tt_dt_bus', headers=self.headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        try:
            return soup.find_all('div', {'id': 'tn15content'})[0].text
        except:
            return ''

    def get_imdb_gross(self, text):
        try:
           all_gross = re.findall(r'\nGross\n.*', text)[0]
           return self.fix_money(re.findall(r'\$[\d+,?]{1,100}(?= \(Worldwide\))', all_gross)[0])
        except:
           return ''

    def get_imdb_budget(self, text):
        try:
           return self.fix_money(re.findall(r'(?<=Budget\n)\$[\d+,?]{1,100}', text)[0])
        except:
            return ''

    def fix_money(self, text):
        return int(re.findall(r'(?<=\$)[\d+,?]{1,}',text)[0].replace(',', ''))

    def fix_award_score(self, text):
        try:
            wins = re.findall(r'\d{1,2} wins?', text)[0]
            wins = int(re.findall(r'\d{1,2}', wins)[0])
        except:
            wins = 0
        try:
            nominations = re.findall(r'\d{1,2} nominations?', text)[0]
            nominations = int(re.findall(r'\d{1,2}', nominations)[0])
        except:
            nominations = 0
        return max((3 * wins) + nominations,0)

    def fix_bechdel(self, img_string):
        if re.search(r'\/nopass\.png', img_string):
            return 0
        else:
            return 1

    def select_fields(self,json_data,*fields):
        new_json = []
        for e in json_data:
            record = {}
            record['Bechdel'] = e['Bechdel']
            record['Title'] = e['Title']
            record['Gross'] = e['Gross']
            record['Budget'] = e['Budget']
            record['Metascore'] = int(e['Metascore'])
            record['imdbRating'] = float(e['imdbRating'])
            record['Awards'] = e['Awards']
            record['AwardScore'] = e['AwardScore']
            record['Year'] = int(e['Year'])
            record['Released'] = e['Released']
            record['Rated'] = e['Rated']
            new_json.append(record)
        return new_json

if __name__=='__main__':

    src = Scrape()

    with open('data\\raw_bechdel_data.json') as raw_data:
        raw_data = json.load(raw_data)
        src.expand_data(raw_data)



