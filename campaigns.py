import psycopg2


def get_campaigns():
	conn = psycopg2.connect(host="ec2-23-21-198-69.compute-1.amazonaws.com",dbname="daccvcf9bv8j6n", user="nshkapmqhsqoae", password="79f70cb476b17b1ae0db8753bc4011565f80242c94e139b5877c3baa86d4e96e")
	cur = conn.cursor()
	cur.execute(""" select distinct campaign_id from clicks 
					order by campaign_id;""")
	rows = cur.fetchall()
	rows_list = []
	for row in rows:
		rows_list.append(row[0]) 
	conn.close()
	return rows_list


if __name__ == '__main__':
    get_campaigns()	