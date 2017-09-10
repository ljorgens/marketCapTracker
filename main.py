from flask import Flask, flash, redirect, render_template, request, session, abort
import urllib2
import json
app = Flask(__name__)

	
@app.route("/")
def hello():
	coins = []
	coinMarketCapApi = urllib2.urlopen('https://api.coinmarketcap.com/v1/ticker/')
	if coinMarketCapApi.getcode() == 200:
		data = json.load(coinMarketCapApi)
		coins = data
			# for thing in data
			# 	print thing
	else:
		return "FAILED " + coinMarketCapApi.getcode()
	
	return render_template('hello.html',**locals())
 
if __name__ == "__main__":
    app.run()