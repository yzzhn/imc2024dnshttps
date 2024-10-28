import pandas as pd
import numpy as np
import os
import datetime
import json
# import local files
import preprocessfns as fns


def count_rrsig_overlap(date_l, df_overlap, datedir, file_name="apex_https.csv"):
    
    df_rrsig = pd.DataFrame(columns=['date', 'num_rrsig'])
    
    for day in date_l:
        print ("processing ", day, "...")
        
        date_str = day.strftime("%Y-%m-%d")
        month_str = day.strftime("%Y-%m")
        log_path = os.path.join(datedir, month_str, date_str, file_name)
        
        try:
            df = pd.read_csv(log_path)
        except:
            pass

        if "www" in file_name: # parse apex name out 
             df['domain'] = df['domain'].apply(lambda x: x.split("www.")[-1])
            
        df_merge = df.merge(df_overlap, how='inner', left_on="domain", right_on='apex')
        df_merge["https.dict"] = df_merge["https"].apply(lambda x: json.loads(x))
        df_merge["rrsig.exist"] = df_merge["https.dict"].apply(lambda x: fns.if_key_exists(x, "RRSIG"))
        
        tmp_dict = dict({'date': date_str, \
                         'num_rrsig': df_merge['rrsig.exist'].sum()})
        
        tmp_dict = {key:[value] for key, value in tmp_dict.items()}
        
        df_rrsig = pd.concat([df_rrsig, pd.DataFrame(tmp_dict)], ignore_index=True)
    return df_rrsig


def count_adbit_overlap(date_l, df_overlap, datadir, domtype):
    
    df_adbit = pd.DataFrame(columns=['date', 'num_adbit'])
    
    for day in date_l:
        print ("processing ", day, "...")
        
        date_str = day.strftime("%Y-%m-%d")
        month_str = day.strftime("%Y-%m")
        log_pathapex = os.path.join(datadir, month_str, date_str, f"{domtype}_https.csv")
        log_pathad = os.path.join(datadir, month_str, date_str, f"{domtype}_flags.csv")
        
        try:
            dfapex = pd.read_csv(log_pathapex)
            dfad = pd.read_csv(log_pathad)
        except:
            print("no logs")
            pass
        
        
        if "www" in log_pathapex: # parse apex name out 
             dfapex['domain'] = dfapex['domain'].apply(lambda x: x.split("www.")[-1])
             dfad['domain'] = dfad['domain'].apply(lambda x: x.split("www.")[-1])
            
        df_mergeoverlap = dfapex.merge(df_overlap, how="inner", left_on="domain", right_on='apex')
        
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
            
    
    ### compute httpsrr rrsig rate given the time range 
    apex_rrsig = count_rrsig_overlap(date_l1, df_overlap1, DataRawDir, "apex_https.csv")
    apex_https = pd.read_csv("../data/processed/overlap/adoption_apex_httpsrr1.csv")
    apex_rrsigmerge = apex_rrsig.merge(apex_https, how='inner', on='date')
    apex_rrsigmerge.to_csv("../data/processed/overlap/rrsig_apex1.csv", index=False)

    
    www_rrsig = count_rrsig_overlap(date_l1, df_overlap1, DataRawDir, "www_https.csv")
    www_https = pd.read_csv("../data/processed/overlap/adoption_www_httpsrr1.csv")
    www_rrsigmerge = www_rrsig.merge(www_https, how='inner', on='date')
    www_rrsigmerge.to_csv("../data/processed/overlap/rrsig_www1.csv", index=False)

    ### compute adbit rate given the time range
    apex_ad = count_adbit_overlap(date_l1, df_overlap1, DataRawDir, "apex")
    apex_ad.to_csv("../data/processed/overlap/adbit_apex1.csv", index=False)
    
    www_ad = count_adbit_overlap(date_l1, df_overlap1, DataRawDir, "www")
    www_ad.to_csv("../data/processed/overlap/adbit_www1.csv", index=False)

    ### Time range 2
    start_d = datetime.datetime(2023,8,2)
    end_d = datetime.datetime(2024,4,1)
    ndays = (end_d - start_d).days
    date_l2 = [start_d + datetime.timedelta(days=i) for i in range(ndays)]
    print("Time range 2, firstday:", date_l2[0], "lastday:", date_l2[-1])

    ### compute httpsrr rrsig rate given the time range 
    apex_rrsig = count_rrsig_overlap(date_l2, df_overlap2, DataRawDir, "apex_https.csv")
    apex_https = pd.read_csv("../data/processed/overlap/adoption_apex_httpsrr2.csv")
    apex_rrsigmerge = apex_rrsig.merge(apex_https, how='inner', on='date')
    apex_rrsigmerge.to_csv("../data/processed/overlap/rrsig_apex2.csv", index=False)

    www_rrsig = count_rrsig_overlap(date_l2, df_overlap2, DataRawDir, "www_https.csv")
    www_https = pd.read_csv("../data/processed/overlap/adoption_www_httpsrr2.csv")
    www_rrsigmerge = www_rrsig.merge(www_https, how='inner', on='date')
    www_rrsigmerge.to_csv("../data/processed/overlap/rrsig_www2.csv", index=False)

    ### compute adbit rate given the time range
    apex_ad = count_adbit_overlap(date_l2, df_overlap2, DataRawDir, "apex")
    apex_ad.to_csv("../data/processed/overlap/adbit_apex2.csv", index=False)
    
    www_ad = count_adbit_overlap(date_l2, df_overlap2, DataRawDir, "www")
    www_ad.to_csv("../data/processed/overlap/adbit_www2.csv", index=False)

    


