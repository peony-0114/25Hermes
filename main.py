import streamlit as st
import pandas as pd
import pydeck as pdk

CSV_URL = "air_pollution_with_coords.csv"  # 로컬 또는 GitHub raw 주소 가능

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

def main():
    st.title("🌍 Air Pollution Map (with Preloaded Coordinates)")

    df = load_data()

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
