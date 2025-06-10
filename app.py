
import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

# Install correct ChromeDriver
chromedriver_autoinstaller.install()

# Streamlit App Configuration
st.set_page_config(page_title="Solana GMGN Wallet Analyzer", layout="wide")
st.title("🔍 Solana GMGN Wallet Analyzer Dashboard")

uploaded_file = st.file_uploader("Upload CSV with wallet addresses", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'wallet_address' not in df.columns:
        st.error("CSV must contain a 'wallet_address' column.")
    else:
        if 'added' not in df.columns:
            df['added'] = False

        start_analysis = st.button("Start Analysis")

        if start_analysis:
            results = []

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(options=chrome_options)

            progress_bar = st.progress(0)
            status_text = st.empty()

            total_wallets = len(df)
            start_time = time.time()

            for i, row in df.iterrows():
                wallet = row['wallet_address']
                url = f"https://gmgn.ai/sol/address/{wallet}"

                driver.get(url)
                time.sleep(5)  # Let the page fully load

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                wallet_data = {"wallet_address": wallet}

                timeframes = ['1d', '7d', '30d', 'all']
                for tf in timeframes:
                    pnl_block = soup.find('div', {'data-testid': f'{tf}-realized-pnl'})
                    win_block = soup.find('div', {'data-testid': f'{tf}-win-rate'})
                    hold_block = soup.find('div', {'data-testid': f'{tf}-average-hold-time'})

                    wallet_data[f'{tf}_pnl'] = pnl_block.text.strip() if pnl_block else "N/A"
                    wallet_data[f'{tf}_win'] = win_block.text.strip() if win_block else "N/A"
                    wallet_data[f'{tf}_hold'] = hold_block.text.strip() if hold_block else "N/A"

                wallet_data['added'] = False
                results.append(wallet_data)

                progress_bar.progress((i + 1) / total_wallets)
                elapsed = time.time() - start_time
                eta = (elapsed / (i + 1)) * (total_wallets - (i + 1))
                status_text.text(f"Processed {i + 1}/{total_wallets} wallets | ETA: {int(eta)}s")

            driver.quit()

            result_df = pd.DataFrame(results)

            st.success("Analysis complete.")
            st.dataframe(result_df)

            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="gmgn_wallet_analysis.csv", mime='text/csv')
