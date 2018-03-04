from flask import Flask, render_template
from tables import create_tbl
import loadData
import campaigns
import db_queries

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/create_tables")
def create_tables():
	create_tbl()
	return render_template("index.html")

@app.route("/load_data")
def load():
	loadData.load_data()
	return render_template("index.html")

campaign_list = campaigns.get_campaigns()
@app.route('/campaigns')
def campaigns():
     return render_template('campaigns.html', campaign_list=campaign_list)	

@app.route('/campaigns/<int:campaign_id>')
def serve_ad(campaign_id):
	import random
	banners= db_queries.get_conversion_banners(campaign_id)
	lazy_banners = db_queries.get_lazy_banners(campaign_id)
	if len(banners) > 10:
		banners = banners[:10]
	elif len(banners) in range(5,9):
		banners = banners #just for symmetry 
	elif len(banners) in range (1,4):
		banners = banners + lazy_banners[:5]
	elif len(banners) == 0:
		banners = lazy_banners[:5]
	final_banner = random.choice(banners)
	return render_template("banner_ad.html", banner_id=final_banner)     	
    

if __name__ == "__main__":
	app.run(debug=True)	