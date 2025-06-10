
# GMGN Wallet Analyzer (Streamlit Cloud Version)

## Features
- Upload a CSV of Solana wallet addresses
- Scrapes GMGN.ai for:
  - Realized PnL ($ + %)
  - Win Rate
  - Avg Hold Time
  - For 1D / 7D / 30D / All Time
- Sortable dashboard with export to CSV
- Runs fully on Streamlit Cloud with headless Chrome

## Setup
1. Upload to GitHub
2. Deploy at https://streamlit.io/cloud
3. Use `app.py` as the entry point

## Input Format
CSV with a header `wallet_address`, e.g.

```
wallet_address
HGqZDkAoZdxKr9bX5KqHUkbbFoEohsze3p17mr2JTC54
4H3m77dAYJ9mM1BMsYBVxeeach3an1xfT7FmrrTE6qRy
```
