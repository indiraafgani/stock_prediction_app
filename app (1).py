import streamlit as st
import pandas as pd
import numpy as np
import warnings
import os
import pickle
import hashlib
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SIGNAL — Trading Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;500;600;700;800&display=swap');

:root {
  --bg:#070a0f; --bg2:#0d1117; --bg3:#161b22; --border:#21262d;
  --accent:#00ff88; --accent2:#0088ff; --accent3:#ff4466; --warn:#ffaa00;
  --text:#e6edf3; --muted:#6e7681; --card:#0d1117;
}
*{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Syne',sans-serif;background-color:var(--bg);color:var(--text);}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
.block-container{padding:1.5rem 2rem 2rem;max-width:100%;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}

.nav-bar{display:flex;align-items:center;justify-content:space-between;padding:0.9rem 0;margin-bottom:1.5rem;border-bottom:1px solid var(--border);}
.nav-logo{font-family:'Space Mono',monospace;font-size:1.4rem;font-weight:700;color:var(--accent);letter-spacing:-0.03em;}
.nav-logo span{color:var(--muted);}
.nav-time{font-family:'Space Mono',monospace;font-size:0.75rem;color:var(--muted);}
.nav-status{display:flex;align-items:center;gap:0.5rem;font-size:0.7rem;color:var(--muted);font-family:'Space Mono',monospace;}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 6px var(--accent);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}

.ticker-header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:1.2rem;flex-wrap:wrap;gap:0.8rem;}
.ticker-name{font-size:2.2rem;font-weight:800;line-height:1;}
.ticker-sub{font-size:0.8rem;color:var(--muted);font-family:'Space Mono',monospace;margin-top:0.3rem;}
.ticker-price{text-align:right;}
.price-big{font-size:2rem;font-weight:700;font-family:'Space Mono',monospace;}
.price-chg{font-size:0.85rem;font-family:'Space Mono',monospace;}
.up{color:var(--accent);}.dn{color:var(--accent3);}.fl{color:var(--warn);}

.metric-row{display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;margin-bottom:1.2rem;}
.metric-card{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:0.9rem 1rem;position:relative;overflow:hidden;}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.metric-card.green::before{background:var(--accent);}
.metric-card.blue::before{background:var(--accent2);}
.metric-card.red::before{background:var(--accent3);}
.metric-card.yellow::before{background:var(--warn);}
.metric-label{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;}
.metric-value{font-size:1.5rem;font-weight:700;font-family:'Space Mono',monospace;}
.metric-sub{font-size:0.7rem;color:var(--muted);margin-top:0.2rem;}

.signal-box{border-radius:10px;padding:1.4rem 1.8rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem;border:1px solid;}
.signal-box.buy{background:rgba(0,255,136,0.07);border-color:var(--accent);}
.signal-box.sell{background:rgba(255,68,102,0.07);border-color:var(--accent3);}
.signal-box.hold{background:rgba(255,170,0,0.07);border-color:var(--warn);}
.signal-label{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;}
.signal-value{font-size:2.4rem;font-weight:800;letter-spacing:-0.02em;}
.signal-box.buy .signal-value{color:var(--accent);}
.signal-box.sell .signal-value{color:var(--accent3);}
.signal-box.hold .signal-value{color:var(--warn);}
.signal-reason{font-size:0.8rem;color:var(--muted);max-width:50%;}
.signal-conf{text-align:right;font-family:'Space Mono',monospace;}
.conf-pct{font-size:1.6rem;font-weight:700;}
.conf-label{font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em;}

.insight-box{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:0.85rem;line-height:1.6;color:#b1bac4;}
.insight-title{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;}

.model-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:0.8rem;margin-bottom:1.2rem;}
.model-card{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:0.9rem 1rem;}
.model-card-title{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;}
.model-name{font-size:1rem;font-weight:600;color:var(--accent2);font-family:'Space Mono',monospace;}
.eval-grid{display:flex;gap:1rem;margin-top:0.4rem;flex-wrap:wrap;}
.eval-item{font-size:0.75rem;font-family:'Space Mono',monospace;color:var(--muted);}
.eval-item span{color:var(--text);}

.forecast-table{width:100%;border-collapse:collapse;font-family:'Space Mono',monospace;font-size:0.78rem;}
.forecast-table th{text-align:left;padding:0.5rem 0.7rem;color:var(--muted);font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;border-bottom:1px solid var(--border);}
.forecast-table td{padding:0.55rem 0.7rem;border-bottom:1px solid rgba(33,38,45,0.5);}
.forecast-table tr:last-child td{border-bottom:none;}
.forecast-table tr:hover td{background:rgba(255,255,255,0.02);}

