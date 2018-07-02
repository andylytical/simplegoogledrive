###
#  Use a Google Sheet as a Time Series Database
###

import dateutil.parser
import functools

class TimeSeriesDB(object):
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
        self.headers = None
        

    def has_header_row( self, val=None ):
        if self.headers is None:
            if val is None:
                val = self.get_dates( start=1, end=1 )
            try:
                d = dateutil.parser.parse( val )
                self.headers = False
            except (ValueError) as e:
                self.headers = True
        return self.headers


    def timestamps( self ):
        return self._get_dates()

    def _get_dates( self, start='', end='' ):
        range_ = "'{name}'!{col}{start}:{col}{end}".format(
            name=self.sheet_name,
            col=self.primary_column,
            start=start,
            end=end
            )
        params = {
            'spreadsheetId': self.file_id,
            'range': range_,
            'majorDimension': 'COLUMNS',
        }
        results = self.service.spreadsheets().values().get(**params).execute()
        values = results['values'][0]
        # check for, and remove, header row
        if self.has_header_row( values[0] ):
            values = values[1:]
        # create native python datetime from each string value
        dates = list( map( dateutil.parser.parse, values ) )
        return dates
        
