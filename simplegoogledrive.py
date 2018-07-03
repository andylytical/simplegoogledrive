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
        if len( results['files'] ) < 1 :
            msg = "No files found matching name prefix '{}'".format( pfx )
            raise UserWarning( msg )
        elif len( results['files'] ) > 1 :
            msg = "Multiple files found matching name prefix '{}'".format( pfx )
            raise UserWarning( msg )
        info = results['files'][0]
        self._assert_is_sheet( info )
        return info


    def _assert_is_sheet( self, file_info ):
        sheet_meta = { 'kind': 'drive#file',
                       'mimeType': 'application/vnd.google-apps.spreadsheet',
                     }
        for k in sheet_meta.keys():
            if file_info[k] != sheet_meta[k] :
                msg = "Not a sheet file; File Meta mismatch: '{}'='{}', expected '{}'".format(
                    k, file_info[k], sheet_meta[k] )
                raise UserWarning( msg )
        
