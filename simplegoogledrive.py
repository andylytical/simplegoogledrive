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


    def create_from_template( self, file_id, new_name ):
        parms = { 'fileId': file_id,
                  'body': { 'name': new_name },
                }
        request = self.drive.files().copy( **parms )
        response = request.execute()
        return response['id']


    def get_sheet_by_name_prefix( self, parent, pfx ):
        ''' Get list of sheets matching name prefix
        '''
        infolist = []
        fmt = ( "name contains '{pfx}'"
                " and mimeType =  'application/vnd.google-apps.spreadsheet'"
                " and '{parent}' in parents"
              )
        query = fmt.format( pfx=pfx, parent=parent )
        query_params = { 'q': query }
        return self._ls_files( query_params )
#        results = self.drive.files().list( q=query ).execute()
#        if len( results['files'] ) < 1 :
#            msg = "No files found matching name prefix '{}'".format( pfx )
#            raise UserWarning( msg )
#        elif len( results['files'] ) > 1 :
#            msg = "Multiple files found matching name prefix '{}'".format( pfx )
#            raise UserWarning( msg )
#        info = results['files'][0]
#        self._assert_is_sheet( info )
#        return info


    def _assert_is_sheet( self, file_info ):
        ''' Return True if file_info refers to a sheet; False otherwise
        '''
        rv = True
        sheet_meta = { 'kind': 'drive#file',
                       'mimeType': 'application/vnd.google-apps.spreadsheet',
                     }
        for k in sheet_meta.keys():
            if file_info[k] != sheet_meta[k] :
                rv = False
#                msg = "Not a sheet file; File Meta mismatch: '{}'='{}', expected '{}'".format(
#                    k, file_info[k], sheet_meta[k] )
#                raise UserWarning( msg )
        return rv
        

    def _ls_files( self, query_params ):
        ''' Wrapper around service.files().list() to handle pagination
            PARAMETERS:
                query_params - Valid paramters to pass to drive.files(),list()
            See also: https://developers.google.com/api-client-library/python/guide/pagination
        '''
        result_list = []
        files = self.drive.files()
        request = files.list( **query_params )
        while request is not None:
            response = request.execute()
#            result_list.extend( response.get('files', []) )
            for file in response.get('files', []):
                if self._assert_is_sheet( file ):
                    result_list.append( file )
#                print( 'Found file: %s (%s)' % (file.get('name'), file.get('id')) )
            request = files.list_next( request, response )
        return result_list
