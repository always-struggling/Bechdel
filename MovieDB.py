import psycopg2
import json

class DB(object):

    def __init__(self):
        self.conn = psycopg2.connect("dbname=Bechdel user=postgres password=oreflan@51")
        self.cur = self.conn.cursor()

    def insert_bechdel_info(self, row):
        self.cur.execute('''INSERT INTO Bechdel(imdb_id, title, bechdel)
                            VALUES (%(imdb_id)s, %(title)s, %(bechdel)s)
                                ON CONFLICT (imdb_id)
                                DO NOTHING;''', row)

    def insert_movie_info(self, row):
        self.cur.execute('''insert into movie_info (
                                  Budget, Poster, Year, Writer, Response, Released
                                , Type, AwardScore, imdb_ID, Runtime, Plot, Rated, Gross, imdbVotes
                                , imdbRating, Genre, Metascore, Language, Title, Awards
                                , Country, Director, Actors
                                )
                            values (
                                  %(Budget)s, %(Poster)s, %(Year)s, %(Writer)s, %(Response)s,  %(Released)s
                                , %(Type)s, %(AwardScore)s, %(imdb_ID)s, %(Runtime)s, %(Plot)s, %(Rated)s, %(Gross)s, %(imdbVotes)s
                                , %(imdbRating)s, %(Genre)s, %(Metascore)s, %(Language)s, %(Title)s, %(Awards)s
                                , %(Country)s, %(Director)s, %(Actors)s
                                ) ''', row)

    def get_unappended_films(self):
        self.cur.execute('''SELECT imdb_id
                              FROM bechdel
                             WHERE imdb_id NOT IN (SELECT imdb_id
                                                    FROM movie_info)''')
        result = [d[0] for d in self.cur.fetchall()]
        return result

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__=='__main__':
    db = DB()
    result = db.get_data()
    print (result)
