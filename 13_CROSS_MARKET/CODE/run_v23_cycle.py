#!/usr/bin/env python3
"""
SINGLE LOCAL ENTRY POINT — CeeWilli Entry-02 v2.3 rebuild + external FVG diagnostic + visual
pack. Issue #3 ("CeeWilli v2.3 rebuild + external FVG diagnostic").

Run from the researcher's Mac, from this directory, against the canonical market-data store
already documented in `13_CROSS_MARKET/DATA/CROSS_MARKET_DATA_INVENTORY.md` and read by
mdload.py (`~/mnt/Market Data`):

    cd 13_CROSS_MARKET/CODE
    python3 run_v23_cycle.py

Optional flags:
    --instruments NAS100,US500   (default: NAS100,US500 -- the two validated index proxies)
    --skip-visuals                skip the PNG review-pack render step
    --n-each 2                    examples per visual-pack scenario class (default 2)

What it does, in order:
  1. Runs cw_v23_selftest.py (synthetic data, no market data needed). Aborts before touching
     real data if any self-test fails -- do not trust the mechanics on real data otherwise.
  2. Loads each instrument once via cw_entry02.load_ny, caches to WORK/ny_{inst}.parquet.
  3. Runs all 16 v2.3 cells {1m,5m} x {HOLD,DEEP} x {BE off,on} x {DRAW-NQ,DRAW-SQ} per
     instrument, saves T/J to WORK/, and writes gross-first economics to
     OUTPUTS/CW_ENTRY02_V23_ECONOMICS.md (NEW file -- v2.2's OUTPUTS/CW_ENTRY02_ECONOMICS.md
     is left untouched as superseded/provisional historical evidence).
  4. Runs the external-FVG diagnostic (cw_fvg_diag) against every cell's T/J, writes
     contingency counts/rates to OUTPUTS/CW_FVG_DIAGNOSTIC_V23.md, and the full annotated
     per-event frames to WORK/ (for follow-up analysis, not committed).
  5. Renders the five-scenario visual review pack (cw_fvg_figs) to
     WORK/FVG_VISUAL_PACK/*.png (not committed -- binary output, regenerate locally).

Nothing here selects between DRAW-NQ/DRAW-SQ, chooses a trend definition, adds an FVG
threshold, or turns the FVG observation into an Entry-02 filter. All of that is explicitly
out of scope for this cycle (see the issue).
"""
import argparse, os, sys, traceback
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "OUTPUTS")
WORK = os.path.join(HERE, "..", "WORK")

def die(msg):
    print(f"\nABORT: {msg}\n", file=sys.stderr)
    sys.exit(1)

def check_data_store():
    mount = os.path.expanduser("~/mnt/Market Data")
    if not os.path.isdir(mount):
        die(f"Canonical market-data store not found at {mount!r}. This script must be run "
            f"on the researcher's Mac with that mount present -- see "
            f"13_CROSS_MARKET/DATA/CROSS_MARKET_DATA_INVENTORY.md. Nothing was executed.")

def run_selftests():
    print("=== [1/5] self-tests (synthetic data) ===")
    import cw_v23_selftest as ST
    try:
        ST.run_all()
    except SystemExit:
        die("self-tests FAILED -- fix cw_entry02.py / cw_fvg_diag.py before trusting real-data output.")

CELLS = [(tf, u22, be, rule) for tf in (1, 5) for u22 in ("HOLD", "DEEP")
         for be in (False, True) for rule in ("NQ", "SQ")]

def load_and_cache(inst):
    import cw_entry02 as CW
    cache_fn = os.path.join(WORK, f"ny_{inst}.parquet")
    if os.path.exists(cache_fn):
        print(f"  {inst}: loading cached {cache_fn}")
        d = pd.read_parquet(cache_fn)
    else:
        print(f"  {inst}: loading from canonical store...")
        d = CW.load_ny(inst)
        d.to_parquet(cache_fn)
    return d

def run_cells(inst, d):
    import cw_entry02 as CW
    results = {}
    for tf, u22, be, rule in CELLS:
        T, J = CW.run(inst, tf=tf, u22=u22, be=be, d=d, draw_rule=rule)
        T.to_parquet(os.path.join(WORK, f"CW_{inst}_{rule}_{tf}m_{u22}_BE{int(be)}.parquet"))
        J.to_parquet(os.path.join(WORK, f"CWrej_{inst}_{rule}_{tf}m_{u22}_BE{int(be)}.parquet"))
        results[(tf, u22, be, rule)] = (T, J)
        print(f"  {inst} {tf}m {u22} BE{int(be)} {rule}: {len(T)} trades, {len(J)} gate-rejects")
    return results

