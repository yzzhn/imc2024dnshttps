import pandas as pd
import numpy as np
import os
import datetime


def count_httpsrr_overlap(date_l, overlapdf, datedir, file_name="apex_https.csv"):
    adoptiondf = pd.DataFrame(columns=['date', 'num_httpsrr'])
    
    for day in date_l:
        print ("processing ", day, "...")
        date_str = day.strftime("%Y-%m-%d")
        month_str = day.strftime("%Y-%m")
        log_path = os.path.join(datedir, month_str, date_str, file_name)
        try:
            df = pd.read_csv(log_path)
        except:
            print("error")
            pass
    
        if file_name == "www_https.csv":
             df['domain'] = df['domain'].apply(lambda x: x.split("www.")[-1])
            
        df_merge = df.merge(overlapdf, how='inner', left_on="domain", right_on='apex')
        tmp_dict = dict({'date': date_str, 'num_httpsrr': df_merge.shape[0]})
        tmp_dict = {key:[value] for key, value in tmp_dict.items()}
        adoptiondf = pd.concat([adoptiondf, pd.DataFrame(tmp_dict)], ignore_index=True)
        clear_output(wait=True)    
    return adoptiondf

if __name__ == "__main__":
    # set this to data directory
    DataRawDir = "../raw"
    
    # Read overlapped domain list
    df_overlap1 = pd.read_csv("../data/processed/overlap/overlapdom_part1.csv")
    df_overlap2 = pd.read_csv("../data/processed/overlap/overlapdom_part2.csv")
    
    # Time range from beginning to end
    start_d = datetime.datetime(2023,5,8)
    end_d = datetime.datetime(2023,8,2)
    ndays = (end_d - start_d).days
    date_l1 = [start_d + datetime.timedelta(days=i) for i in range(ndays)]
    print("Time range 1, firstday:", date_l1[0], "lastday:", date_l1[-1])
            
    
    start_d = datetime.datetime(2023,8,2)
    end_d = datetime.datetime(2024,4,1)
    ndays = (end_d - start_d).days
    date_l2 = [start_d + datetime.timedelta(days=i) for i in range(ndays)]
    print("Time range 2, firstday:", date_l1[0], "lastday:", date_l1[-1])
    
    apex_httpsrr1 = count_httpsrr_overlap(date_l1, df_overlap1, DataRawDir, "apex_https.csv")
    apex_httpsrr1.to_csv("../data/processed/overlap/adoption_apex_httpsrr1.csv", index=False)
    
    apex_httpsrr2 = count_httpsrr_overlap(date_l2, df_overlap2, DataRawDir, "apex_https.csv")
    apex_httpsrr2.to_csv("../data/processed/overlap/adoption_apex_httpsrr2.csv", index=False)

    www_httpsrr1 = count_httpsrr_overlap(date_l1, df_overlap1, DataRawDir, "www_https.csv")
    www_httpsrr1.to_csv("../data/processed/overlap/adoption_www_httpsrr1.csv", index=False)
    
    www_httpsrr2 = count_httpsrr_overlap(date_l2, df_overlap2, DataRawDir, "www_https.csv")
    www_httpsrr2 = pd.read_csv("../data/processed/overlap/adoption_www_httpsrr2.csv")


