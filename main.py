from flask import Flask, flash, redirect, render_template, request, session, abort
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import os
app = Flask(__name__)

	
@app.route("/")
def hello():
	coins = []
	coinMarketCapApi = urlopen('https://api.coinmarketcap.com/v1/ticker/')
	if coinMarketCapApi.getcode() == 200:
		data = json.load(coinMarketCapApi)
		coins = data
			# for thing in data
			# 	print thing
	else:
		return "FAILED " + coinMarketCapApi.getcode()
	
	return render_template('hello.html',**locals())
 
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)