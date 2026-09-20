import numpy as np, pandas as pd, mdload, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R0,R1,SESS_END=570,585,960
def day_bars(inst,day):
    d=mdload.load(inst); d['timestamp']=pd.to_datetime(d.timestamp,utc=True)
    loc=d.timestamp.dt.tz_convert('America/New_York')
    d['m']=loc.dt.hour*60+loc.dt.minute; d['day']=loc.dt.normalize()
    return d[(d.day==pd.Timestamp(day,tz='America/New_York'))&(d.m>=R0)&(d.m<SESS_END)]
def panel(ax,s,t):
    s=s[s.m<=min(t.entry_m+90,SESS_END-1)]
    O,H,L,C,M=s.open.values,s.high.values,s.low.values,s.close.values,s.m.values
    x=np.arange(len(O)); n0=int((M<R1).sum())
    ax.add_patch(Rectangle((0,t.ORL),len(O),t.ORH-t.ORL,facecolor="#cfe4cb",alpha=.55,ec="none",zorder=0))
    ax.axhline(t.ORH,color="#6f9c68",lw=1); ax.axhline(t.ORL,color="#6f9c68",lw=1)
    for i in range(len(O)):
        col="#c99a2e" if i<n0 else ("#2c7d72" if C[i]>=O[i] else "#a33c26")
        ax.plot([i,i],[L[i],H[i]],color=col,lw=.6,zorder=2)
        ax.add_patch(Rectangle((i-.32,min(O[i],C[i])),.64,max(abs(C[i]-O[i]),1e-9),fc=col,ec=col,lw=.3,zorder=3))
    def V(mm,col,ls="-"):
        w=np.where(M==mm)[0]
        if len(w): ax.axvline(w[0],color=col,lw=1.0,ls=ls,alpha=.95,zorder=4)
    V(t.break_m,"#8a6209",":"); V(t.return_m,"#7a8b99","--"); V(t.sig_m,"#1f5fa8"); V(t.entry_m,"#111111")
    ax.axhline(t.entry,color="#1f5fa8",lw=1.1); ax.axhline(t.stop,color="#a33c26",lw=1.1)
    if t.has_target: ax.axhline(t.target,color="#0f6b64",lw=1.1)
    def hm(v): return f"{int(v)//60:02d}:{int(v)%60:02d}"
    ax.set_title(f"{t.inst} {t.date} {'LONG' if t.side==1 else 'SHORT'} | brk {hm(t.break_m)} ret {hm(t.return_m)} "
                 f"sig {hm(t.sig_m)} fill {hm(t.entry_m)} | R={t.R_pts:.1f} tgt={t.tgt_R:.1f}R | {t.exit_reason} "
                 f"{t.gross:+.2f}R mfe={t.mfe_R:.2f}R",fontsize=6.6,loc="left")
    ax.set_xticks([]); ax.tick_params(labelsize=5.2)
    lo=min(L.min(),t.stop); hi=max(H.max(),t.stop); pad=.04*(hi-lo)
    ax.set_ylim(lo-pad,hi+pad); ax.set_xlim(-1,len(O))
def grid(rows,fn,sup):
    n=len(rows); r=(n+1)//2
    fig,axes=plt.subplots(r,2,figsize=(13,2.4*r)); axes=np.array(axes).reshape(-1)
    for a in axes[n:]: a.axis("off")
    cache={}
    for a,t in zip(axes,rows):
        k=(str(t["inst"]),str(t["date"]))
        if k not in cache: cache[k]=day_bars(t.inst,t.date)
        panel(a,cache[k],t)
    fig.suptitle(sup,fontsize=10,y=.999); fig.tight_layout(rect=[0,0,1,.985])
    fig.savefig(fn,dpi=105); plt.close(fig)