def write_economics(inst_results, instruments):
    import cw_report as R
    out = ["# CEEWILLI ENTRY-02 v2.3 -- FULL ECONOMICS, 16 CELLS, GROSS FIRST",
           "PENDING LOCAL EXECUTION until this file is regenerated with real numbers below "
           "this line by `run_v23_cycle.py` on the researcher's Mac. See ANALYST_CURRENT.md "
           "for the v2.2 superseded/provisional result this supersedes.\n",
           "Both DRAW-NQ and DRAW-SQ are reported. **Neither is selected** (§D.11.3, H29)."]
    for inst in instruments:
        for rule in ("NQ", "SQ"):
            out.append(f"\n### {inst} -- draw rule: {rule}\n")
            R.block(inst, rule, out)
            R.extras(inst, rule, out)
    fn = os.path.join(OUT, "CW_ENTRY02_V23_ECONOMICS.md")
    with open(fn, "w") as f: f.write("\n".join(out))
    print(f"  wrote {fn}")

def run_fvg_diagnostic(inst_results, d_by_inst, instruments):
    import cw_fvg_diag as FD
    out = ["# EXTERNAL FVG / FAILED-BREAK DIAGNOSTIC -- v2.3, issue #3",
           "PENDING LOCAL EXECUTION until this file is regenerated with real numbers below "
           "this line. DIAGNOSTIC ONLY -- not an Entry-02 filter, no FVG threshold, no trend "
           "rule (see cw_fvg_diag.TREND_BIAS_NOTE)."]
    all_ann = []
    for inst in instruments:
        d = d_by_inst[inst]
        fvg_cache = {}   # shared across all 16 cells for this instrument -- same (inst,tf) day
                          # bars are resampled/scanned once, not once per cell
        for (tf, u22, be, rule), (T, J) in inst_results[inst].items():
            ann = FD.annotate(T, J, inst, tf, d=d, cache=fvg_cache)
            if len(ann):
                ann.to_parquet(os.path.join(WORK, f"FVG_ANN_{inst}_{rule}_{tf}m_{u22}_BE{int(be)}.parquet"))
                all_ann.append(ann)
                label = f"{inst} {tf}m {u22} BE{int(be)} {rule}"
                out.append(FD.build_report(ann, label))
        for tf in (1, 5):
            census = FD.census_all_days(inst, tf, d=d, cache=fvg_cache)
            census.to_parquet(os.path.join(WORK, f"FVG_CENSUS_{inst}_{tf}m.parquet"))
            n_above = int(census.ext_above_present.sum()); n_below = int(census.ext_below_present.sum())
            out.append(f"\n**{inst} {tf}m full-population census** (n={len(census)} ORB days, "
                       f"independent of any break): external FVG above ORH present on {n_above} "
                       f"days, below ORL present on {n_below} days.")
    if all_ann:
        pooled = pd.concat(all_ann, ignore_index=True)
        out.append(FD.build_report(pooled, "ALL CELLS / ALL INSTRUMENTS POOLED"))
    fn = os.path.join(OUT, "CW_FVG_DIAGNOSTIC_V23.md")
    with open(fn, "w") as f: f.write("\n".join(out))
    print(f"  wrote {fn}")
    return pd.concat(all_ann, ignore_index=True) if all_ann else pd.DataFrame()

def run_visual_pack(pooled_ann, d_by_inst, n_each):
    import cw_fvg_figs as FF
    outdir = os.path.join(WORK, "FVG_VISUAL_PACK")
    if len(pooled_ann) == 0:
        print("  no annotated events -- skipping visual pack")
        return
    # one reference cell keeps the pack a manageable size: 1m DEEP BE0 NQ, if present
    ref = pooled_ann[(pooled_ann.u22 == "DEEP") & (pooled_ann.be == 0) & (pooled_ann.draw_rule == "NQ") & (pooled_ann.tf == 1)]
    src = ref if len(ref) else pooled_ann
    written = FF.build_pack(src, d_by_inst, outdir, n_each=n_each)
    print(f"  wrote {len(written)} panel(s) to {outdir}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instruments", default="NAS100,US500")
    ap.add_argument("--skip-visuals", action="store_true")
    ap.add_argument("--n-each", type=int, default=2)
    args = ap.parse_args()
    instruments = [s.strip() for s in args.instruments.split(",") if s.strip()]

    # cw_report.py reads "../WORK/..." relative to CWD -- chdir here so the single-command
    # invocation works from any starting directory, not just from inside CODE/.
    os.chdir(HERE)
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    run_selftests()

    check_data_store()
    print("=== [2/5] loading instruments ===")
    d_by_inst = {inst: load_and_cache(inst) for inst in instruments}

    print("=== [3/5] running 16 v2.3 cells per instrument ===")
    inst_results = {inst: run_cells(inst, d_by_inst[inst]) for inst in instruments}
    write_economics(inst_results, instruments)

    print("=== [4/5] external FVG diagnostic ===")
    pooled_ann = run_fvg_diagnostic(inst_results, d_by_inst, instruments)

    if not args.skip_visuals:
        print("=== [5/5] visual review pack ===")
        run_visual_pack(pooled_ann, d_by_inst, args.n_each)
    else:
        print("=== [5/5] visual review pack SKIPPED (--skip-visuals) ===")

    print("\nDone. Markdown reports in OUTPUTS/, raw parquet + PNGs in WORK/ (gitignored -- "
          "not committed). Update ANALYST_CURRENT.md by hand with the headline numbers before "
          "committing.")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