.ind-row{display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;margin-bottom:1.2rem;}
.ind-card{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:0.9rem 1rem;}
.ind-name{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;margin-bottom:0.3rem;}
.ind-val{font-size:1.1rem;font-weight:700;font-family:'Space Mono',monospace;}
.ind-sig{font-size:0.7rem;margin-top:0.2rem;font-family:'Space Mono',monospace;}

.warn-box{background:rgba(255,170,0,0.06);border:1px solid rgba(255,170,0,0.3);border-radius:8px;padding:0.8rem 1rem;font-size:0.78rem;color:#ffaa00;margin-bottom:1rem;font-family:'Space Mono',monospace;}
.sec-hdr{font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;padding-bottom:0.4rem;border-bottom:1px solid var(--border);margin-bottom:0.8rem;}

[data-testid="stSidebar"]{background:var(--bg2) !important;border-right:1px solid var(--border) !important;}
[data-testid="stSidebar"] .block-container{padding:1rem;}
.sidebar-logo{font-family:'Space Mono',monospace;font-size:1.1rem;color:var(--accent);font-weight:700;margin-bottom:1.5rem;padding-bottom:0.8rem;border-bottom:1px solid var(--border);}

.stSelectbox>div>div{background:var(--bg3) !important;border-color:var(--border) !important;color:var(--text) !important;}
label{color:var(--muted) !important;font-size:0.75rem !important;}
.stButton>button{background:var(--bg3) !important;border:1px solid var(--border) !important;color:var(--text) !important;font-family:'Space Mono',monospace !important;font-size:0.75rem !important;border-radius:6px !important;width:100%;margin-top:0.5rem;transition:border-color 0.2s;}
.stButton>button:hover{border-color:var(--accent) !important;color:var(--accent) !important;}
div[data-testid="stMetric"]{display:none;}
.stSpinner>div{border-top-color:var(--accent) !important;}
.stProgress>div>div>div{background:var(--accent) !important;}

.stTabs [data-baseweb="tab-list"]{gap:0;background:var(--bg3);border-radius:6px;border:1px solid var(--border);padding:3px;}
.stTabs [data-baseweb="tab"]{font-family:'Space Mono',monospace !important;font-size:0.72rem !important;color:var(--muted) !important;background:transparent !important;border:none !important;padding:0.4rem 0.8rem !important;}
.stTabs [aria-selected="true"]{background:var(--bg) !important;color:var(--text) !important;border-radius:4px !important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1rem !important;}
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

METHODS = ["Auto (Best Model)", "SARIMAX", "Prophet", "Hybrid SARIMAX+Prophet"]
MODEL_DIR = "/tmp/.model_chance"
os.makedirs(MODEL_DIR, exist_ok=True)
THRESHOLD = 20.0


# ─── Data & Features ─────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_data(ticker: str, train_months: int) -> pd.DataFrame:
    import yfinance as yf
    end = datetime.now()
    start = end - timedelta(days=train_months * 31)
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Open","High","Low","Close","Volume"]].dropna()
    df.index = pd.to_datetime(df.index)
    return df


@st.cache_data(ttl=60)
def fetch_current_price(ticker: str) -> dict:
    import yfinance as yf
    tk = yf.Ticker(ticker)
    hist = tk.history(period="5d")
    if hist.empty:
        return {"price":0,"change":0,"pct":0,"volume":0}
    closes = hist["Close"].dropna()
    price = float(closes.iloc[-1])
    prev  = float(closes.iloc[-2]) if len(closes)>1 else price
    chg   = price - prev
    pct   = (chg/prev*100) if prev else 0
    vol   = float(hist["Volume"].iloc[-1]) if "Volume" in hist else 0
    return {"price":price,"change":chg,"pct":pct,"volume":vol}


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    c = d["Close"]
    for lag in [1,2,3,5,10,20]:
        d[f"lag_{lag}"] = c.shift(lag)
    d["returns_1d"] = c.pct_change(1)
    d["returns_5d"] = c.pct_change(5)
    # RSI
    delta = c.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    d["RSI"] = 100 - (100/(1+rs))
    # MACD
    ema12 = c.ewm(span=12,adjust=False).mean()
    ema26 = c.ewm(span=26,adjust=False).mean()
    d["MACD"] = ema12 - ema26
    d["MACD_signal"] = d["MACD"].ewm(span=9,adjust=False).mean()
    d["MACD_hist"] = d["MACD"] - d["MACD_signal"]
    # Bollinger Bands
    sma20 = c.rolling(20).mean()
    std20 = c.rolling(20).std()
    d["BB_upper"] = sma20 + 2*std20
    d["BB_lower"] = sma20 - 2*std20
    d["BB_pct"] = (c - d["BB_lower"]) / (d["BB_upper"] - d["BB_lower"] + 1e-9)
    d["vol_10"] = d["returns_1d"].rolling(10).std()
    return d.dropna()


# ─── Model Cache ──────────────────────────────────────────────────────────────
def get_model_key(ticker, horizon, method):
    raw = f"{ticker}_{horizon}_{method}_{datetime.now().strftime('%Y%m%d')}"
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


# ─── Metrics & Threshold ──────────────────────────────────────────────────────
def eval_metrics(actual, predicted):
    a, p = np.array(actual, dtype=float), np.array(predicted, dtype=float)
    mask = ~(np.isnan(a)|np.isnan(p))
    a, p = a[mask], p[mask]
    if len(a)<2:
        return {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}
    mae  = np.mean(np.abs(a-p))
    rmse = np.sqrt(np.mean((a-p)**2))
    mape = np.mean(np.abs((a-p)/(np.abs(a)+1e-9)))*100
    dir_acc = np.mean(np.sign(np.diff(a))==np.sign(np.diff(p)))*100 if len(a)>1 else 0
    return {"MAE":mae,"RMSE":rmse,"MAPE":mape,"DIR":dir_acc}

def passes_threshold(m):
    return m["MAE"]<THRESHOLD and m["RMSE"]<THRESHOLD and m["MAPE"]<THRESHOLD


# ─── Model Trainers ───────────────────────────────────────────────────────────
def train_sarimax(train_series, forecast_days):
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        from itertools import product as ip
        best_aic, best_order = np.inf, (1,1,1)
        for p,d,q in ip([0,1,2],[0,1],[0,1,2]):
            try:
                r = SARIMAX(train_series, order=(p,d,q),
                            seasonal_order=(1,0,1,5),
                            enforce_stationarity=False,
                            enforce_invertibility=False).fit(disp=False, maxiter=50)
                if r.aic < best_aic:
                    best_aic=r.aic; best_order=(p,d,q)
            except: continue
        result = SARIMAX(train_series, order=best_order,
                         seasonal_order=(1,1,1,5),
                         enforce_stationarity=False,
                         enforce_invertibility=False).fit(disp=False, maxiter=100)
        fc = result.forecast(steps=forecast_days)
        n  = max(5, len(train_series)//5)
        met = eval_metrics(train_series.values[-n:], result.fittedvalues[-n:])
        return np.array(fc), met
    except Exception as e:
        return np.array([]), {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}

def train_prophet(df, forecast_days):
    try:
        from prophet import Prophet
        dfp = df[["Close"]].reset_index()
        dfp.columns = ["ds","y"]
        dfp["ds"] = pd.to_datetime(dfp["ds"]).dt.tz_localize(None)
        m = Prophet(daily_seasonality=True, weekly_seasonality=True,
                    yearly_seasonality=True, changepoint_prior_scale=0.1,
                    seasonality_prior_scale=10, uncertainty_samples=200)
        m.fit(dfp)
        future = m.make_future_dataframe(periods=forecast_days, freq="B")
        fc_df  = m.predict(future)
        fcast  = fc_df["yhat"].values[-forecast_days:]
        n = max(5, len(dfp)//5)
        met = eval_metrics(dfp["y"].values[-n:], fc_df["yhat"].values[len(dfp)-n:len(dfp)])
        return fcast, met
    except Exception as e:
        return np.array([]), {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}

def train_hybrid(df, forecast_days):
    try:
        s_fc, s_met = train_sarimax(df["Close"], forecast_days)
        p_fc, p_met = train_prophet(df, forecast_days)
        if len(s_fc)==0 or len(p_fc)==0: raise ValueError("component failed")
        n = min(len(s_fc), len(p_fc))
        hybrid = 0.55*s_fc[:n] + 0.45*p_fc[:n]
        met = {"MAE":s_met["MAE"]*0.5+p_met["MAE"]*0.5,
               "RMSE":s_met["RMSE"]*0.5+p_met["RMSE"]*0.5,
               "MAPE":s_met["MAPE"]*0.5+p_met["MAPE"]*0.5,
               "DIR":max(s_met["DIR"],p_met["DIR"])}
        return hybrid, met
    except:
        return np.array([]), {"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}


def run_models(df, cfg, method):
    fc_days = cfg["forecast_days"]
    results = {}
    if method in ["Auto (Best Model)", "SARIMAX"]:
        fc,met = train_sarimax(df["Close"], fc_days)
        results["SARIMAX"] = {"forecast":fc,"metrics":met}
    if method in ["Auto (Best Model)", "Prophet"]:
        fc,met = train_prophet(df, fc_days)
        results["Prophet"] = {"forecast":fc,"metrics":met}
    if method in ["Auto (Best Model)", "Hybrid SARIMAX+Prophet"]:
        fc,met = train_hybrid(df, fc_days)
        results["Hybrid"] = {"forecast":fc,"metrics":met}
    # Fallback single-method
    if method=="SARIMAX" and "SARIMAX" not in results:
        fc,met = train_sarimax(df["Close"], fc_days)
        results["SARIMAX"] = {"forecast":fc,"metrics":met}
    elif method=="Prophet" and "Prophet" not in results:
        fc,met = train_prophet(df, fc_days)
        results["Prophet"] = {"forecast":fc,"metrics":met}
    elif method=="Hybrid SARIMAX+Prophet" and "Hybrid" not in results:
        fc,met = train_hybrid(df, fc_days)
        results["Hybrid"] = {"forecast":fc,"metrics":met}
    # Best selection
    valid = {k:v for k,v in results.items() if len(v.get("forecast",[]))>0 and passes_threshold(v["metrics"])}
    if not valid:
        valid = {k:v for k,v in results.items() if len(v.get("forecast",[]))>0}
    best = max(valid.keys(), key=lambda k:valid[k]["metrics"]["DIR"]) if valid else list(results.keys())[0]
    if method != "Auto (Best Model)":
        key_map = {"SARIMAX":"SARIMAX","Prophet":"Prophet","Hybrid SARIMAX+Prophet":"Hybrid"}
        best = key_map.get(method, best)
    results["_best"] = best
    return results


# ─── Signal & Insight ─────────────────────────────────────────────────────────
def generate_signal(forecast, current_price, df, metrics):
    if len(forecast)==0 or current_price==0:
        return {"signal":"HOLD","confidence":0,"reason":"Insufficient data","ret":0,"vol":0,"rsi":50,"macd_hist":0,"bb_pct":0.5}
    avg_fc   = float(np.mean(forecast))
    ret_avg  = (avg_fc - current_price)/current_price*100
    returns  = df["Close"].pct_change().dropna()
    vol      = float(returns.std()*np.sqrt(252)*100)
    rsi_val  = float(df["RSI"].iloc[-1]) if "RSI" in df.columns else 50
    macd_h   = float(df["MACD_hist"].iloc[-1]) if "MACD_hist" in df.columns else 0
    bb_pct   = float(df["BB_pct"].iloc[-1]) if "BB_pct" in df.columns else 0.5
    score    = 0; reasons = []
    if ret_avg>1.5: score+=2; reasons.append(f"Forecast +{ret_avg:.1f}%")
    elif ret_avg>0.5: score+=1; reasons.append(f"Forecast +{ret_avg:.1f}%")
    elif ret_avg<-1.5: score-=2; reasons.append(f"Forecast {ret_avg:.1f}%")
    elif ret_avg<-0.5: score-=1; reasons.append(f"Forecast {ret_avg:.1f}%")
    if rsi_val<30: score+=1; reasons.append("RSI oversold")
    elif rsi_val>70: score-=1; reasons.append("RSI overbought")
    if macd_h>0: score+=1; reasons.append("MACD bullish")
    elif macd_h<0: score-=1; reasons.append("MACD bearish")
    if bb_pct<0.2: score+=1; reasons.append("Near BB lower")
    elif bb_pct>0.8: score-=1; reasons.append("Near BB upper")
    dir_bonus = (metrics.get("DIR",50)-50)/50
    confidence = min(100, max(20, 50+abs(score)*10+dir_bonus*20))
    if vol>50: reasons.append("⚠ High volatility"); confidence=max(20,confidence-15)
    signal = "BUY" if score>=2 else ("SELL" if score<=-2 else "HOLD")
    return {"signal":signal,"confidence":round(confidence),"reason":" · ".join(reasons[:3]) if reasons else "Mixed signals",
            "ret":ret_avg,"vol":vol,"rsi":rsi_val,"macd_hist":macd_h,"bb_pct":bb_pct}

def generate_insight(ticker, name, price_data, signal, horizon, model_name):
    direction = "bullish" if signal["signal"]=="BUY" else ("bearish" if signal["signal"]=="SELL" else "neutral")
    vol_desc  = "elevated" if signal.get("vol",0)>40 else ("moderate" if signal.get("vol",0)>20 else "low")
    rsi       = signal.get("rsi",50)
    rsi_desc  = "oversold territory" if rsi<30 else ("overbought territory" if rsi>70 else "neutral range")
    pct_sign  = "+" if price_data["pct"]>=0 else ""
    fc_sign   = "+" if signal["ret"]>=0 else ""
    return (f"{ticker} ({name}) is currently trading at ${price_data['price']:.2f}, "
            f"{pct_sign}{price_data['pct']:.2f}% today. "
            f"The {model_name} model forecasts an average return of {fc_sign}{signal['ret']:.2f}% "
            f"over the selected {horizon} horizon, suggesting a {direction} outlook. "
            f"Volatility is {vol_desc} at {signal.get('vol',0):.1f}% annualized, "
            f"with RSI in {rsi_desc} ({rsi:.1f}). "
            f"Technical confluence supports a {signal['signal']} signal with {signal['confidence']}% confidence.")


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
    df = add_features(df)
    results = run_models(df, cfg, method)
    best    = results["_best"]
    best_r  = results.get(best, {})
    payload = {"ticker":ticker,"horizon":horizon,"method":method,
               "best_model":best,"forecast":best_r.get("forecast",np.array([])),
               "metrics":best_r.get("metrics",{"MAE":999,"RMSE":999,"MAPE":999,"DIR":0}),
               "all_results":{k:v for k,v in results.items() if k!="_best"},
               "df":df,"trained_at":datetime.now().isoformat()}
    save_model(key, payload)
    return payload


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">◈ SIGNAL</div>', unsafe_allow_html=True)
    ticker  = st.selectbox("TICKER", list(TICKERS.keys()),
                            format_func=lambda x: f"{x} — {TICKERS[x][:22]}")
    horizon = st.selectbox("TIME HORIZON", list(HORIZONS.keys()), index=1)
    method  = st.selectbox("FORECAST METHOD", METHODS, index=0)
    st.markdown("---")
    extend    = st.checkbox("Extend Prediction Range", value=False)
    extra_pct = st.slider("Extrapolation %", 10, 100, 30, 10) if extend else 0
    st.markdown("---")
    retrain = st.button("⟳  Force Retrain")
    st.markdown("""
    <div style="margin-top:2rem;font-family:'Space Mono',monospace;font-size:0.62rem;color:#4a5568;">
    SIGNAL v1.0<br>Models: SARIMAX · Prophet · Hybrid<br>
    Indicators: RSI · MACD · Bollinger<br>Cache: .model_chance<br>Threshold: &lt;20
    </div>""", unsafe_allow_html=True)


# ─── Nav Bar ──────────────────────────────────────────────────────────────────
now_str = datetime.now().strftime("%A, %B %d %Y  ·  %H:%M:%S")
st.markdown(f"""
<div class="nav-bar">
  <div class="nav-logo">◈ SIGNAL<span>·ai</span></div>
  <div class="nav-time">{now_str}</div>
  <div class="nav-status"><div class="status-dot"></div>LIVE DATA · YF ENGINE</div>
</div>""", unsafe_allow_html=True)


# ─── Run Pipeline ─────────────────────────────────────────────────────────────
with st.spinner(f"Loading {ticker} · {horizon} · {method} ..."):
    price_info = fetch_current_price(ticker)
    result     = run_pipeline(ticker, horizon, method, force_retrain=retrain)

if result is None:
    st.error("Failed to load data. Check internet connection or try another ticker.")
    st.stop()

best_model  = result["best_model"]
forecast    = result["forecast"]
metrics     = result["metrics"]
all_results = result["all_results"]
df          = result["df"]
cfg         = HORIZONS[horizon]

# Extend forecast
show_warn = False
if extend and extra_pct>0 and len(forecast)>0:
    extra = int(len(forecast)*extra_pct/100)
    trend = (forecast[-1]-forecast[0])/len(forecast)
    forecast = np.concatenate([forecast, [forecast[-1]+trend*(i+1) for i in range(extra)]])
    show_warn = True

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
    <div style="font-size:0.65rem;color:var(--muted);font-family:'Space Mono',monospace;margin-top:0.2rem;">Trained {trained}</div>
  </div>
</div>""", unsafe_allow_html=True)


# ─── Signal Box ───────────────────────────────────────────────────────────────
sig = signal_data["signal"].lower()
sig_col = "var(--accent)" if sig=="buy" else ("var(--accent3)" if sig=="sell" else "var(--warn)")
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
ret_str  = f"{'+'if signal_data['ret']>=0 else ''}{signal_data['ret']:.2f}%"
mae_col  = "green" if metrics["MAE"]<20 else "red"
dir_col  = "green" if metrics["DIR"]>55 else ("yellow" if metrics["DIR"]>45 else "red")

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


# ─── Warnings ─────────────────────────────────────────────────────────────────
if show_warn:
    st.markdown(f'<div class="warn-box">⚠  EXTRAPOLATION WARNING — Forecast extended by {extra_pct}%. Reliability decreases beyond the recommended {cfg["forecast_days"]}-day window. Treat extended projections as directional estimates only.</div>', unsafe_allow_html=True)

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

# ── Tab 1: Chart ──────────────────────────────────────────────────────────────
with tab1:
    if len(forecast)>0:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        hist_close = df["Close"].tail(60)
        hist_dates = hist_close.index
        fc_dates   = []
        d = datetime.now(); cnt = 0
        while cnt < len(forecast):
            d += timedelta(days=1)
            if d.weekday()<5: fc_dates.append(d); cnt+=1

        fig = make_subplots(rows=2,cols=1,shared_xaxes=True,
                            row_heights=[0.72,0.28],vertical_spacing=0.04)
        fig.add_trace(go.Scatter(x=hist_dates,y=hist_close,mode="lines",name="Historical",
                                  line=dict(color="#6e7681",width=1.5)),row=1,col=1)
        std_fc = float(df["Close"].std())*0.05
        ub = [f+std_fc*(1+i*0.05) for i,f in enumerate(forecast)]
        lb = [f-std_fc*(1+i*0.05) for i,f in enumerate(forecast)]
        fig.add_trace(go.Scatter(x=fc_dates+fc_dates[::-1],y=ub+lb[::-1],
                                  fill="toself",fillcolor="rgba(0,136,255,0.07)",
                                  line=dict(color="rgba(0,0,0,0)"),showlegend=False),row=1,col=1)
        sig_color = "#00ff88" if signal_data["signal"]=="BUY" else ("#ff4466" if signal_data["signal"]=="SELL" else "#ffaa00")
        fig.add_trace(go.Scatter(x=fc_dates,y=forecast,mode="lines+markers",
                                  name=f"Forecast ({best_model})",
                                  line=dict(color=sig_color,width=2,dash="dot"),
                                  marker=dict(size=4,color=sig_color)),row=1,col=1)
        fig.add_trace(go.Scatter(x=[hist_dates[-1],fc_dates[0]],
                                  y=[float(hist_close.iloc[-1]),float(forecast[0])],
                                  mode="lines",line=dict(color=sig_color,width=1,dash="dot"),
                                  showlegend=False),row=1,col=1)
        fig.add_hline(y=price_info["price"],line_dash="dot",
                       line_color="rgba(255,255,255,0.2)",line_width=1,row=1,col=1)
        if "Volume" in df.columns:
            vol_hist = df["Volume"].tail(60)
            colors_v = ["#00ff88" if c>=o else "#ff4466"
                        for c,o in zip(df["Close"].tail(60),df["Open"].tail(60))]
            fig.add_trace(go.Bar(x=hist_dates,y=vol_hist,name="Volume",
                                  marker_color=colors_v,opacity=0.6),row=2,col=1)
        fig.update_layout(height=480,paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(13,17,23,0.8)",
                           font=dict(family="Space Mono",color="#6e7681",size=10),
                           legend=dict(bgcolor="rgba(13,17,23,0.8)",bordercolor="#21262d",
                                       borderwidth=1,font=dict(size=10),x=0.01,y=0.99),
                           margin=dict(l=0,r=0,t=10,b=0),hovermode="x unified")
        fig.update_xaxes(gridcolor="rgba(33,38,45,0.5)",zeroline=False,tickfont=dict(size=9))
        fig.update_yaxes(gridcolor="rgba(33,38,45,0.5)",zeroline=False,
                          tickfont=dict(size=9),tickprefix="$")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    else:
        st.warning("No forecast data available.")

# ── Tab 2: Forecast Table ─────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-hdr">Forecast Output Table</div>', unsafe_allow_html=True)
    if len(forecast)>0:
        dates=[]; d=datetime.now(); cnt=0
        while cnt<len(forecast):
            d+=timedelta(days=1)
            if d.weekday()<5: dates.append(d); cnt+=1
        rows_html = ""
        for dt, fc_v in zip(dates, forecast):
            chg = (fc_v - price_info["price"])/price_info["price"]*100 if price_info["price"] else 0
            cc  = "up" if chg>=0 else "dn"
            rows_html += f'<tr><td style="color:var(--muted)">{dt.strftime("%b %d, %Y")}</td><td style="color:var(--text)">${fc_v:.2f}</td><td class="{cc}">{"+"if chg>=0 else ""}{chg:.2f}%</td></tr>'
        st.markdown(f"""<table class="forecast-table">
        <thead><tr><th>Date</th><th>Forecast Price</th><th>Expected Change</th></tr></thead>
        <tbody>{rows_html}</tbody></table>""", unsafe_allow_html=True)
        if show_warn:
            n_ext = int(len(result["forecast"])*extra_pct/100)
            st.markdown(f'<div class="warn-box" style="margin-top:1rem;">Extended rows ({n_ext} additional) shown with reduced statistical reliability.</div>', unsafe_allow_html=True)

# ── Tab 3: Model Evaluation ───────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-hdr">Model Performance Comparison</div>', unsafe_allow_html=True)
    best_met = all_results.get(best_model,{}).get("metrics",metrics)
    ok_col   = "var(--accent)" if passes_threshold(best_met) else "var(--accent3)"
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
        <div class="model-name" style="color:{'var(--accent)' if passes_threshold(best_met) else 'var(--accent3)'}">
          {'✓ PASS' if passes_threshold(best_met) else '✗ FAIL'}
        </div>
        <div style="font-size:0.72rem;color:var(--muted);margin-top:0.4rem;font-family:'Space Mono',monospace;">
          Limit: MAE/RMSE/MAPE &lt; {THRESHOLD}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr" style="margin-top:1rem;">All Models</div>', unsafe_allow_html=True)
    rows_h = ""
    for mname, res in all_results.items():
        if not res: continue
        m = res.get("metrics",{})
        ok = passes_threshold(m)
        ib = mname==best_model
        rows_h += f"""<tr style="{'background:rgba(0,255,136,0.04);' if ib else ''}">
          <td style="color:{'var(--accent)'if ib else 'var(--text)'}">{'★ ' if ib else ''}{mname}</td>
          <td>{m.get('MAE',999):.3f}</td><td>{m.get('RMSE',999):.3f}</td>
          <td>{m.get('MAPE',999):.2f}%</td>
          <td style="color:{'var(--accent)'if m.get('DIR',0)>55 else 'var(--accent3)'}">{m.get('DIR',0):.1f}%</td>
          <td style="color:{'var(--accent)'if ok else 'var(--accent3)'}">{'✓'if ok else '✗'}</td></tr>"""
    st.markdown(f"""<table class="forecast-table">
    <thead><tr><th>Model</th><th>MAE</th><th>RMSE</th><th>MAPE</th><th>DIR</th><th>Pass</th></tr></thead>
    <tbody>{rows_h}</tbody></table>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box" style="margin-top:1rem;">
      <div class="insight-title">Evaluation Methodology</div>
      <b>MAE</b> (Mean Absolute Error) measures average price prediction error. <b>RMSE</b> penalizes
      large errors more heavily. <b>MAPE</b> expresses error as a percentage. <b>DIR</b> (Directional
      Accuracy) measures how often the model correctly predicts price direction — this is the primary
      model selection criterion. Models with MAE/RMSE/MAPE &gt; 20 are filtered out automatically.
    </div>""", unsafe_allow_html=True)

# ── Tab 4: Technical Indicators ───────────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-hdr">Technical Indicators</div>', unsafe_allow_html=True)
    rsi_v  = signal_data.get("rsi",50)
    macd_v = signal_data.get("macd_hist",0)
    bb_v   = signal_data.get("bb_pct",0.5)
    rsi_sig= "OVERSOLD ▲" if rsi_v<30 else ("OVERBOUGHT ▼" if rsi_v>70 else "NEUTRAL")
    rsi_c  = "var(--accent)" if rsi_v<30 else ("var(--accent3)" if rsi_v>70 else "var(--warn)")
    mac_sig= "BULLISH ▲" if macd_v>0 else "BEARISH ▼"
    mac_c  = "var(--accent)" if macd_v>0 else "var(--accent3)"
    bb_sig = "OVERSOLD ▲" if bb_v<0.2 else ("OVERBOUGHT ▼" if bb_v>0.8 else "NEUTRAL")
    bb_c   = "var(--accent)" if bb_v<0.2 else ("var(--accent3)" if bb_v>0.8 else "var(--warn)")
    st.markdown(f"""
    <div class="ind-row">
      <div class="ind-card"><div class="ind-name">RSI (14)</div>
        <div class="ind-val">{rsi_v:.1f}</div>
        <div class="ind-sig" style="color:{rsi_c}">{rsi_sig}</div>
        <div style="font-size:0.65rem;color:var(--muted);margin-top:0.4rem;">Oversold &lt;30 · Overbought &gt;70</div>
      </div>
      <div class="ind-card"><div class="ind-name">MACD Histogram</div>
        <div class="ind-val">{'+'if macd_v>=0 else ''}{macd_v:.3f}</div>
        <div class="ind-sig" style="color:{mac_c}">{mac_sig}</div>
        <div style="font-size:0.65rem;color:var(--muted);margin-top:0.4rem;">EMA(12) − EMA(26) − Signal(9)</div>
      </div>
      <div class="ind-card"><div class="ind-name">Bollinger %B</div>
        <div class="ind-val">{bb_v:.2f}</div>
        <div class="ind-sig" style="color:{bb_c}">{bb_sig}</div>
        <div style="font-size:0.65rem;color:var(--muted);margin-top:0.4rem;">0=Lower Band · 1=Upper Band</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if len(df)>0:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        fig2 = make_subplots(rows=3,cols=1,shared_xaxes=True,
                              row_heights=[0.4,0.3,0.3],vertical_spacing=0.04,
                              subplot_titles=["Price + Bollinger Bands","RSI (14)","MACD"])
        tail = df.tail(120)
        fig2.add_trace(go.Scatter(x=tail.index,y=tail["Close"],name="Price",
                                   line=dict(color="#6e7681",width=1.5)),row=1,col=1)
        fig2.add_trace(go.Scatter(x=tail.index,y=tail["BB_upper"],name="BB Upper",
                                   line=dict(color="rgba(0,136,255,0.5)",width=1,dash="dot")),row=1,col=1)
        fig2.add_trace(go.Scatter(x=tail.index,y=tail["BB_lower"],name="BB Lower",
                                   line=dict(color="rgba(0,136,255,0.5)",width=1,dash="dot"),
                                   fill="tonexty",fillcolor="rgba(0,136,255,0.04)"),row=1,col=1)
        fig2.add_trace(go.Scatter(x=tail.index,y=tail["RSI"],name="RSI",
                                   line=dict(color="#ffaa00",width=1.5)),row=2,col=1)
        fig2.add_hline(y=70,line_dash="dot",line_color="rgba(255,68,102,0.4)",row=2,col=1)
        fig2.add_hline(y=30,line_dash="dot",line_color="rgba(0,255,136,0.4)",row=2,col=1)
        colors_m = ["#00ff88" if v>=0 else "#ff4466" for v in tail["MACD_hist"]]
        fig2.add_trace(go.Bar(x=tail.index,y=tail["MACD_hist"],name="Hist",
                               marker_color=colors_m,opacity=0.7),row=3,col=1)
        fig2.add_trace(go.Scatter(x=tail.index,y=tail["MACD"],name="MACD",
                                   line=dict(color="#0088ff",width=1.2)),row=3,col=1)
        fig2.add_trace(go.Scatter(x=tail.index,y=tail["MACD_signal"],name="Signal",
                                   line=dict(color="#ff4466",width=1.2)),row=3,col=1)
        fig2.update_layout(height=500,paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(13,17,23,0.8)",
                            font=dict(family="Space Mono",color="#6e7681",size=9),
                            showlegend=False,margin=dict(l=0,r=0,t=25,b=0))
        fig2.update_xaxes(gridcolor="rgba(33,38,45,0.5)",zeroline=False)
        fig2.update_yaxes(gridcolor="rgba(33,38,45,0.5)",zeroline=False)
        for ann in fig2.layout.annotations:
            ann.font = dict(size=9,color="#6e7681",family="Space Mono")
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
