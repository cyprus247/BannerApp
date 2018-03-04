import psycopg2
import datetime

def get_quarter():
	now = datetime.datetime.now()
	if 0<=now.minute<=14:
		return 1
	elif 15<=now.minute<=329:
		return 2
	elif 30<=now.minute<=44:
		return 3
	elif 45<=now.minute<=59:	
		return 4

def get_conversion_banners(campaign_id):
	""" this will return an ordered list of the banner_ids 
	with associated conversion ordered by descending revenue """
	conn = psycopg2.connect(host="ec2-23-21-198-69.compute-1.amazonaws.com",dbname="daccvcf9bv8j6n", user="nshkapmqhsqoae", password="79f70cb476b17b1ae0db8753bc4011565f80242c94e139b5877c3baa86d4e96e")
	cur = conn.cursor()
	cur.execute(""" select c.banner_id,c.campaign_id,
					sum(coalesce(s.revenue,0)) 
					from clicks c
					left join conversions s
					on s.click_id = c.click_id
					where c.campaign_id = {}
					and c.quarter_file = {}
					group by c.banner_id, c.campaign_id
					order by sum(coalesce(s.revenue,0)) desc,c.campaign_id
					""".format(campaign_id,get_quarter()))
	rows = cur.fetchall()
	rows_list = []
	for row in rows:
		rows_list.append(row[0]) 
	conn.close()
	return rows_list