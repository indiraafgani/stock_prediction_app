# ◈ SIGNAL — Trading Intelligence Dashboard

A high-performance, minimalistic trading signal dashboard built with Streamlit.

## Features

- **18 Major Tickers**: AAPL, MSFT, GOOG, AMZN, NVDA, META, AVGO, TSLA, AMD, INTC, ORCL, ADBE, CSCO, QCOM, NFLX, COST, PEP, UBER
- **3 Forecast Models**: SARIMAX (auto-tuned), Prophet, Hybrid SARIMAX+Prophet
- **Auto Model Selection**: Picks best model by Directional Accuracy (DIR) with threshold filtering
- **3 Technical Indicators**: RSI (14), MACD, Bollinger Bands %B
- **7 Time Horizons**: 1 Week → 10 Years, each with adaptive training windows
- **Trading Signals**: BUY / SELL / HOLD with confidence scores
- **Model Caching**: `.model_chance` format, daily retrain cycle
- **Forecast Extension**: Extrapolation with reliability warnings

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

```
app.py
├── fetch_data()          → Yahoo Finance data with 5-min cache
├── add_features()        → RSI, MACD, Bollinger, lag features
├── train_sarimax()       → Auto-tuned SARIMAX (grid search on p,d,q)
├── train_prophet()       → Facebook Prophet with uncertainty
├── train_hybrid()        → 55% SARIMAX + 45% Prophet blend
├── run_models()          → Parallel model runner + auto-selector
├── eval_metrics()        → MAE, RMSE, MAPE, DIR
├── generate_signal()     → BUY/SELL/HOLD with confidence
├── run_pipeline()        → Full pipeline with .model_chance caching
└── Streamlit UI          → Dark dashboard with 4 tabs
```

## Model Selection Logic

1. All models are evaluated on held-out in-sample data
2. Models with MAE/RMSE/MAPE > 20 are flagged/filtered
3. Among passing models, highest **Directional Accuracy (DIR)** wins
4. Fallback: best DIR regardless of threshold

## Horizon → Training Window Mapping

| Horizon  | Training Data | Forecast Window |
|----------|--------------|-----------------|
| 1 Week   | 3 months     | 3 trading days  |
| 1 Month  | 6 months     | 10 trading days |
| 3 Months | 12 months    | 20 trading days |
| 6 Months | 24 months    | 30 trading days |
| 1 Year   | 36 months    | 60 trading days |
| 5 Years  | 84 months    | 180 trading days|
| 10 Years | 120 months   | 365 trading days|

## Caching

Models are saved as `.model_chance` pickle files in `/tmp/.model_chance/`
keyed by `MD5(ticker + horizon + method + date)`. This ensures:
- Instant load on re-run same day
- Automatic daily retraining
- Force retrain via sidebar button
