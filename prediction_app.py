import streamlit as st
import pandas as pd
import numpy as np
import warnings
import os
import pickle
import hashlib
from datetime import datetime, timedelta
import pytz

warnings.filterwarnings("ignore")

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SIGNAL — Trading Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS (LIGHT MODE) ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;500;600;700;800&display=swap');

:root {
  --bg:#ffffff; --bg2:#f8fafc; --bg3:#f1f5f9; --border:#e2e8f0;
  --accent:#10b981; --accent2:#3b82f6; --accent3:#ef4444; --warn:#f59e0b;
  --text:#111827; --muted:#64748b; --card:#ffffff;
}
*{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Syne',sans-serif;background-color:var(--bg);color:var(--text);}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
.block-container{padding:1.5rem 2rem 2rem;max-width:100%;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}

/* NAV */
.nav-bar{display:flex;align-items:center;justify-content:space-between;padding:0.9rem 0;margin-bottom:1.5rem;border-bottom:1px solid var(--border);}
.nav-logo{font-family:'Space Mono',monospace;font-size:1.4rem;font-weight:700;color:var(--accent);letter-spacing:-0.03em;}
.nav-logo span{color:var(--muted);}
.nav-time{font-family:'Space Mono',monospace;font-size:0.75rem;color:var(--muted);}
.nav-status{display:flex;align-items:center;gap:0.5rem;font-size:0.7rem;color:var(--muted);font-family:'Space Mono',monospace;}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 6px var(--accent);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}

/* TICKER HEADER */
.ticker-header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:1.2rem;flex-wrap:wrap;gap:0.8rem;}
.ticker-name{font-size:2.2rem;font-weight:800;line-height:1;color:var(--text);}
.ticker-sub{font-size:0.8rem;color:var(--muted);font-family:'Space Mono',monospace;margin-top:0.3rem;}
.ticker-price{text-align:right;}
.price-big{font-size:2rem;font-weight:700;font-family:'Space Mono',monospace;color:var(--text);}
.price-chg{font-size:0.85rem;font-family:'Space Mono',monospace;}
.up{color:#10b981 !important;} .dn{color:#ef4444 !important;} .fl{color:#f59e0b !important;}

/* METRIC CARDS */
.metric-row{display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;margin-bottom:1.2rem;}
.metric-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:0.9rem 1rem;position:relative;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.05);}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.metric-card.green::before{background:var(--accent);}
.metric-card.blue::before{background:var(--accent2);}
.metric-card.red::before{background:var(--accent3);}
.metric-card.yellow::before{background:var(--warn);}
.metric-label{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;}
.metric-value{font-size:1.5rem;font-weight:700;font-family:'Space Mono',monospace;color:var(--text);}
.metric-sub{font-size:0.7rem;color:var(--muted);margin-top:0.2rem;}

