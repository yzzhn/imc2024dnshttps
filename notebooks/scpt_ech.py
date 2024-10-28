import pandas as pd
import numpy as np
import os
import datetime
import json
# import local files
import preprocessfns as fns

def count_ech(date_l, datadir, dom_type):
    df_ech = pd.DataFrame(columns=['date', 'num_ech'])
    
    for day in date_l:
        print ("processing ", day, "...")
        date_str = day.strftime("%Y-%m-%d")
        month_str = day.strftime("%Y-%m")
        log_path = os.path.join(datadir, month_str, date_str, f"{dom_type}_https.csv")
        print("read logs:", log_path)
        try:
            df = pd.read_csv(log_path)
        except:
            pass
        df["https.dict"] = df["https"].apply(lambda x: json.loads(x))
        df["https.ech"] = df["https.dict"].apply(lambda x: fns.get_https_fields(x, "HTTPS", "svcb.ech"))
        
        tmp_dict = dict({'date': date_str, \
                         'num_ech': df.loc[df["https.ech"].notna()].shape[0]})
        tmp_dict = {key:[value] for key, value in tmp_dict.items()}
        df_ech = pd.concat([df_ech, pd.DataFrame(tmp_dict)], ignore_index=True)
    return df_ech
    

if __name__ == "__main__":
    # set this to data directory
    DataRawDir = "/scratch/yz6me/dnsdata/httpsrr/"

    # Time range beginning to end
    start_d = datetime.datetime(2023,5,8)
    end_d = datetime.datetime(2024,10,1)
    ndays = (end_d - start_d).days
    date_l0 = [start_d + datetime.timedelta(days=i) for i in range(ndays)]
    print("first day:", date_l0[0], "last day:", date_l0[-1])

    ### compute httpsrr rrsig rate given the time range 
    apex_ech = count_ech(date_l0, DataRawDir, "apex")
    apex_https = pd.read_csv("../data/processed/alldom/adoption_apex_httpsrr.csv")
    apex_ech_merge = apex_ech.merge(apex_https, how='inner', on='date')
    apex_ech_merge.to_csv("../data/processed/alldom/ech_apex.csv", index=False)

    www_ech = count_ech(date_l0, DataRawDir, "www")
    www_https = pd.read_csv("../data/processed/alldom/adoption_www_httpsrr.csv")
    www_ech_merge = www_ech.merge(www_https, how='inner', on='date')
    www_ech_merge.to_csv("../data/processed/alldom/ech_www.csv", index=False)


