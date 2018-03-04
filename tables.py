import psycopg2


def create_tbl():
	conn = psycopg2.connect(host="ec2-23-21-198-69.compute-1.amazonaws.com",dbname="daccvcf9bv8j6n", user="nshkapmqhsqoae", password="79f70cb476b17b1ae0db8753bc4011565f80242c94e139b5877c3baa86d4e96e")

	cur = conn.cursor()
	cur.execute(""" drop table if exists clicks """)
	cur.execute(""" create table if not exists clicks 
		(click_id INT PRIMARY KEY,banner_id INT,campaign_id INT, quarter_file INT) """)
	cur.execute(""" drop table if exists conversions """)
	cur.execute(""" create table if not exists conversions 
		(conversion_id INT PRIMARY KEY,click_id INT,revenue DECIMAL (12,6), quarter_file INT) """)
	cur.execute(""" drop table if exists impressions """)
	cur.execute(""" create table if not exists impressions 
		(banner_id INT ,campaign_id INT, quarter_file INT) """)
	cur.execute(""" commit; """)


	cur.close()   
	conn.close()
	return

if __name__ == '__main__':
    create_tbl()