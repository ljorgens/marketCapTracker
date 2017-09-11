from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, abort
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import os
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

app = Flask(__name__)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
	    Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
	    os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
	                               'sheets.googleapis.com-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
	    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
	    flow.user_agent = APPLICATION_NAME
	    if flags:
	        credentials = tools.run_flow(flow, store, flags)
	    else: # Needed only for compatibility with Python 2.6
	        credentials = tools.run(flow, store)
	    print('Storing credentials to ' + credential_path)
	return credentials
    
def writeToGoogleDoc(data):
	"""Shows basic usage of the Sheets API.

	Creates a Sheets API service object and prints the names and majors of
	students in a sample spreadsheet:
	https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
	                'version=v4')
	service = discovery.build('sheets', 'v4', http=http,
	                          discoveryServiceUrl=discoveryUrl)

	spreadsheetId = '181_H2IeqQzYfuBu-_WitdN2ftQtFoJC1ydwRpqG3XOw'
	rangeName = 'A2:D16'
	value_input_option = 'USER_ENTERED'
	values = data
	body = {
	  'values': values
	}
	result = service.spreadsheets().values().update(
	    spreadsheetId=spreadsheetId, range=rangeName,
	    valueInputOption=value_input_option, body=body).execute()

@app.route("/")
def hello():
	coins = []
	coinMarketCapApi = urlopen('https://api.coinmarketcap.com/v1/ticker/')
	if coinMarketCapApi.getcode() == 200:
		data = json.load(coinMarketCapApi)
		coins = data
	else:
		return "FAILED " + coinMarketCapApi.getcode()
	
	return render_template('hello.html',**locals())
	
@app.route("/update")
def update_google_doc():
	coins = []
	coinMarketCapApi = urlopen('https://api.coinmarketcap.com/v1/ticker/')
	if coinMarketCapApi.getcode() == 200:
		data = json.load(coinMarketCapApi)
		cleanedCoins = []
		for index, coin in enumerate(data):
			if index > 14:
				break
			else:
				cleanedCoins.append([coin['rank'], coin['name'], coin['market_cap_usd'], coin['price_usd']])
		writeToGoogleDoc(cleanedCoins)
	else:
		return "FAILED " + coinMarketCapApi.getcode()
	return render_template('update.html')
	
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)