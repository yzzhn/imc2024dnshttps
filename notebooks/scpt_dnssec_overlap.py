import pandas as pd
import numpy as np
import os
import datetime

def rrsig_adopt(date_l, df_overlap, datedir, file_name="apex_https.csv"):
    
    df_rrsig = pd.DataFrame(columns=['date', 'num_rrsig'])
    
    for day in date_l:
        print ("processing ", day, "...")
        clear_output(wait=True)
        date_str = day.strftime("%Y-%m-%d")
        month_str = day.strftime("%Y-%m")
        log_path = os.path.join(datedir, month_str, date_str, file_name)
        try:
            df = pd.read_csv(log_path)
        except:
            pass

        if file_name == "www_https.csv":
             df['domain'] = df['domain'].apply(lambda x: x.split("www.")[-1])

        df_noerr['apex'] = df_noerr['domain'].apply(lambda x: x.split("www.")[-1])
        df_merge = df.merge(df_overlap, how='inner', on='apex')
        df_merge["https.dict"] = df_merge["https"].apply(lambda x: json.loads(x))
        df_merge["rrsig.exist"] = df_merge["https.dict"].apply(lambda x: if_key_exists(x, "RRSIG"))
        tmp_dict = dict({'date': date_str, \
                         'num_rrsig': df_merge['rrsig.exist'].sum()})
        tmp_dict = {key:[value] for key, value in tmp_dict.items()}
        df_rrsig = pd.concat([df_rrsig, pd.DataFrame(tmp_dict)], ignore_index=True)
    return df_rrsig


def adbit(df_overlap, date_l, domtype):
    df_adbit = pd.DataFrame(columns=['date', 'num_adbit'])
    for day in date_l:
        print ("processing ", day, "...")
        clear_output(wait=True)
        date_str = day.strftime("%Y-%m-%d")
        log_pathapex = os.path.join("/data/parsed", date_str, domtype + "_https.csv")
        log_pathad = os.path.join("/data/parsed", date_str, domtype + "_flags.csv")
        
        #if os.path.exists(log_pathapex) and os.path.exists(log_pathad):
        try:
            dfapex = pd.read_csv(log_pathapex)
            dfad = pd.read_csv(log_pathad)
        except:
            pass
        
        df_noerr = dfapex.loc[dfapex["error"]=='{}']
        
        # comment if for apex not www
        df_noerr['apex'] = df_noerr['domain'].apply(lambda x: x.split("www.")[-1]) 
        df_mergeoverlap = df_noerr.merge(df_overlap, how="inner", on='apex')
        
        df_merge = df_mergeoverlap.merge(dfad, how='left', on="domain")
        df_merge['flags'] = df_merge['flags'].fillna("noflag")
        df_merge = df_merge.fillna(False)
        
        tmp_dict = dict({'date': date_str, \
                         'num_adbit': df_merge['AD'].sum()})
        tmp_dict = {key:[value] for key, value in tmp_dict.items()}
        df_adbit = pd.concat([df_adbit, pd.DataFrame(tmp_dict)], ignore_index=True)
    return df_adbit


if __name__ == "__main__":
    # set this to data directory
    DataRawDir = "/scratch/yz6me/dnsdata/httpsrr/"
    
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


