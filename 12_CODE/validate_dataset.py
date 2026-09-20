#!/usr/bin/env python3
"""Validate a shared Dukascopy 1m CSV for ORB research use. Read-only on the shared store."""
import sys, json, hashlib, os
import pandas as pd, numpy as np

SHARED = os.path.expanduser("~/mnt/Dukascopy")
OUT = os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/06_DATA/VALIDATION")

def main(name, fname, sess_tz, sess_start, sess_end):
    path = os.path.join(SHARED, fname)
    df = pd.read_csv(path, usecols=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    n = len(df)
    dups = int(df["timestamp"].duplicated().sum())
    mono = bool(df["timestamp"].is_monotonic_increasing)
    ohlc_bad = int(((df["high"] < df[["open","close"]].max(axis=1)) |
                    (df["low"]  > df[["open","close"]].min(axis=1)) |
                    (df["high"] < df["low"])).sum())
    nonpos = int((df[["open","high","low","close"]] <= 0).any(axis=1).sum())
    zerorange = int((df["high"] == df["low"]).sum())

    loc = df["timestamp"].dt.tz_convert(sess_tz)
    df["d"] = loc.dt.date
    mins = loc.dt.hour*60 + loc.dt.minute
    dow = loc.dt.dayofweek
    in_sess = (mins >= sess_start) & (mins < sess_end) & (dow < 5)
    s = df[in_sess]
    # per-session-day bar counts
    cnt = s.groupby("d").size()
    expected = sess_end - sess_start
    full_days = int((cnt == expected).sum())
    part_days = int((cnt < expected).sum())
    res = {
      "dataset": name, "file": path, "rows": n,
      "coverage_start_utc": str(df["timestamp"].iloc[0]), "coverage_end_utc": str(df["timestamp"].iloc[-1]),
      "duplicate_timestamps": dups, "monotonic": mono,
      "ohlc_violations": ohlc_bad, "nonpositive_prices": nonpos, "zero_range_bars": zerorange,
      "session_tz": sess_tz, "session_window_local": f"{sess_start//60:02d}:{sess_start%60:02d}-{sess_end//60:02d}:{sess_end%60:02d}",
      "session_days": int(len(cnt)), "expected_bars_per_session": expected,
      "complete_session_days": full_days, "incomplete_session_days": part_days,
      "complete_pct": round(100*full_days/max(len(cnt),1), 2),
      "session_bar_count_pctiles": {str(p): float(np.percentile(cnt, p)) for p in [1,5,25,50,100]},
      "years": {str(y): int(v) for y, v in pd.Series(pd.to_datetime(cnt.index).year).value_counts().sort_index().items()},
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"VALIDATION_{name}.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
