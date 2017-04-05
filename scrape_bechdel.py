from bs4 import BeautifulSoup
import requests
import re
import time
import json
from MovieDB import DB

db = DB()


class ScrapeBechdel(object):


    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_bechdel_data(self):
        bechdel_data = self.get_all_bechdel_films()
        for r in bechdel_data:
            db.insert_bechdel_info(r)
        db.commit()

    def get_all_bechdel_films(self):
        films = []
        for i in range(0, 1):
            films.extend(self.scrape_bechdel_page(i))
            time.sleep(3)
        return [self.get_bechdel_film_info(e) for e in films]

    def scrape_bechdel_page(self, page_no):
        html = requests.get('http://bechdeltest.com/?page=' + str(page_no), headers=self.headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        films = soup.find_all('div', {'class': 'movie'})
        return films

    def get_bechdel_film_info(self, film_html):
        title = film_html.find_all('a')[1].text
        imdb_url = film_html.find_all('a')[0].get('href').split('/')[4]
        bechdel = self.fix_bechdel(film_html.find_all('a')[0].find_all('img')[0].get('src'))
        return {'title': title, 'imdb_id': imdb_url, 'bechdel': bechdel}

    def fix_bechdel(self, img_string):
        if re.search(r'\/nopass\.png', img_string):
            return 'Fail'
        else:
            return 'Pass'

class ScrapeExtraInfo(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def run(self):
        self.movies = db.get_unappended_films()
        c = 0
        for m in self.movies:
            c += 1
            movie_info = self.get_movie_info(m)
            print (movie_info)
            if movie_info:
                db.insert_movie_info(movie_info)
                if divmod(c,2)[1]==0:
                    print ('commit - c')
                    db.commit()

    def get_movie_info(self, imdb_id):
        try:
            movie_dict = self.get_imdb_info(imdb_id)
            box_office_info = self.scrape_imdb_box_office(imdb_id)
            movie_dict['Budget'] = self.get_imdb_budget(box_office_info)
            movie_dict['Gross'] = self.get_imdb_gross(box_office_info)
            movie_dict['imdb_ID'] = movie_dict['imdbID']
            movie_dict['AwardScore'] = self.fix_award_score(movie_dict['Awards'])
            movie_dict = self.get_chosen_fields(movie_dict)
            movie_dict['Year'] = movie_dict['Year'][0:4]
            for m in movie_dict.keys():
                movie_dict[m] = self.fix_imbd_nulls(movie_dict[m] )
            return movie_dict
        except:
            return

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
           return None

    def get_imdb_budget(self, text):
        try:
           return self.fix_money(re.findall(r'(?<=Budget\n)\$[\d+,?]{1,100}', text)[0])
        except:
            return None

    def fix_money(self, text):
        return int(re.findall(r'(?<=\$)[\d+,?]{1,}',text)[0].replace(',', ''))

    def fix_imbd_nulls(self, imdb_info):
        if imdb_info == 'N/A':
            return None
        else:
            return imdb_info

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

    def get_chosen_fields(self, movie_info):

        columns = [ 'Budget', 'Poster', 'Year', 'Writer', 'Response', 'Released'
              , 'Type', 'AwardScore', 'imdb_ID', 'Runtime', 'Plot', 'Rated', 'Gross', 'imdbVotes'
              , 'imdbRating', 'Genre', 'Metascore', 'Language', 'Title', 'Awards'
              , 'Country', 'Director', 'Actors']

        new_movie_info = {}
        for m in columns:
            new_movie_info[m] = movie_info[m]
        return new_movie_info


if __name__=='__main__':
    #src = ScrapeBechdel()
    #src.get_bechdel_data()
    src = ScrapeExtraInfo()
    src.run()
    blah = src.get_movie_info('tt6527026')
    print(blah)



