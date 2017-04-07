import unittest
import math
from Banding import Bands
from graph_data import Startup, Bar, Scatter, User
from MovieDB import DB
import pandas

class TestUser(unittest.TestCase):

    def test_startup(self):
        type = 'sql'
        sql =  '''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                    from bechdel a
                    join movie_info b
                      on a.imdb_id = b.imdb_id'''
        user = User(sql, type)


    def test_user_metadata(self):
        type = 'sql'
        sql =  '''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                    from bechdel a
                    join movie_info b
                      on a.imdb_id = b.imdb_id'''
        user = User(sql, type)
        user.get_metadata(user.df)

    def test_user_bar(self):
        type = 'sql'
        sql =  '''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                    from bechdel a
                    join movie_info b
                      on a.imdb_id = b.imdb_id'''
        user = User(sql, type)
        json = user.get_bar_json(user.df, 'imdbrating', 'Total', 'bechdel')


    def test_user_scatter(self):
        type = 'sql'
        sql = '''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                    from bechdel a
                    join movie_info b
                      on a.imdb_id = b.imdb_id'''
        user = User(sql, type)
        user.get_scatter_json(user.df, 'imdbrating', 'metascore', 'bechdel', 'title')


class TestStartup(unittest.TestCase):

    def test_load_data(self):
        start = Startup()
        type = 'file'
        location = 'data\\bechdel_data.json'
        df = start.load_data(location, type)
        self.assertGreater(df.shape[1], 0)
        type = 'sql'
        location = '''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                         from bechdel a
                         join movie_info b
                           on a.imdb_id = b.imdb_id'''
        df = start.load_data(location, type)
        self.assertGreater(df.shape[1], 0)

    def test_load_sql(self):
        start = Startup()
        sql = '''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                           from bechdel a
                           join movie_info b
                             on a.imdb_id = b.imdb_id'''
        df = start.load_from_database(sql)
        self.assertGreater(df.shape[1], 0)

    def test_load_file(self):
        start = Startup()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        self.assertGreater(df.shape[1], 0)

    def test_get_metadata(self):
        start = Startup()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        meta = start.get_metadata(df)
        self.assertEqual(meta['title'], 'Bechdel Analysis')
        self.assertEqual(meta['bar'], ["Rated", "AwardScore", "Year", "Bechdel", "Metascore", "Budget", "imdbRating", "Gross"])
        self.assertEqual(meta['scatter'],["AwardScore", "Year", "Bechdel", "Metascore", "Budget", "imdbRating", "Gross"])
        self.assertEqual(meta['z'], ["Rated", "Year", "Bechdel"])
        self.assertEqual(meta['index'], 'Title')

class TestBar(unittest.TestCase):

    def test_band_datarame(self):
        start = Startup()
        bar = Bar()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        df = bar.band_dataframe(df, 'imdbRating')
        self.assertGreater(df.shape[1], 0)

    def test_group_dataframe(self):
        start = Startup()
        bar = Bar()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        df = bar.band_dataframe(df, 'imdbRating')
        df = bar.group_dataframe( df, 'imdbRating', 'Bechdel')
        self.assertEqual(df.shape[1], 3)
        self.assertGreater(df.shape[0], 1)

    def test_aggregate_dataframe(self):
        start = Startup()
        bar = Bar()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        df = bar.band_dataframe(df, 'imdbRating')
        df = bar.group_dataframe( df, 'imdbRating', 'Bechdel')
        df = bar.aggregate_dataframe(df, 'imdbRating', 'Bechdel')
        self.assertEqual(df.shape[1], 3)
        self.assertLess(df.shape[0], 25)

    def test_get_bar_json(self):
        start = Startup()
        bar = Bar()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        json = bar.get_bar_json(df, 'imdbRating', 'Total', 'Bechdel')
        print(json)


class TestScatter(unittest.TestCase):

    def test_get_scatter_json(self):
        start = Startup()
        scatter = Scatter()
        filename = 'data\\bechdel_data.json'
        df = start.load_from_file(filename)
        json = scatter.get_scatter_json(df, 'imdbRating', 'Metascore', 'Bechdel', 'Title')
        print(json)



