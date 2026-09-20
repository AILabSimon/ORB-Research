#!/usr/bin/env python3
"""Measure TRUE historical spread from paired Dukascopy BID/ASK 1m series.
Spread is not assumed - it is reconstructed. Read-only on the shared store."""
import os, json, sys
import pandas as pd, numpy as np
SH=os.path.expanduser("~/mnt/Dukascopy")
OUT=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/09_VALIDATION/COSTS")
os.makedirs(OUT,exist_ok=True)

def load(f):
    d=pd.read_csv(os.path.join(SH,f),usecols=["timestamp","close"])
    d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True)
    return d.set_index("timestamp")["close"]

def run(name,bidf,askf,tz,windows,unit,unit_name):
    b=load(bidf); a=load(askf)
    j=pd.concat({"bid":b,"ask":a},axis=1).dropna()
    sp=(j["ask"]-j["bid"])/unit
    sp=sp[(sp>=0)&(sp<sp.quantile(0.99999))]
    loc=sp.index.tz_convert(tz); m=loc.hour*60+loc.minute; dw=loc.dayofweek
    res={"instrument":name,"unit":unit_name,"paired_minutes":int(len(sp)),
         "coverage":[str(sp.index[0]),str(sp.index[-1])],"windows":{}}
    for wn,(s,e) in windows.items():
        w=sp[(m>=s)&(m<e)&(dw<5)]
        if len(w)==0: continue
        res["windows"][wn]={"n":int(len(w)),
            "median":round(float(w.median()),4),"mean":round(float(w.mean()),4),
            "p75":round(float(w.quantile(.75)),4),"p90":round(float(w.quantile(.90)),4),
            "p99":round(float(w.quantile(.99)),4)}
    # recent-era check (last 3 years) on the primary window
    wn0=list(windows)[0]; s,e=windows[wn0]
    rec=sp[(sp.index>=sp.index[-1]-pd.Timedelta(days=1095))&(m>=s)&(m<e)&(dw<5)]
    res["recent_3y_"+wn0]={"n":int(len(rec)),"median":round(float(rec.median()),4),
                           "p90":round(float(rec.quantile(.90)),4)}
    with open(os.path.join(OUT,f"SPREAD_{name}.json"),"w") as f: json.dump(res,f,indent=2)
    print(json.dumps(res,indent=2)); return res

if __name__=="__main__":
    which=sys.argv[1]
    if which=="idx":
        run("NAS100","NAS100_1m.csv","NAS100_1m_ASK.csv","America/New_York",
            {"open_0930_0945":(570,585),"cash_0930_1600":(570,960),"powerhour_1500_1600":(900,960)},1.0,"index points")
        run("US500","US500_1m.csv","US500_1m_ASK.csv","America/New_York",
            {"open_0930_0945":(570,585),"cash_0930_1600":(570,960),"powerhour_1500_1600":(900,960)},1.0,"index points")
    else:
        run("EURUSD","EURUSD_1M.csv","EURUSD_1m_ASK.csv","Europe/London",
            {"london_0800_0815":(480,495),"ny_1330_1345":(810,825),"london_day_0700_1700":(420,1020)},0.0001,"pips")
        run("GBPUSD","GBPUSD_1M.csv","GBPUSD_1m_ASK.csv","Europe/London",
            {"london_0800_0815":(480,495),"ny_1330_1345":(810,825),"london_day_0700_1700":(420,1020)},0.0001,"pips")
