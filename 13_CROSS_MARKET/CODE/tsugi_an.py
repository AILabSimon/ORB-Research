import numpy as np, pandas as pd

RNG=np.random.default_rng(20260917)
def rb(a,b):
    """rank-biserial correlation from Mann-Whitney U."""
    if len(a)<10 or len(b)<10: return np.nan,np.nan
    a=np.asarray(a,float); b=np.asarray(b,float)
    all_=np.concatenate([a,b]); r=pd.Series(all_).rank().values
    ra=r[:len(a)].sum(); u=ra-len(a)*(len(a)+1)/2.
    rbc=2*u/(len(a)*len(b))-1
    # permutation p on the rank-biserial itself
    lab=np.zeros(len(all_),bool); lab[:len(a)]=True; cnt=0
    for _ in range(2000):
        RNG.shuffle(lab)
        uu=r[lab].sum()-len(a)*(len(a)+1)/2.
        if abs(2*uu/(len(a)*len(b))-1)>=abs(rbc): cnt+=1
    return rbc,(cnt+1)/2001.
def perm(a,b,n=10000):
    a=np.asarray(a,float); b=np.asarray(b,float); obs=a.mean()-b.mean()
    pool=np.concatenate([a,b]); na=len(a); cnt=0
    for _ in range(n):
        RNG.shuffle(pool)
        if abs(pool[:na].mean()-pool[na:].mean())>=abs(obs): cnt+=1
    return obs,(cnt+1)/(n+1)
def qtab(d,feat,q=5,lbl=None):
    x=d[feat]
    try: g=pd.qcut(x,q,labels=False,duplicates="drop")
    except Exception: return
    print(f"  {lbl or feat}")
    for k in sorted(pd.Series(g).dropna().unique()):
        s=d[g==k]; net=s.net.values
        y=s.date.str[:4].astype(int).values
        dev=net[y<=2021].mean() if (y<=2021).any() else np.nan
        hol=net[y>2021].mean() if (y>2021).any() else np.nan
        print(f"    Q{int(k)+1} [{s[feat].min():.3f}-{s[feat].max():.3f}] n={len(s):4d} "
              f"net={net.mean():+.4f} win={100*(net>=.05).mean():4.1f}% "
              f"dev={dev:+.3f} hol={hol:+.3f}")
def wl(d,feat):
    w=d[d.net>=.05][feat].dropna(); lo=d[d.net<=-.05][feat].dropna()
    r,p=rb(w,lo)
    print(f"  {feat:22s} win_mean={w.mean():+.4f} loss_mean={lo.mean():+.4f} "
          f"diff={w.mean()-lo.mean():+.4f} rank-biserial r={r:+.4f} p={p:.4f}")
