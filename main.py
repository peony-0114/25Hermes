import streamlit as st
import pandas as pd
import zipfile
import io
import requests
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# GitHub의 raw zip URL
ZIP_URL = "https://raw.githubusercontent.com/peony-0114/25peonyoops/main/archive.zip"

@st.cache_data
def load_csv_from_zip(url):
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for filename in z.namelist():
            if filename.endswith('.csv'):
                with z.open(filename) as f:
                    df = pd.read_csv(f)
                    df["AQI Value"] = pd.to_numeric(df["AQI Value"], errors="coerce")
                    return df
    return pd.DataFrame()

@st.cache_data
def geocode_locations(df):
    geolocator = Nominatim(user_agent="air_pollution_mapper")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    def get_coordinates(row):
        try:
            location = geocode(f"{row['City']}, {row['Country']}")
            if location:
                return pd.Series([location.latitude, location.longitude])
        except:
            return pd.Series([None, None])
        return pd.Series([None, None])

    coords = df.apply(get_coordinates, axis=1)
    df[['Latitude', 'Longitude']] = coords
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    return df

def main():
    st.title("🌍 Global Air Pollution Map from GitHub archive.zip")

    df = load_csv_from_zip(ZIP_URL)
    if df.empty:
        st.error("❌ CSV 파일을 archive.zip에서 불러오지 못했습니다.")
        return

    df = geocode_locations(df)

    aqi_filter = st.slider("Select AQI range to display", 0, 500, (0, 100))

    filtered_df = df[(df["AQI Value"] >= aqi_filter[0]) & (df["AQI Value"] <= aqi_filter[1])]

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered_df,
                get_position='[Longitude, Latitude]',
                get_color='[255, 140, 0, 160]',
                get_radius=50000,
                pickable=True,
            ),
        ],
        tooltip={"text": "City: {City}\nAQI: {AQI Value}\nCategory: {AQI Category}"}
    ))

    st.dataframe(filtered_df[['Country', 'City', 'AQI Value', 'AQI Category']])

if __name__ == "__main__":
    main()
