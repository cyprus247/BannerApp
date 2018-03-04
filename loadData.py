import pandas as pd
import io
import os
import datetime
from pathlib import Path
import psycopg2


def load_data():
    conn = psycopg2.connect(host="ec2-23-21-198-69.compute-1.amazonaws.com",dbname="daccvcf9bv8j6n", user="nshkapmqhsqoae", password="79f70cb476b17b1ae0db8753bc4011565f80242c94e139b5877c3baa86d4e96e")
    exec_time = datetime.datetime.now()
    print (exec_time.strftime('Data load started at: %Y-%m-%d %H:%M:%S'))
    clicks_df = pd.DataFrame()
    clicks_df.name = "clicks"
    conversions_df = pd.DataFrame()
    conversions_df.name = "conversions"
    impressions_df = pd.DataFrame()
    impressions_df.name = "impressions"

    pathlist = Path("ads").glob('**/*.csv')

    for path in pathlist:
        temp_df = pd.DataFrame()
        # because path is object not string
        path_in_str = str(path)
        if "clicks" in path_in_str:
            temp_df = pd.read_csv(path_in_str)
            temp_df["quarter_file"]=path_in_str.split(os.sep)[1]
            clicks_df = clicks_df.append(temp_df)
        elif "conversions" in path_in_str:
            temp_df = pd.read_csv(path_in_str)
            temp_df["quarter_file"]=path_in_str.split(os.sep)[1]
            conversions_df = conversions_df.append(temp_df)
        elif "impressions" in path_in_str:
            temp_df = pd.read_csv(path_in_str)
            temp_df["quarter_file"]=path_in_str.split(os.sep)[1]
            impressions_df = impressions_df.append(temp_df)
        else:
        	continue

    df_list = [clicks_df,conversions_df,impressions_df]

    def deduplicate (df,key,table,file):
        filename=os.path.join("rejects",file+exec_time.strftime("%Y-%m-%dT%H:%M:%S"+".csv"))
        col_list=list(clicks_df.columns.values).remove('quarter_file')
        cursor = conn.cursor()
        cursor.execute("select {} from {};".format(key,table))
        keys = pd.DataFrame(cursor.fetchall(),columns={key})
        reject_df = df[df[key].isin(keys[key])]
        if len(reject_df.index)!=0 :
            reject_df.to_csv(filename,columns=col_list, index=False)
        remain_df = df[~df[key].isin(keys[key])]
        cursor.close()
        return remain_df


    def insert_to_db(df,table,col_list):
        f = io.StringIO()
        df.to_csv(f, index=False, header=False)  # removed header
        f.seek(0)  # move position to beginning of file before reading
        cursor = conn.cursor()
        #cursor.execute('create table bbbb (a int, b int);COMMIT; ')
        cursor.copy_from(f, table, columns=col_list, sep=',')
        cursor.execute("COMMIT;")
        cursor.close()
        return


    clicks_df = deduplicate(clicks_df,"click_id","clicks","click_rejects")
    conversions_df = deduplicate(conversions_df,"conversion_id","conversions","conversion_rejects")
    insert_to_db(clicks_df,"clicks",['click_id','banner_id','campaign_id','quarter_file'])
    insert_to_db(conversions_df,"conversions",['conversion_id','click_id','revenue','quarter_file'])
    insert_to_db(impressions_df,"impressions",['banner_id','campaign_id','quarter_file'])
    conn.close()
    return

if __name__ == '__main__':
    load_data()