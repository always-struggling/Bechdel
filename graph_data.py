import pandas
from Banding import Bands
from MovieDB import DB

bands = Bands()
db = DB()

import json

class Analyse(object):

    def __init__(self, file):
        self.file = file
        self.df = self.load_dataframe()
        print (self.df)
        #self.df = pandas.read_json(file)
        self.field_info = self.set_field_info()
        self.number_fields = self.set_number_fields(self.field_info)
        self.splitter_fields = self.set_splitter_fields(self.field_info)
        self.index_field = self.set_index_fields(self.field_info)[0]

    def load_dataframe(self):
        '''
        Queriers either the bechdel database or a raw file
        :return: Dictionary of data
        '''
        if self.file:
            print('getting json')
            return pandas.read_json(self.file)
        else:
            print ('getting db')
            data =  db.get_data()
            return pandas.DataFrame(data)




    def set_field_info(self):
        '''
        Analyses the fields of a dataframe and determines the datatype
        and number of unique values for each field
        :param df: The dataframe of the data we are analysing.
        :return: A dictionary - {field_name: [data type, unique values]}
        '''
        field_info ={}
        fields = list(self.df)
        for field in fields:
            field_info[field] = {'type':self.get_column_type(field), 'unq':self.get_distinct(field)}
        return field_info

    def set_number_fields(self, field_info):
        number_fields = []
        for field in field_info.keys():
            if field_info[field]['type'] == 'number':
                number_fields.append(field)
        return number_fields

    def set_splitter_fields(self, field_info):
        splitter_fields = []
        for field in field_info.keys():
            if 1 < field_info[field]['unq'] < 11:
                splitter_fields.append(field)
        return splitter_fields

    def set_index_fields(self, field_info):
        index_fields = []
        for field in field_info.keys():
            if field_info[field]['type'] == 'string' and len(self.df) == field_info[field]['unq']:
                index_fields.append(field)
        return index_fields

    def get_column_type(self, field):
        '''
        This function determines the data type
        of a field.
        '''
        if self.df[field].dtype in ('float64', 'int64'):
            type = 'number'
        elif self.df[field].dtype == 'object':
            try:
                self.df[field] = pandas.to_datetime(self.df[field])
                type = 'date'
            except ValueError:
                type = 'string'
        return type

    def get_distinct(self, field):
        '''
        This function determines the number of distinct
        values in a field
        :param df: The data frame of the data we loading
        :param field: The field in that data frame
        :return: An integer, detailing the number of distinct values in that field
        '''
        return self.df[field].nunique()

    def get_bar_json(self, x, z, y):
        '''
        This creates the json needed to construct a grouped bar graph
        :param df: The dataframe of the complete data
        :param field: The field we want to create a grouped bar graph from
        :param spread: The spread column
        :return: A json string containing the data we need to split it by
        '''
        tmp_df = self.df[[x, z]]
        nunq = self.get_distinct(x)
        unq = tmp_df[z].unique()
        type = self.get_column_type(x)
        mn = tmp_df[x].min()
        mx = tmp_df[x].max()
        if type == 'number' and nunq > 25:
            banding, labels = bands.get_banding(mn, mx)
            tmp_df['Banding'] = pandas.cut(tmp_df[x], bins=banding, labels=False)
            tmp_df = tmp_df.replace({"Banding": labels})
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
        tmp_df = tmp_df.fillna(0)
        tmp_df[unq] = tmp_df[unq].astype(int)

        json = tmp_df.to_json(orient='records')
        return json

    def get_scatter_json(self, x, y, r, z):
        fields = [self.index_field, x, y, r, z]
        fields = list(set(fields))
        return self.df[fields].to_json(orient='records')

    def get_button_json(self):
        button_info = {}
        button_info['cols'] = self.number_fields
        #button_info['scatter'] = {}
        #for i in self.splitter_fields:
        #    button_info['scatter'][i]   = list(self.df[i].unique())
        return json.dumps(button_info)




if __name__=='__main__':
    #data = Analyse('data\\bechdel_data.json')
    data = Analyse('')
    #blah = data.get_bar_json('imdbRating','Bechdel', 'T')
    print('hello')
    blah = data.get_scatter_json('Gross', 'imdbRating','imdbRating', 'Metascore')
    print(blah)