class TestBanding(unittest.TestCase):

    def test_get_base(self):
        band = Bands()
        self.assertEqual(band.get_base(1), 0)
        self.assertEqual(band.get_base(5), 0)
        self.assertEqual(band.get_base(10), 1)
        self.assertEqual(band.get_base(10.0), 1)
        self.assertEqual(band.get_base(1234.2203), 3)
        self.assertEqual(band.get_base(2.5), 0)

    def test_nicen_number(self):
        band = Bands()
        self.assertEqual(band.nicen_number(1.2), 1)
        self.assertEqual(band.nicen_number(23.559), 10)
        self.assertEqual(band.nicen_number(4355.9), 5000)
        self.assertEqual(band.nicen_number(790.9), 1000)
        self.assertEqual(band.nicen_number(0.9), 1)
        self.assertEqual(band.nicen_number(3), 1)

    def test_get_chunk_size(self):
        band = Bands()
        self.assertEqual(band.get_chunk_size(2.2,9.8), 1)
        self.assertEqual(band.get_chunk_size(20,400), 10)
        self.assertEqual(band.get_chunk_size(400,410), 1)
        self.assertEqual(band.get_chunk_size(400,142410), 10000)
        self.assertEqual(band.get_chunk_size(13456,14019), 50)

    def test_get_min_value(self):
        band = Bands()
        self.assertEqual(band.get_min_value(2.4, 1), 2)
        self.assertEqual(band.get_min_value(14153, 10), 14150)
        self.assertEqual(band.get_min_value(14153, 5), 14150)
        self.assertEqual(band.get_min_value(3553, 500), 3500)
        self.assertEqual(band.get_min_value(3134, 1), 3134)


    def test_get_band(self):
        band = Bands()
        self.assertEqual(band.get_bands(2, 9.8, 1), [2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(band.get_bands(700, 1253, 100), [700, 800, 900, 1000, 1100, 1200, 1300])
        self.assertEqual(band.get_bands(2, 6.2, 1), [2, 3, 4, 5, 6, 7])

    def test_get_labels(self):
        band = Bands()
        self.assertEqual(band.get_labels([100,200,300]),[150, 250])
        self.assertEqual(band.get_labels([2, 4, 6, 8]), [3, 5, 7])
        self.assertEqual(band.get_labels([1, 2, 3, 4]), [1.5, 2.5, 3.5])

    def test_get_bands(self):
        bands = Bands()
        print(bands.get_banding(2.2, 9.8))




class TestDB(unittest.TestCase):

    def test_insert_bechdel(self):
        db = DB()
        row = {'bechdel': 'Fail', 'title': '"The Big Bang Theory" The Comic-Con Conundrum', 'imdb_id': 'tt6527026'}
        db.insert_bechdel_info(row)
        db.commit()
        db.close()

    def test_insert_movie_info(self):
        db = DB()
        row = {'Type': 'episode', 'seriesID': 'tt0898266', 'Year': '2017', 'Episode': '17', 'Budget': None, 'imdb_ID': 'tt6527026', 'imdbRating': None, 'Director': 'Mark Cendrowski', 'Runtime': '22 min', 'Genre': 'Comedy, Romance', 'Released': '23 Feb 2017', 'Response': 'True', 'Awards': None, 'Country': 'USA', 'Metascore': None, 'imdbVotes': 'N/A', 'Writer': 'N/A', 'Rated': 'TV-14', 'Season': '10', 'AwardScore': 0, 'Title': 'The Comic-Con Conundrum', 'Gross': None, 'Language': 'English', 'Actors': 'Johnny Galecki, Jim Parsons, Kaley Cuoco, Simon Helberg', 'Poster': 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTUyNDMxNjQyN15BMl5BanBnXkFtZTgwNzA4NDQwMDI@._V1_SX300.jpg', 'Plot': "The guys' annual trip to Comic Con is in doubt when Raj can't afford to go."}
        db.insert_movie_info(row)
        db.commit()
        db.close()

if __name__ == '__main__':
    unittest.main()
