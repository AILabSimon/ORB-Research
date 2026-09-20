import pandas as pd, json, glob, os
M=os.path.expanduser("~/mnt/Market Data")
def load(inst,tf="1m",side="BID"):
    base=f"{M}/Canonical/{tf}/{inst}/{side}"
    v=open(f"{base}/CURRENT").read().strip(); chosen={}
    while v:
        man=json.load(open(f"{base}/{v}/MANIFEST.json"))
        for f in glob.glob(f"{base}/{v}/*.parquet"):
            yr=os.path.basename(f).split("_")[-1].split(".")[0]; chosen.setdefault(yr,f)
        v=man.get("parent_version")
    d=pd.concat([pd.read_parquet(f) for f in sorted(chosen.values())]).sort_values("timestamp").reset_index(drop=True)
    d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True); return d
