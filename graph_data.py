import pandas
from Banding import Bands
import json
import psycopg2

banding = Bands()


class Startup(object):

    def load_data(self, location, type):
        if type == 'sql':
            return self.load_from_database(location)
        elif type == 'file':
            return self.load_from_file(location)

    def load_from_database(self, sql):
        '''
        :param sql:
        :return:
        '''
        return pandas.read_sql_query(sql, psycopg2.connect("dbname=Bechdel user=postgres password=") )

    def load_from_file(self, file):
        '''
        Queriers either the bechdel database or a raw file
        :return: Dictionary of data
        '''
        return pandas.read_json(file)

    def get_metadata(self, df):
        '''

        :return:
        '''
        metadata={}
        metadata['title'] = 'Bechdel Analysis'
        field_info = self.set_field_info(df)
        metadata['bar'] = self.set_bar_fields(field_info)
        metadata['scatter'] = self.set_scatter_fields(field_info)
        metadata['z'] = self.set_z_fields(field_info)
        metadata['index'] = self.set_index_fields(df, field_info)[0]
        return json.dumps(metadata)


    def set_field_info(self, df):
        '''
        Analyses the fields of a dataframe and determines the datatype
        and number of unique values for each field
        :param df: The dataframe of the data we are analysing.
        :return: A dictionary - {field_name: [data type, unique values]}
        '''
        field_info ={}
        fields = list(df)
        for field in fields:
            field_info[field] = {'type':self.get_column_type(df, field), 'unq':self.get_distinct(df, field)}
        return field_info

    def get_column_type(self, df, field):
        '''
        This function determines the data type
        of a field.
        '''
        if df[field].dtype in ('float64', 'int64'):
            return 'number'
        elif df[field].dtype == 'object':
            try:
                df[field] = pandas.to_datetime(df[field])
                return 'date'
            except:
                return 'string'


    def get_distinct(self, df, field):
        '''
        This function determines the number of distinct
        values in a field
        :param df: The data frame of the data we loading
        :param field: The field in that data frame
        :return: An integer, detailing the number of distinct values in that field
        '''
        return df[field].nunique()


    def set_scatter_fields(self, field_info):
        scatter_buttons = []
        for field in field_info.keys():
            if field_info[field]['type'] == 'number':
                scatter_buttons.append(field)
        return scatter_buttons


    def set_bar_fields(self, field_info):
        bar_buttons = []
        for field in field_info.keys():
            if field_info[field]['type'] == 'number' or field_info[field]['unq'] <= 20:
                bar_buttons.append(field)
        return bar_buttons

    def set_z_fields(self, field_info):
        z_buttons = []
        for field in field_info.keys():
            if 1 < field_info[field]['unq'] < 11:
                z_buttons.append(field)
        return z_buttons

    def set_index_fields(self, df, field_info):
        index_fields = []
        for field in field_info.keys():
            if field_info[field]['type'] == 'string' and len(df) == field_info[field]['unq']:
                index_fields.append(field)
        return index_fields

class Bar(object):

    def get_bar_json(self, df, x, y, z):
        '''
        Returns bar graph data in json, by banding
        and aggregating dataframe column.
        :param df: The dataframe.
        :param x: The dataframe column we are analysing
        :param y: Either 'Percentage' or 'Total'
        :param z: Any additional additional fields we are grouping by
        :return: A json string containing the bar graph data
        '''
        df = self.remove_nulls_bar(df, x, z)
        df = self.band_dataframe(df, x)
        df = self.group_dataframe(df, x, z)
        df = self.aggregate_dataframe(df, x, z)
        return df.to_json(orient='records')

    def remove_nulls_bar(self, df, x, z):
        '''
        Removes rows with null values in columns x and z
        :param df: The dataframe.
        :param x: A dataframe column
        :param z: A dataframe column
        :return: The dataframe with nulls removed
        '''
        return df.dropna(axis=0, how='any', subset=[x, z])[[x, z]]


    def band_dataframe(self, df, x):
        '''
        Splits dataframe column into chunks
        so that it can be aggregated to create the
        bar graph.
        :param df: The dataframe.
        :param x: The column we are banding.
        :return: The dataframe with appended 'banded' column
        '''
        if df[x].nunique() > 25:
            mn = df[x].min()
            mx = df[x].max()
            bands, labels = banding.get_banding(mn, mx)
            df['Banding'] = pandas.cut(df[x], bins=bands, labels=labels)
            return df
        else:
            df['banding'] = df[x]
            return df

    def group_dataframe(self, df, x, z ):
        return df.groupby([z, 'Banding'])[x].count().reset_index()

    def aggregate_dataframe(self, df, x, z):
        return df.pivot(index='Banding', columns=z, values=x).reset_index()

