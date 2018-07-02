#!/bin/bash

export GOOGLE_CLIENT_SECRETS_FILE='client_secrets.json'
export GOOGLE_CREDENTIALS_FILE='credentials.json'
export SHEETS_PARENT_ID='1d57i-VAQRbCfLDIb9JCHGI3GPBK8cZ4O'
export SHEETS_NAME_PREFIX='20180701'
export TSDB_SHEET_NAME='RIMS Data'
#export TSDB_PRIMARY_COLUMN='A' # default is A, so don't have to set this

python test.py
