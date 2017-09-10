from flask import Flask, render_template
import urllib2
import json
app = Flask(__name__)

	
@app.route("/")
def hello():
	coinMarketCapApi = urllib2.urlopen('https://api.coinmarketcap.com/v1/ticker/')
	if coinMarketCapApi.getcode() == 200:
		data = json.load(coinMarketCapApi)
		for thing in data:
			return render_template('%s.html' % "hello")

			# for thing in data
			# 	print thing
	else:
		return "FAILED " + coinMarketCapApi.getcode()
 
if __name__ == "__main__":
    app.run()