import pandas as pd, numpy as np
RNG=np.random.default_rng(2026)
CELLS=[(tf,u,be) for tf in (1,5) for u in ("HOLD","DEEP") for be in (0,1)]
def ci(v,n=4000):
    b=np.array([RNG.choice(v,len(v),True).mean() for _ in range(n)])
    return np.percentile(b,2.5),np.percentile(b,97.5)
def block(inst,rule,out):
    P=lambda s: out.append(s)
    P(f"\n### {inst} — draw rule: {rule}\n")
    P("| cell | cand | gate pass | gate rej (no draw / rr<2) | trades | /yr | GROSS | 95% CI | win% | meanW | meanL | MFE med | MAE med | 1R | 2R | 3R | stop | inval | target | BE | NET |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for tf,u,be in CELLS:
        t=pd.read_parquet(f"../WORK/CW_{inst}_{rule}_{tf}m_{u}_BE{be}.parquet")
        j=pd.read_parquet(f"../WORK/CWrej_{inst}_{rule}_{tf}m_{u}_BE{be}.parquet")
        nd=int((j.reason=="no_draw").sum()); rl=int((j.reason=="rr_below_2").sum())
        g=t.gross.values; lo,hi=ci(g) if len(g)>=20 else (np.nan,np.nan)
        w=g[g>0]; l=g[g<0]
        er=t.exit_reason.value_counts()
        pc=lambda k: 100*er.get(k,0)/len(t)
        P(f"| {tf}m {u} BE{be} | {len(t)+len(j)} | {len(t)} | {nd} / {rl} | {len(t)} | {len(t)/10.7:.0f} | "
          f"**{g.mean():+.4f}** | [{lo:+.3f}, {hi:+.3f}] | {100*(g>0).mean():.1f} | {w.mean():+.2f} | {l.mean():+.2f} | "
          f"{t.mfe_R.median():.2f} | {t.mae_R.median():.2f} | {100*(t.mfe_R>=1).mean():.0f}% | {100*(t.mfe_R>=2).mean():.0f}% | "
          f"{100*(t.mfe_R>=3).mean():.0f}% | {pc('stop'):.0f}% | {pc('invalidation'):.0f}% | {pc('target'):.0f}% | {pc('be_stop'):.0f}% | {t.net.mean():+.3f} |")
def extras(inst,rule,out):
    t=pd.read_parquet(f"../WORK/CW_{inst}_{rule}_1m_DEEP_BE0.parquet")
    j=pd.read_parquet(f"../WORK/CWrej_{inst}_{rule}_1m_DEEP_BE0.parquet")
    a=pd.concat([t.rr_pre.rename("rr"), j.rr]).dropna()
    out.append(f"\n**available_RR across all {len(a)} gate evaluations ({inst} {rule} 1m DEEP):** "
               f"median {a.median():.2f}, p75 {a.quantile(.75):.2f}, p90 {a.quantile(.90):.2f}; "
               f"<0.5 on {100*(a<0.5).mean():.0f}%, >=2 on {100*(a>=2).mean():.1f}%")
    out.append(f"\n**accepted available_RR:** median {t.rr_pre.median():.2f}, p90 {t.rr_pre.quantile(.9):.2f}, max {t.rr_pre.max():.1f}")
    dt=t.draw_type.value_counts()
    out.append("\n**draw type used:** " + ", ".join(f"{k} {v}" for k,v in dt.items()))
    out.append("\n**year-by-year gross (1m DEEP BE0):** " + "  ".join(
        f"{y}:{t[t.yr==y].gross.mean():+.2f}(n={len(t[t.yr==y])})" for y in sorted(t.yr.unique())))
