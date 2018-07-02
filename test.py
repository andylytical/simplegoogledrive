from simplegoogledrive import SimpleGoogleDrive
from timeseriesdb import TimeSeriesDB
import os
import pprint

sheets_parms = {
    'parent': os.environ['SHEETS_PARENT_ID'],
    'pfx': os.environ['SHEETS_NAME_PREFIX'],
}

g = SimpleGoogleDrive()

# Find spreadsheet
file_info = g.get_sheet_by_name_prefix( **sheets_parms )

# Get existing timestamps
tsdb_parms = {
    'sheets_service': g.sheets,
    'file_id': file_info['id'],
    'sheet_name': os.environ['TSDB_SHEET_NAME']
}
tsdb = TimeSeriesDB( **tsdb_parms )
results = tsdb.timestamps()
pprint.pprint( results )
