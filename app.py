#William Polan U0000012741
import streamlit as st
import requests
import pandas as pd
import altair as alt

@st.cache_data
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API.")
        return []

st.title("Cryptocurrency Prices")

#Allow user to select how many diffrent coins are displayed in table
numberOfResults = st.slider("How Many Coins To Display In Chart",1,20,10) 

#Get API Data for current markert, price etc..
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": numberOfResults}
data = fetch_data(url + "?" + "&".join(f"{k}={v}" for k, v in params.items()))
df = pd.DataFrame(data)

#Output Coin data as table
st.dataframe(df[[
    "name",
    "symbol",
    "current_price",
    "market_cap",
    "price_change_percentage_24h"
]])

#Show the top 3 coin as percent of pie chart
st.subheader("Top 3 Coin Price Distribution")
pie = alt.Chart(df.head(3)).mark_arc().encode(theta="current_price:Q",color="name:N",tooltip=["name", "current_price"])
st.altair_chart(pie, width="stretch")

#Ask user to select coin to view price vs time
st.subheader("Current Price In USD")
coin = st.selectbox(
    "Select a coin to view on graph",
    df["id"]
)

#Ask user which time period to view coin price
time_options = {
    "1 Day": 1,
    "30 Days": 30,
    "90 Days": 90,
    "1 Year": 365
}
time_label = st.selectbox("Select time range", list(time_options.keys()))
timeScale = time_options[time_label]

#Get API Data for price at diffrent time periods
url2 = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params2 = {"vs_currency": "usd", "days": timeScale}
data = fetch_data(url2 + "?" + "&".join(f"{k}={v}" for k, v in params2.items()))
prices = data["prices"]

#Show the selected coins price at the selected time scale
df2 = pd.DataFrame(prices, columns=["timestamp", "price"])
df2["timestamp"] = pd.to_datetime(df2["timestamp"], unit="ms")
chart = alt.Chart(df2).mark_line().encode(
    x="timestamp:T",
    y="price:Q",
    tooltip=["timestamp", "price"]
).properties(
    title=f"{coin.capitalize()} Price (Last {timeScale} Days)"
)
st.altair_chart(chart, width='stretch')