class Scatter(object):

    def get_scatter_json(self, df, x, y, z, i):
        '''
        Returns scatter graph data in json, by removing
        any null values and selecting the correct columns.
        This exists predominantly to reduce the amount of data
        sent.
        :param df: The dataframe
        :param x: A dataframe column
        :param y: A dataframe column
        :param z: A dataframe column
        :param i: A dataframe column - index
        :return: The reduced dataframe
        '''
        #df = self.remove_nulls_scatter(df, x, z, y)
        fields = [x, y, z, i]
        print (fields)
        df = df[fields]
        return df.to_json(orient='records')

    def remove_nulls_scatter(self, df, x, y, z):
        '''
        Removes rows with null values in columns x, y and z.
        :param df: The dataframe
        :param x: A dataframe column
        :param y: A dataframe column
        :param z: A dataframe column
        :return: The dataframe with nulls removed
        '''
        return df.dropna(axis=0, how='any', subset=[x, y, z])[[x, y, z]]

class User(Startup, Bar, Scatter):

    def __init__(self, data, type):
        self.df = self.load_data(data, type)



    '''
    def get_bar_json(self, x, z, y):

        bands = Bands()
        tmp =

        unq = tmp_df[z].unique()
        type = self.get_column_type(x)

        if type == 'number' and nunq > 25:
            banding, labels = bands.get_banding(mn, mx)
            print (banding)
            print(labels)
            print (tmp_df[x].min())
            tmp_df['Banding'] = pandas.cut(tmp_df[x], bins=banding, labels=False)
            #tmp_df = tmp_df.replace({"Banding": labels})
        else:
            tmp_df['Banding'] = tmp_df[x]
        tmp_df = tmp_df.groupby([z, 'Banding'])[x].count().reset_index()
        # The y-axis determines whether we return the total or the percentage total.
        if y == 'P':
            total = tmp_df.groupby([z]).sum().reset_index()
            tmp_df = tmp_df.merge(total, left_on=z, right_on=z, how='inner')
            tmp_df[x] = ( tmp_df[x +'_x']  / tmp_df[x +'_y'] ) * 100
            tmp_df = tmp_df[[x,z, 'Banding']]
        tmp_df = tmp_df.pivot(index='Banding', columns=z, values=x).reset_index()
        # Replace nulls with 0
        #tmp_df[unq] = tmp_df[unq].astype(int)
        json = tmp_df.to_json(orient='records')
        return json




    def get_button_json(self):
        button_info = {}
        button_info['cols'] = self.number_fields
        #button_info['scatter'] = {}
        #for i in self.splitter_fields:
        #    button_info['scatter'][i]   = list(self.df[i].unique())
        return json.dumps(button_info)
    '''

if __name__=='__main__':
        sql = ''''select Year, AwardScore, Bechdel, Gross, Budget, Metascore, Rated, a.Title, Released, imdbRating
                           from bechdel a
                           join movie_info b
                             on a.imdb_id = b.imdb_id'''
        type = 'sql'
        data = User(sql, type)
        print(data.df)







