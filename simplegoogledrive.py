import os
import pprint

from googleauthorizedservice import GoogleAuthorizedService

class SimpleGoogleDrive( object ):
    api_parameters = { 
        'drive': {
            'api_name': 'drive', 
            'api_version': 'v3', 
            'scopes': [ 'https://www.googleapis.com/auth/drive' ],
        },
        'sheets': {
            'api_name': 'sheets', 
            'api_version': 'v4', 
            'scopes': [ 'https://www.googleapis.com/auth/spreadsheets' ],
        },
    }
        

    def __init__( self, *a, **k ):
        self.drive = GoogleAuthorizedService( **(self.api_parameters[ 'drive' ]) )
        self.sheets = GoogleAuthorizedService( **(self.api_parameters[ 'sheets' ]) )


    def get_sheet_by_name_prefix( self, parent, pfx ):
        fmt = ("name contains '{pfx}'"
               " and mimeType =  'application/vnd.google-apps.spreadsheet'"
               " and '{parent}' in parents"
               )
        query = fmt.format( pfx=pfx, parent=parent )
        results = self.drive.files().list( q=query ).execute()
        pprint.pprint( results, indent=2 )
