import datetime
import dateutil.parser
import functools

class TimeSeriesDB(object):
    ''' Treat a Google Sheet as a (simple) Time Series Database
    '''
    primary_column = 'A'

    def __init__( self,
                  sheets_service,
                  file_id,
                  sheet_name,
                  primary_column=None ):
        self.service = sheets_service
        self.file_id = file_id
        self.sheet_name = sheet_name
        if primary_column:
            self.primary_column = primary_column


    def timestamps( self ):
        range_ = "'{name}'!{col}:{col}".format(
            name=self.sheet_name,
            col=self.primary_column
            )
        elems = self._get_values( query=range_, majorDimension='COLUMNS' )
        # convert to python datetimes, ignore first (header) row
        return list( map( dateutil.parser.parse, elems[1:] ) )


    def headers( self ):
        range_ = "'{name}'!1:1".format( name=self.sheet_name )
        return self._get_values( query=range_, majorDimension='ROWS' )


    def _get_values( self, query, majorDimension ):
        params = {
            'spreadsheetId': self.file_id,
            'range': query,
            'majorDimension': majorDimension,
        }
        results = self.service.spreadsheets().values().get(**params).execute()
        return results['values'][0]


    def append( self, rows ):
        ''' rows is a list of lists
            each elem of rows is a list of data values to insert, one per cell
            data will be interpolated (date strings converted to google dates, etc.)
            return number of rows inserted
        '''
        clean_rows = self.py2js( rows )
        params = {
            'spreadsheetId': self.file_id,
            'body': { 'values': clean_rows },
            'range': "'{}'!A2".format( self.sheet_name ),
            'valueInputOption': 'USER_ENTERED',
        }
        result = self.service.spreadsheets().values().append( **params ).execute()
        return result['updates']['updatedRows']


    @staticmethod
    def py2js( val ):
        ''' Convert Python type to javascript type
        '''
        if isinstance( val, dict ):
            return { k: TimeSeriesDB.py2js( v ) for k,v in val.items() }
        elif isinstance( val, list ):
            return [ TimeSeriesDB.py2js( v ) for v in val ]
        elif isinstance( val, datetime.datetime ):
            return str( val )
        else:
            return val