/* SIGNAL BOX */
.signal-box{border-radius:10px;padding:1.4rem 1.8rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem;border:1px solid;}
.signal-box.buy{background:rgba(16,185,129,0.08);border-color:#10b981;}
.signal-box.sell{background:rgba(239,68,68,0.08);border-color:#ef4444;}
.signal-box.hold{background:rgba(245,158,11,0.08);border-color:#f59e0b;}
.signal-label{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;}
.signal-value{font-size:2.4rem;font-weight:800;letter-spacing:-0.02em;}
.signal-box.buy .signal-value{color:#10b981;}
.signal-box.sell .signal-value{color:#ef4444;}
.signal-box.hold .signal-value{color:#f59e0b;}
.signal-reason{font-size:0.8rem;color:#334155;max-width:50%;}
.signal-conf{text-align:right;font-family:'Space Mono',monospace;}
.conf-pct{font-size:1.6rem;font-weight:700;}
.conf-label{font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em;}

/* INSIGHT BOX */
.insight-box{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:0.85rem;line-height:1.7;color:#334155;}
.insight-title{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;}

/* MODEL GRID */
.model-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:0.8rem;margin-bottom:1.2rem;}
.model-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:0.9rem 1rem;box-shadow:0 1px 3px rgba(0,0,0,0.05);}
.model-card-title{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;}
.model-name{font-size:1rem;font-weight:600;color:#3b82f6;font-family:'Space Mono',monospace;}
.eval-grid{display:flex;gap:1rem;margin-top:0.4rem;flex-wrap:wrap;}
.eval-item{font-size:0.75rem;font-family:'Space Mono',monospace;color:var(--muted);}
.eval-item span{color:var(--text);}

/* FORECAST TABLE */
.forecast-table{width:100%;border-collapse:collapse;font-family:'Space Mono',monospace;font-size:0.78rem;}
.forecast-table th{text-align:left;padding:0.5rem 0.7rem;color:var(--muted);font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;border-bottom:1px solid var(--border);}
.forecast-table td{padding:0.55rem 0.7rem;border-bottom:1px solid rgba(226,232,240,0.6);color:var(--text);}
.forecast-table tr:last-child td{border-bottom:none;}
.forecast-table tr:hover td{background:rgba(15,23,42,0.03);}

/* INDICATOR CARDS */
.ind-row{display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;margin-bottom:1.2rem;}
.ind-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:0.9rem 1rem;box-shadow:0 1px 3px rgba(0,0,0,0.05);}
.ind-name{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;margin-bottom:0.3rem;}
.ind-val{font-size:1.1rem;font-weight:700;font-family:'Space Mono',monospace;color:var(--text);}
.ind-sig{font-size:0.7rem;margin-top:0.2rem;font-family:'Space Mono',monospace;font-weight:600;}

/* WARN BOX */
.warn-box{background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.4);border-radius:8px;padding:0.8rem 1rem;font-size:0.78rem;color:#b45309;margin-bottom:1rem;font-family:'Space Mono',monospace;}
.sec-hdr{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;padding-bottom:0.4rem;border-bottom:1px solid var(--border);margin-bottom:0.8rem;}

/* SIDEBAR */
[data-testid="stSidebar"]{background:var(--bg2) !important;border-right:1px solid var(--border) !important;}
[data-testid="stSidebar"] .block-container{padding:1rem;}
.sidebar-logo{font-family:'Space Mono',monospace;font-size:1.1rem;color:var(--accent);font-weight:700;margin-bottom:1.5rem;padding-bottom:0.8rem;border-bottom:1px solid var(--border);}

/* STREAMLIT OVERRIDES */
.stSelectbox>div>div{background:var(--card) !important;border-color:var(--border) !important;color:var(--text) !important;}
label{color:#334155 !important;font-size:0.78rem !important;font-weight:600 !important;}
.stButton>button{background:var(--card) !important;border:1px solid var(--border) !important;color:#334155 !important;font-family:'Space Mono',monospace !important;font-size:0.75rem !important;border-radius:6px !important;width:100%;margin-top:0.5rem;transition:all 0.2s;}
.stButton>button:hover{border-color:var(--accent) !important;color:var(--accent) !important;}
div[data-testid="stMetric"]{display:none;}
.stSpinner>div{border-top-color:var(--accent) !important;}
.stProgress>div>div>div{background:var(--accent) !important;}
.stTabs [data-baseweb="tab-list"]{gap:0;background:var(--bg3);border-radius:6px;border:1px solid var(--border);padding:3px;}
.stTabs [data-baseweb="tab"]{font-family:'Space Mono',monospace !important;font-size:0.72rem !important;color:var(--muted) !important;background:transparent !important;border:none !important;padding:0.4rem 0.8rem !important;}
.stTabs [aria-selected="true"]{background:var(--bg) !important;color:var(--text) !important;border-radius:4px !important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1rem !important;}
[data-testid="stSelectbox"] div[data-baseweb="select"] span{color:var(--text) !important;}
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
TICKERS = {
    "AAPL":"Apple Inc.","MSFT":"Microsoft Corporation","GOOG":"Alphabet Inc. (Google)",
    "AMZN":"Amazon.com Inc.","NVDA":"NVIDIA Corporation","META":"Meta Platforms Inc.",
    "AVGO":"Broadcom Inc.","TSLA":"Tesla Inc.","AMD":"Advanced Micro Devices",
    "INTC":"Intel Corporation","ORCL":"Oracle Corporation","ADBE":"Adobe Inc.",
    "CSCO":"Cisco Systems Inc.","QCOM":"Qualcomm Inc.","NFLX":"Netflix Inc.",
    "COST":"Costco Wholesale Corp.","PEP":"PepsiCo Inc.","UBER":"Uber Technologies Inc.",
}

HORIZONS = {
    "1 Week":   {"days":7,   "train_months":3,   "forecast_days":3,   "freq":"D"},
    "1 Month":  {"days":30,  "train_months":6,   "forecast_days":10,  "freq":"D"},
    "3 Months": {"days":90,  "train_months":12,  "forecast_days":20,  "freq":"D"},
    "6 Months": {"days":180, "train_months":24,  "forecast_days":30,  "freq":"W"},
    "1 Year":   {"days":365, "train_months":36,  "forecast_days":60,  "freq":"W"},
    "5 Years":  {"days":1825,"train_months":84,  "forecast_days":180, "freq":"M"},
    "10 Years": {"days":3650,"train_months":120, "forecast_days":365, "freq":"M"},
}

METHODS    = ["Auto (Best Model)", "SARIMAX", "Prophet", "Hybrid SARIMAX+Prophet"]
MODEL_DIR  = "/tmp/.model_chance"
os.makedirs(MODEL_DIR, exist_ok=True)
THRESHOLD  = 20.0
ET_TZ      = pytz.timezone("America/New_York")


# ─── Time Helpers ─────────────────────────────────────────────────────────────
def now_et() -> datetime:
    return datetime.now(ET_TZ)

def next_biz_days(n: int, start: datetime | None = None) -> list[datetime]:
    days = []
    d = (start or now_et()).replace(tzinfo=None)
    while len(days) < n:
        d += timedelta(days=1)
        if d.weekday() < 5:
            days.append(d)
    return days

def market_status(now: datetime) -> str:
    if now.weekday() >= 5:
        return "CLOSED · WEEKEND"
    t = now.time()
    import datetime as dt_mod
    pre  = dt_mod.time(4, 0)
    open_= dt_mod.time(9, 30)
    close= dt_mod.time(16, 0)
    ext  = dt_mod.time(20, 0)
    if pre <= t < open_:
        return "PRE-MARKET"
    elif open_ <= t < close:
        return "OPEN"
    elif close <= t < ext:
        return "AFTER-HOURS"
    else:
        return "CLOSED"


# ─── Data & Features ─────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_data(ticker: str, train_months: int) -> pd.DataFrame:
    import yfinance as yf
    end   = datetime.now()
    start = end - timedelta(days=train_months * 31)
    df    = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Open","High","Low","Close","Volume"]].dropna()
    df.index = pd.to_datetime(df.index)
    df = df[df.index.dayofweek < 5]
    return df


@st.cache_data(ttl=60)
def fetch_current_price(ticker: str) -> dict:
    import yfinance as yf
    tk   = yf.Ticker(ticker)
    hist = tk.history(period="5d")
    if hist.empty:
        return {"price":0,"change":0,"pct":0,"volume":0}
    closes = hist["Close"].dropna()
    price  = float(closes.iloc[-1])
    prev   = float(closes.iloc[-2]) if len(closes)>1 else price
    chg    = price - prev
    pct    = (chg/prev*100) if prev else 0
    vol    = float(hist["Volume"].iloc[-1]) if "Volume" in hist else 0
    return {"price":price,"change":chg,"pct":pct,"volume":vol}


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    c = d["Close"]
    for lag in [1,2,3,5,10,20]:
        d[f"lag_{lag}"] = c.shift(lag)
    d["returns_1d"] = c.pct_change(1)
    d["returns_5d"] = c.pct_change(5)
    delta = c.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, np.nan)
    d["RSI"] = 100 - (100/(1+rs))
    ema12 = c.ewm(span=12,adjust=False).mean()
    ema26 = c.ewm(span=26,adjust=False).mean()
    d["MACD"]        = ema12 - ema26
    d["MACD_signal"] = d["MACD"].ewm(span=9,adjust=False).mean()
    d["MACD_hist"]   = d["MACD"] - d["MACD_signal"]
    sma20 = c.rolling(20).mean()
    std20 = c.rolling(20).std()
    d["BB_upper"] = sma20 + 2*std20
    d["BB_lower"] = sma20 - 2*std20
    d["BB_pct"]   = (c - d["BB_lower"]) / (d["BB_upper"] - d["BB_lower"] + 1e-9)
    d["vol_10"]   = d["returns_1d"].rolling(10).std()
    return d.dropna()


# ─── Model Cache ──────────────────────────────────────────────────────────────
def get_model_key(ticker, horizon, method):
    raw = f"{ticker}_{horizon}_{method}_{now_et().strftime('%Y%m%d')}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]

def save_model(key, payload):
    path = os.path.join(MODEL_DIR, f"{key}.model_chance")
    with open(path,"wb") as f: pickle.dump(payload, f)

def load_model(key):
    path = os.path.join(MODEL_DIR, f"{key}.model_chance")
    if os.path.exists(path):
        try:
            with open(path,"rb") as f: return pickle.load(f)
        except: return None
    return None


# ─── Metrics ──────────────────────────────────────────────────────────────────
def eval_metrics(actual, predicted):
    a, p = np.array(actual,dtype=float), np.array(predicted,dtype=float)
    mask = ~(np.isnan(a)|np.isnan(p))
    a, p = a[mask], p[mask]
    if len(a)<2:
        return {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}
    mae     = np.mean(np.abs(a-p))
    rmse    = np.sqrt(np.mean((a-p)**2))
    mape    = np.mean(np.abs((a-p)/(np.abs(a)+1e-9)))*100
    dir_acc = np.mean(np.sign(np.diff(a))==np.sign(np.diff(p)))*100 if len(a)>1 else 0
    return {"MAE":mae,"RMSE":rmse,"MAPE":mape,"DIR":dir_acc}

def passes_threshold(m):
    return m["MAE"]<THRESHOLD and m["RMSE"]<THRESHOLD and m["MAPE"]<THRESHOLD


# ─── Model Trainers (unchanged - safe) ───────────────────────────────────────
def train_sarimax(train_series, forecast_days):
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        from itertools import product as ip
        best_aic, best_order = np.inf, (1,1,1)
        for p,d,q in ip([0,1,2],[0,1],[0,1,2]):
            try:
                r = SARIMAX(train_series,order=(p,d,q),seasonal_order=(1,0,1,5),
                            enforce_stationarity=False,enforce_invertibility=False
                            ).fit(disp=False,maxiter=50)
                if r.aic < best_aic:
                    best_aic=r.aic; best_order=(p,d,q)
            except: continue
        result = SARIMAX(train_series,order=best_order,seasonal_order=(1,1,1,5),
                         enforce_stationarity=False,enforce_invertibility=False
                         ).fit(disp=False,maxiter=100)
        fc  = result.forecast(steps=forecast_days)
        pred = result.get_forecast(steps=forecast_days)
        ci   = pred.conf_int(alpha=0.2)
        ci_lower = ci.iloc[:,0].values
        ci_upper = ci.iloc[:,1].values
        n   = max(5, len(train_series)//5)
        met = eval_metrics(train_series.values[-n:], result.fittedvalues[-n:])
        return np.array(fc), met, ci_lower, ci_upper
    except:
        return np.array([]), {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}, np.array([]), np.array([])

def train_prophet(df, forecast_days):
    try:
        from prophet import Prophet
        dfp = df[["Close"]].reset_index()
        dfp.columns = ["ds","y"]
        dfp["ds"] = pd.to_datetime(dfp["ds"]).dt.tz_localize(None)
        m = Prophet(daily_seasonality=True,weekly_seasonality=True,yearly_seasonality=True,
                    changepoint_prior_scale=0.1,seasonality_prior_scale=10,uncertainty_samples=300)
        m.fit(dfp)
        future = m.make_future_dataframe(periods=forecast_days,freq="B")
        fc_df  = m.predict(future)
        fcast  = fc_df["yhat"].values[-forecast_days:]
        ci_lo  = fc_df["yhat_lower"].values[-forecast_days:]
        ci_hi  = fc_df["yhat_upper"].values[-forecast_days:]
        n      = max(5, len(dfp)//5)
        met    = eval_metrics(dfp["y"].values[-n:], fc_df["yhat"].values[len(dfp)-n:len(dfp)])
        return fcast, met, ci_lo, ci_hi
    except:
        return np.array([]), {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}, np.array([]), np.array([])

def train_hybrid(df, forecast_days):
    try:
        s_fc, s_met, s_lo, s_hi = train_sarimax(df["Close"], forecast_days)
        p_fc, p_met, p_lo, p_hi = train_prophet(df, forecast_days)
        if len(s_fc)==0 or len(p_fc)==0: raise ValueError
        n      = min(len(s_fc),len(p_fc))
        hybrid = 0.55*s_fc[:n] + 0.45*p_fc[:n]
        ci_lo  = 0.55*s_lo[:n] + 0.45*p_lo[:n] if len(s_lo)>=n and len(p_lo)>=n else hybrid*0.97
        ci_hi  = 0.55*s_hi[:n] + 0.45*p_hi[:n] if len(s_hi)>=n and len(p_hi)>=n else hybrid*1.03
        met    = {"MAE":s_met["MAE"]*0.5+p_met["MAE"]*0.5,
                  "RMSE":s_met["RMSE"]*0.5+p_met["RMSE"]*0.5,
                  "MAPE":s_met["MAPE"]*0.5+p_met["MAPE"]*0.5,
                  "DIR":max(s_met["DIR"],p_met["DIR"])}
        return hybrid, met, ci_lo, ci_hi
    except:
        return np.array([]), {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}, np.array([]), np.array([])

def run_models(df, cfg, method):
    fc_days = cfg["forecast_days"]
    results = {}
    if method in ["Auto (Best Model)","SARIMAX"]:
        fc,met,ci_lo,ci_hi = train_sarimax(df["Close"], fc_days)
        results["SARIMAX"] = {"forecast":fc,"metrics":met,"ci_lo":ci_lo,"ci_hi":ci_hi}
    if method in ["Auto (Best Model)","Prophet"]:
        fc,met,ci_lo,ci_hi = train_prophet(df, fc_days)
        results["Prophet"] = {"forecast":fc,"metrics":met,"ci_lo":ci_lo,"ci_hi":ci_hi}
    if method in ["Auto (Best Model)","Hybrid SARIMAX+Prophet"]:
        fc,met,ci_lo,ci_hi = train_hybrid(df, fc_days)
        results["Hybrid"]  = {"forecast":fc,"metrics":met,"ci_lo":ci_lo,"ci_hi":ci_hi}
    for mkey, mfn in [("SARIMAX",lambda:train_sarimax(df["Close"],fc_days)),
                      ("Prophet",lambda:train_prophet(df,fc_days)),
                      ("Hybrid",lambda:train_hybrid(df,fc_days))]:
        if method in [mkey, "Hybrid SARIMAX+Prophet" if mkey=="Hybrid" else "__"] and mkey not in results:
            fc,met,ci_lo,ci_hi = mfn()
            results[mkey] = {"forecast":fc,"metrics":met,"ci_lo":ci_lo,"ci_hi":ci_hi}
    valid = {k:v for k,v in results.items() if len(v.get("forecast",[]))>0 and passes_threshold(v["metrics"])}
    if not valid:
        valid = {k:v for k,v in results.items() if len(v.get("forecast",[]))>0}
    best  = max(valid.keys(), key=lambda k:valid[k]["metrics"]["DIR"]) if valid else list(results.keys())[0]
    if method != "Auto (Best Model)":
        km = {"SARIMAX":"SARIMAX","Prophet":"Prophet","Hybrid SARIMAX+Prophet":"Hybrid"}
        best = km.get(method, best)
    results["_best"] = best
    return results


# ─── Signal & Insight (safe) ──────────────────────────────────────────────────
def generate_signal(forecast, current_price, df, metrics):
    if len(forecast)==0 or current_price==0:
        return {"signal":"HOLD","confidence":0,"reason":"Insufficient data",
                "ret":0,"vol":0,"rsi":50,"macd_hist":0,"bb_pct":0.5}
    avg_fc  = float(np.mean(forecast))
    ret_avg = (avg_fc - current_price)/current_price*100
    returns = df["Close"].pct_change().dropna()
    vol     = float(returns.std()*np.sqrt(252)*100)
    rsi_val = float(df["RSI"].iloc[-1])    if "RSI"       in df.columns else 50
    macd_h  = float(df["MACD_hist"].iloc[-1]) if "MACD_hist" in df.columns else 0
    bb_pct  = float(df["BB_pct"].iloc[-1]) if "BB_pct"    in df.columns else 0.5
    score   = 0; reasons = []
    if   ret_avg > 1.5: score+=2; reasons.append(f"Forecast +{ret_avg:.1f}%")
    elif ret_avg > 0.5: score+=1; reasons.append(f"Forecast +{ret_avg:.1f}%")
    elif ret_avg <-1.5: score-=2; reasons.append(f"Forecast {ret_avg:.1f}%")
    elif ret_avg <-0.5: score-=1; reasons.append(f"Forecast {ret_avg:.1f}%")
    if rsi_val < 30: score+=1; reasons.append("RSI oversold")
    elif rsi_val>70: score-=1; reasons.append("RSI overbought")
    if macd_h>0: score+=1; reasons.append("MACD bullish")
    elif macd_h<0: score-=1; reasons.append("MACD bearish")
    if bb_pct<0.2: score+=1; reasons.append("Near BB lower")
    elif bb_pct>0.8: score-=1; reasons.append("Near BB upper")
    dir_bonus  = (metrics.get("DIR",50)-50)/50
    confidence = min(100, max(20, 50+abs(score)*10+dir_bonus*20))
    if vol>50: reasons.append("⚠ High vol"); confidence=max(20,confidence-15)
    signal = "BUY" if score>=2 else ("SELL" if score<=-2 else "HOLD")
    return {"signal":signal,"confidence":round(confidence),
            "reason":" · ".join(reasons[:3]) if reasons else "Mixed signals",
            "ret":ret_avg,"vol":vol,"rsi":rsi_val,"macd_hist":macd_h,"bb_pct":bb_pct}

def generate_insight(ticker, name, price_data, signal, horizon, model_name):
    direction = "bullish" if signal["signal"]=="BUY" else ("bearish" if signal["signal"]=="SELL" else "neutral")
    vol_desc  = "elevated" if signal.get("vol",0)>40 else ("moderate" if signal.get("vol",0)>20 else "low")
    rsi       = signal.get("rsi",50)
    rsi_desc  = "oversold territory" if rsi<30 else ("overbought territory" if rsi>70 else "neutral range")
    pct_sign  = "+" if price_data["pct"]>=0 else ""
    fc_sign   = "+" if signal["ret"]>=0 else ""
    return (f"{ticker} ({name}) is trading at <strong>${price_data['price']:.2f}</strong>, "
            f"{pct_sign}{price_data['pct']:.2f}% today. "
            f"The <strong>{model_name}</strong> model forecasts an average return of "
            f"<strong>{fc_sign}{signal['ret']:.2f}%</strong> over the selected {horizon} horizon, "
            f"suggesting a <strong>{direction}</strong> outlook. "
            f"Volatility is {vol_desc} at {signal.get('vol',0):.1f}% annualized, "
            f"with RSI in {rsi_desc} ({rsi:.1f}). "
            f"Technical confluence supports a <strong>{signal['signal']}</strong> signal "
            f"with <strong>{signal['confidence']}%</strong> confidence.")


# ─── Helper for Plotly colors ─────────────────────────────────────────────────
def hex_to_rgba(hex_color: str, alpha: float = 0.35) -> str:
    """Convert #RRGGBB or #RGB to rgba string safely."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})"


# ─── Pipeline ─────────────────────────────────────────────────────────────────
def run_pipeline(ticker, horizon, method, force_retrain=False):
    cfg = HORIZONS[horizon]
    key = get_model_key(ticker, horizon, method)
    if not force_retrain:
        cached = load_model(key)
        if cached is not None:
            return cached
    df = fetch_data(ticker, cfg["train_months"])
    if df.empty or len(df)<50:
        return None
    df      = add_features(df)
    results = run_models(df, cfg, method)
    best    = results["_best"]
    best_r  = results.get(best, {})
    payload = {
        "ticker":ticker,"horizon":horizon,"method":method,
        "best_model":best,
        "forecast": best_r.get("forecast", np.array([])),
        "ci_lo":    best_r.get("ci_lo",    np.array([])),
        "ci_hi":    best_r.get("ci_hi",    np.array([])),
        "metrics":  best_r.get("metrics",  {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}),
        "all_results": {k:v for k,v in results.items() if k!="_best"},
        "df":df, "trained_at":now_et().isoformat(),
    }
    save_model(key, payload)
    return payload


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">◈ SIGNAL</div>', unsafe_allow_html=True)
    ticker  = st.selectbox("Choose the stock:",  list(TICKERS.keys()),
                            format_func=lambda x: f"{x} — {TICKERS[x][:22]}")
    horizon = st.selectbox("Time Horizon", list(HORIZONS.keys()), index=1)
    method  = st.selectbox("Forecast Method",    METHODS, index=0)
    st.markdown("---")
    retrain = st.button("⟳  Force Retrain")
    st.markdown("""
    <div style="margin-top:2rem;font-family:'Space Mono',monospace;font-size:0.62rem;color:#64748b;">
    created by SIGNAL<br>Models: SARIMAX · Prophet · Hybrid<br>
    </div>""", unsafe_allow_html=True)


# ─── Nav Bar ──────────────────────────────────────────────────────────────────
now_et_dt   = now_et()
now_str     = now_et_dt.strftime("%a %b %d %Y  ·  %I:%M:%S %p ET")
mkt_status  = market_status(now_et_dt)
mkt_color   = "#10b981" if "OPEN" in mkt_status else ("#f59e0b" if "HOURS" in mkt_status or "PRE" in mkt_status else "#64748b")

st.markdown(f"""
<div class="nav-bar">
  <div class="nav-logo">◈ SIGNAL<span>·ai</span></div>
  <div class="nav-time">{now_str}</div>
  <div class="nav-status">
    <div class="status-dot" style="background:{mkt_color};box-shadow:0 0 6px {mkt_color};"></div>
    {mkt_status}
  </div>
</div>""", unsafe_allow_html=True)


# ─── Run Pipeline ─────────────────────────────────────────────────────────────
with st.spinner(f"Loading {ticker} · {horizon} · {method} ..."):
    price_info = fetch_current_price(ticker)
    result     = run_pipeline(ticker, horizon, method, force_retrain=retrain)

if result is None:
    st.error("Failed to load data. Check your internet connection or try another ticker.")
    st.stop()

best_model  = result["best_model"]
forecast    = result["forecast"]
ci_lo       = result.get("ci_lo", np.array([]))
ci_hi       = result.get("ci_hi", np.array([]))
metrics     = result["metrics"]
all_results = result["all_results"]
df          = result["df"]
cfg         = HORIZONS[horizon]

signal_data  = generate_signal(forecast, price_info["price"], df, metrics)
insight_text = generate_insight(ticker, TICKERS[ticker], price_info, signal_data, horizon, best_model)

# ─── Ticker Header ────────────────────────────────────────────────────────────
pct_color = "up" if price_info["pct"]>=0 else "dn"
arrow     = "▲" if price_info["pct"]>=0 else "▼"
trained   = result.get("trained_at","")[:16].replace("T"," ")

st.markdown(f"""
<div class="ticker-header">
  <div>
    <div class="ticker-name">{ticker}</div>
    <div class="ticker-sub">{TICKERS[ticker].upper()} · {horizon.upper()} · {best_model.upper()}</div>
  </div>
  <div class="ticker-price">
    <div class="price-big">${price_info['price']:,.2f}</div>
    <div class="price-chg {pct_color}">{arrow} ${abs(price_info['change']):.2f} ({abs(price_info['pct']):.2f}%)</div>
    <div style="font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;margin-top:0.2rem;">Trained {trained} ET</div>
  </div>
</div>""", unsafe_allow_html=True)

# ─── Signal Box ───────────────────────────────────────────────────────────────
sig     = signal_data["signal"].lower()
sig_col = "#10b981" if sig=="buy" else ("#ef4444" if sig=="sell" else "#f59e0b")
st.markdown(f"""
<div class="signal-box {sig}">
  <div>
    <div class="signal-label">Trading Signal</div>
    <div class="signal-value">{signal_data['signal']}</div>
  </div>
  <div class="signal-reason">{signal_data['reason']}</div>
  <div class="signal-conf">
    <div class="conf-pct" style="color:{sig_col}">{signal_data['confidence']}%</div>
    <div class="conf-label">Confidence</div>
  </div>
</div>""", unsafe_allow_html=True)

# ─── Metric Cards ─────────────────────────────────────────────────────────────
ret_str = f"{'+'if signal_data['ret']>=0 else ''}{signal_data['ret']:.2f}%"
mae_col = "green" if metrics["MAE"]<20 else "red"
dir_col = "green" if metrics["DIR"]>55 else ("yellow" if metrics["DIR"]>45 else "red")

st.markdown(f"""
<div class="metric-row">
  <div class="metric-card blue">
    <div class="metric-label">Avg Forecast Return</div>
    <div class="metric-value {'up' if signal_data['ret']>=0 else 'dn'}">{ret_str}</div>
    <div class="metric-sub">Over {cfg['forecast_days']} trading days</div>
  </div>
  <div class="metric-card yellow">
    <div class="metric-label">Annualized Volatility</div>
    <div class="metric-value">{signal_data.get('vol',0):.1f}%</div>
    <div class="metric-sub">{'High risk' if signal_data.get('vol',0)>40 else 'Moderate risk' if signal_data.get('vol',0)>20 else 'Low risk'}</div>
  </div>
  <div class="metric-card {mae_col}">
    <div class="metric-label">Model MAE / MAPE</div>
    <div class="metric-value">{metrics['MAE']:.2f}</div>
    <div class="metric-sub">MAPE {metrics['MAPE']:.1f}% · RMSE {metrics['RMSE']:.2f}</div>
  </div>
  <div class="metric-card {dir_col}">
    <div class="metric-label">Directional Accuracy</div>
    <div class="metric-value">{metrics['DIR']:.1f}%</div>
    <div class="metric-sub">{'Strong' if metrics['DIR']>60 else 'Moderate' if metrics['DIR']>50 else 'Weak'} signal</div>
  </div>
</div>""", unsafe_allow_html=True)

if not passes_threshold(metrics):
    st.markdown(f'<div class="warn-box">⚠  MODEL QUALITY ALERT — MAE ({metrics["MAE"]:.1f}) or MAPE ({metrics["MAPE"]:.1f}%) exceeds threshold of {THRESHOLD}. Consider force-retraining or changing the horizon.</div>', unsafe_allow_html=True)

# ─── Insight ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="insight-box">
  <div class="insight-title">Market Insight · Dynamic Analysis</div>
  {insight_text}
</div>""", unsafe_allow_html=True)


# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Forecast Chart", "Forecast Table", "Model Evaluation", "Technical Indicators"])

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — FORECAST CHART (Light + Historical Filter + Fixed Plotly)
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    if len(forecast) > 0:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        # ── Historical period filter (NEW) ───────────────────────────────────
        st.markdown("**Historical Data Period**")
        hist_option = st.radio(
            "Show history for the chart:",
            ["1 Month", "3 Months", "6 Months", "All Available"],
            horizontal=True,
            index=1
        )
        days_map = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "All Available": None}
        max_days = days_map[hist_option]

        if max_days is None:
            hist_df = df.copy()
        else:
            # Safe slice using last N business days
            hist_df = df.tail(max_days * 2).iloc[-max_days:]  # conservative

        hist_dates = hist_df.index.tolist()
        hist_close = hist_df["Close"].tolist()

        fc_dates = next_biz_days(len(forecast))

        fc_arr = np.array(forecast)
        if len(ci_lo) == len(fc_arr) and len(ci_hi) == len(fc_arr):
            ci_lo_arr = np.array(ci_lo)
            ci_hi_arr = np.array(ci_hi)
        else:
            std_fc    = float(df["Close"].std()) * 0.04
            ci_lo_arr = fc_arr - std_fc * (1 + np.arange(len(fc_arr))*0.04)
            ci_hi_arr = fc_arr + std_fc * (1 + np.arange(len(fc_arr))*0.04)

        sig_color = "#10b981" if signal_data["signal"]=="BUY" else \
                    ("#ef4444" if signal_data["signal"]=="SELL" else "#f59e0b")
        ci_fill   = ("rgba(16,185,129,0.12)" if signal_data["signal"]=="BUY" else
                     "rgba(239,68,68,0.10)"  if signal_data["signal"]=="SELL" else
                     "rgba(245,158,11,0.10)")

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.73, 0.27], vertical_spacing=0.04)

        # Historical
        fig.add_trace(go.Scatter(x=hist_dates, y=hist_close, mode="lines", name="Training data",
            line=dict(color="#64748b", width=1.8),
            hovertemplate="<b>%{x|%b %d %Y}</b><br>Close: $%{y:.2f}<extra></extra>"), row=1, col=1)

        # Junction
        junction_x = [hist_dates[-1], fc_dates[0]]
        junction_y = [hist_close[-1], float(fc_arr[0])]
        fig.add_trace(go.Scatter(x=junction_x, y=junction_y, mode="lines",
            line=dict(color=sig_color, width=1.5, dash="dot"), showlegend=False, hoverinfo="skip"), row=1, col=1)

        # Forecast line
        # === SHADOW LINE (add this BEFORE your main forecast line) ===
        fig.add_trace(go.Scatter(
            x=fc_dates,
            y=fc_arr,
            mode="lines",
            line=dict(
                color="rgba(220, 200, 170, 0.25)",  # light orange-grey shadow
                width=8  # besar = efek shadow (≈ “size 25 feel”)
            ),
            hoverinfo="skip",
            showlegend=False
        ), row=1, col=1)
        
        
        # === MAIN FORECAST LINE (your original, unchanged structure) ===
        fig.add_trace(go.Scatter(
            x=fc_dates,
            y=fc_arr,
            mode="lines+markers",
            name=f"Forecast · {best_model}",
            line=dict(color=sig_color, width=2.5),
            marker=dict(size=5, color=sig_color, line=dict(color="#ffffff", width=1.5)),
            hovertemplate="<b>%{x|%b %d %Y}</b><br>Forecast: $%{y:.2f}<extra></extra>"
        ), row=1, col=1)

        # Current price line
        fig.add_hline(y=price_info["price"], line_dash="dot",
            line_color="rgba(15,23,42,0.25)", line_width=1,
            row=1, col=1, annotation_text=f"  Now ${price_info['price']:.2f}",
            annotation_font=dict(size=9, color="#64748b"), annotation_position="right")

        # Volume
        if "Volume" in hist_df.columns:
            v_colors = [
                "#10b981" if c >= o else "#ef4444"
                for c, o in zip(hist_df["Close"], hist_df["Open"])
            ]
        
            fig.add_trace(
                go.Bar(
                    x=hist_dates,
                    y=hist_df["Volume"].tolist(),
                    name="Volume",
                    marker=dict(color=v_colors),  # stronger per-bar control
                    opacity=0.85,  # keep higher for clearer split visibility
                    hovertemplate="<b>%{x|%b %d}</b><br>Vol: %{y:,.0f}<extra></extra>"
                ),
                row=2,
                col=1
            )

        fig.update_layout(
            height=520,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#f8fafc",
            font=dict(family="Space Mono", color="#64748b", size=10),
            legend=dict(bgcolor="#f8fafc", bordercolor="#e2e8f0", borderwidth=1,
                        font=dict(size=9, color="#334155"), x=0.01, y=0.99, orientation="h"),
            margin=dict(l=4, r=4, t=12, b=4),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#f1f5f9", bordercolor="#e2e8f0",
                            font=dict(family="Space Mono", size=10, color="#111827")),
        )
        fig.update_xaxes(gridcolor="rgba(226,232,240,0.6)", zeroline=False,
                         tickfont=dict(size=9, color="#64748b"),
                         rangebreaks=[dict(bounds=["sat","mon"])])
        fig.update_yaxes(gridcolor="rgba(226,232,240,0.6)", zeroline=False, tickprefix="$")

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown(f"""
        <div style="display:flex;gap:1.5rem;font-family:'Space Mono',monospace;font-size:0.68rem;color:#64748b;margin-top:0.3rem;flex-wrap:wrap;">
          <span>── <span style="color:#64748b">Training data (historical)</span></span>
          <span>── <span style="color:{sig_color}">Forecast · {best_model}</span></span>
          <span>▒ <span style="color:{sig_color}">80% Confidence Interval</span></span>
        </div>""", unsafe_allow_html=True)
    else:
        st.warning("No forecast data available.")

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — FORECAST TABLE
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-hdr">Forecast Output Table</div>', unsafe_allow_html=True)
    if len(forecast)>0:
        biz_dates = next_biz_days(len(forecast))
        rows_html = ""
        for dt, fc_v, lo_v, hi_v in zip(
            biz_dates, forecast,
            ci_lo if len(ci_lo)==len(forecast) else [None]*len(forecast),
            ci_hi if len(ci_hi)==len(forecast) else [None]*len(forecast),
        ):
            chg  = (fc_v - price_info["price"])/price_info["price"]*100 if price_info["price"] else 0
            cc   = "up" if chg>=0 else "dn"
            sign = "+" if chg>=0 else ""
            ci_str = f"${lo_v:.2f} – ${hi_v:.2f}" if lo_v is not None else "—"
            rows_html += f"""<tr>
              <td style="color:#64748b">{dt.strftime("%a, %b %d %Y")}</td>
              <td style="color:#111827;font-weight:600">${fc_v:.2f}</td>
              <td class="{cc}">{sign}{chg:.2f}%</td>
              <td style="color:#64748b;font-size:0.72rem">{ci_str}</td>
            </tr>"""
        st.markdown(f"""<table class="forecast-table">
        <thead><tr>
          <th>Date</th><th>Forecast Price</th><th>Expected Change</th><th>CI Range (80%)</th>
        </tr></thead>
        <tbody>{rows_html}</tbody></table>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — MODEL EVALUATION
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-hdr">Model Performance Comparison</div>', unsafe_allow_html=True)
    best_met = all_results.get(best_model,{}).get("metrics",metrics)
    ok_col   = "#10b981" if passes_threshold(best_met) else "#ef4444"
    st.markdown(f"""
    <div class="model-grid">
      <div class="model-card">
        <div class="model-card-title">Selected Model</div>
        <div class="model-name">{best_model}</div>
        <div class="eval-grid">
          <div class="eval-item">MAE <span>{best_met['MAE']:.3f}</span></div>
          <div class="eval-item">RMSE <span>{best_met['RMSE']:.3f}</span></div>
          <div class="eval-item">MAPE <span>{best_met['MAPE']:.2f}%</span></div>
          <div class="eval-item">DIR <span style="color:{ok_col}">{best_met['DIR']:.1f}%</span></div>
        </div>
      </div>
      <div class="model-card">
        <div class="model-card-title">Threshold Check</div>
        <div class="model-name" style="color:{'#10b981' if passes_threshold(best_met) else '#ef4444'}">
          {'✓ PASS' if passes_threshold(best_met) else '✗ FAIL'}
        </div>
        <div style="font-size:0.72rem;color:#64748b;margin-top:0.4rem;font-family:'Space Mono',monospace;">
          Limit: MAE / RMSE / MAPE &lt; {THRESHOLD}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr" style="margin-top:1rem;">All Models</div>', unsafe_allow_html=True)
    rows_h = ""
    for mname, res in all_results.items():
        if not res: continue
        m  = res.get("metrics",{})
        ok = passes_threshold(m)
        ib = mname==best_model
        rows_h += f"""<tr style="{'background:rgba(16,185,129,0.05);' if ib else ''}">
          <td style="color:{'#10b981'if ib else '#111827'}">{'★ ' if ib else ''}{mname}</td>
          <td style="color:#334155">{m.get('MAE',999):.3f}</td>
          <td style="color:#334155">{m.get('RMSE',999):.3f}</td>
          <td style="color:#334155">{m.get('MAPE',999):.2f}%</td>
          <td style="color:{'#10b981'if m.get('DIR',0)>55 else '#ef4444'}">{m.get('DIR',0):.1f}%</td>
          <td style="color:{'#10b981'if ok else '#ef4444'}">{'✓'if ok else '✗'}</td>
        </tr>"""
    st.markdown(f"""<table class="forecast-table">
    <thead><tr>
      <th>Model</th><th>MAE</th><th>RMSE</th><th>MAPE</th><th>DIR</th><th>Pass</th>
    </tr></thead><tbody>{rows_h}</tbody></table>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="margin-top:1rem;">
      <div class="insight-title">Evaluation Methodology</div>
      <b style="color:#111827">MAE</b> (Mean Absolute Error) — average price prediction error in dollars.<br>
      <b style="color:#111827">RMSE</b> penalises large errors more heavily.<br>
      <b style="color:#111827">MAPE</b> expresses error as a percentage of price.<br>
      <b style="color:#111827">DIR</b> (Directional Accuracy) measures how often the model correctly predicts price direction — primary selection criterion.
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — TECHNICAL INDICATORS (Light mode)
# ──────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-hdr">Technical Indicators</div>', unsafe_allow_html=True)
    rsi_v  = signal_data.get("rsi",  50)
    macd_v = signal_data.get("macd_hist", 0)
    bb_v   = signal_data.get("bb_pct",  0.5)

    rsi_sig = "OVERSOLD ▲"   if rsi_v<30  else ("OVERBOUGHT ▼" if rsi_v>70  else "NEUTRAL")
    rsi_c   = "#10b981"       if rsi_v<30  else ("#ef4444"      if rsi_v>70  else "#f59e0b")
    mac_sig = "BULLISH ▲"    if macd_v>0  else "BEARISH ▼"
    mac_c   = "#10b981"       if macd_v>0  else "#ef4444"
    bb_sig  = "OVERSOLD ▲"   if bb_v<0.2  else ("OVERBOUGHT ▼" if bb_v>0.8  else "NEUTRAL")
    bb_c    = "#10b981"       if bb_v<0.2  else ("#ef4444"      if bb_v>0.8  else "#f59e0b")

    st.markdown(f"""
    <div class="ind-row">
      <div class="ind-card">
        <div class="ind-name">RSI (14)</div>
        <div class="ind-val">{rsi_v:.1f}</div>
        <div class="ind-sig" style="color:{rsi_c}">{rsi_sig}</div>
        <div style="font-size:0.65rem;color:#64748b;margin-top:0.4rem;">Oversold &lt;30 · Overbought &gt;70</div>
      </div>
      <div class="ind-card">
        <div class="ind-name">MACD Histogram</div>
        <div class="ind-val">{'+'if macd_v>=0 else ''}{macd_v:.3f}</div>
        <div class="ind-sig" style="color:{mac_c}">{mac_sig}</div>
        <div style="font-size:0.65rem;color:#64748b;margin-top:0.4rem;">EMA(12) − EMA(26) − Signal(9)</div>
      </div>
      <div class="ind-card">
        <div class="ind-name">Bollinger %B</div>
        <div class="ind-val">{bb_v:.2f}</div>
        <div class="ind-sig" style="color:{bb_c}">{bb_sig}</div>
        <div style="font-size:0.65rem;color:#64748b;margin-top:0.4rem;">0 = Lower Band · 1 = Upper Band</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if len(df) > 0:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        fig2 = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.42, 0.28, 0.30],
                             vertical_spacing=0.04, subplot_titles=["Price + Bollinger Bands", "RSI (14)", "MACD"])
        tail = df.tail(120)

        fig2.add_trace(go.Scatter(x=tail.index, y=tail["Close"], name="Price",
            line=dict(color="#334155", width=1.8)), row=1, col=1)
        fig2.add_trace(go.Scatter(x=tail.index, y=tail["BB_upper"], name="BB Upper",
            line=dict(color="#3b82f6", width=1, dash="dot")), row=1, col=1)
        fig2.add_trace(go.Scatter(x=tail.index, y=tail["BB_lower"], name="BB Lower",
            line=dict(color="#3b82f6", width=1, dash="dot"), fill="tonexty", fillcolor="rgba(59,130,246,0.06)"), row=1, col=1)

        fig2.add_trace(go.Scatter(x=tail.index, y=tail["RSI"], name="RSI",
            line=dict(color="#f59e0b", width=1.6)), row=2, col=1)
        fig2.add_hline(y=70, line_dash="dot", line_color="#ef4444", row=2, col=1)
        fig2.add_hline(y=30, line_dash="dot", line_color="#10b981", row=2, col=1)

        colors_m = ["#10b981" if v>=0 else "#ef4444" for v in tail["MACD_hist"]]
        fig2.add_trace(go.Bar(x=tail.index, y=tail["MACD_hist"], name="Histogram", marker_color=colors_m, opacity=0.75), row=3, col=1)
        fig2.add_trace(go.Scatter(x=tail.index, y=tail["MACD"], name="MACD", line=dict(color="#3b82f6", width=1.4)), row=3, col=1)
        fig2.add_trace(go.Scatter(x=tail.index, y=tail["MACD_signal"], name="Signal", line=dict(color="#ec4899", width=1.4)), row=3, col=1)

        fig2.update_layout(
            height=520,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#f8fafc",
            font=dict(family="Space Mono", color="#64748b", size=9),
            showlegend=False,
            margin=dict(l=4, r=4, t=25, b=4),
            hoverlabel=dict(bgcolor="#f1f5f9", bordercolor="#e2e8f0", font=dict(family="Space Mono", size=10, color="#111827")),
        )
        fig2.update_xaxes(gridcolor="rgba(226,232,240,0.6)", zeroline=False, rangebreaks=[dict(bounds=["sat","mon"])])
        fig2.update_yaxes(gridcolor="rgba(226,232,240,0.6)", zeroline=False)
        for ann in fig2.layout.annotations:
            ann.font = dict(size=9, color="#64748b", family="Space Mono")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
