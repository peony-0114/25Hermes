import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

st.set_page_config(page_title="연안 수질 지도", layout="wide")
st.title("🌊 대한민국 연안 수질 지도 시각화")

@st.cache_data
def load_data():
    df = pd.read_csv("해양환경공단_해양환경측정망 정보_연안별 평균 해수수질현황_20231231.csv", encoding="cp949")
    return df

@st.cache_data
def geocode_locations(locations):
    geolocator = Nominatim(user_agent="coastal-water-quality")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    coords = {}
    for loc in locations:
        query = f"{loc} 대한민국"
        location = geocode(query)
        if location:
            coords[loc] = (location.latitude, location.longitude)
        else:
            coords[loc] = (None, None)
    return coords

# 데이터 불러오기
df = load_data()
unique_locations = df['연안명칭'].unique()
coords = geocode_locations(unique_locations)

# 위도, 경도 열 추가
df['위도'] = df['연안명칭'].map(lambda x: coords.get(x, (None, None))[0])
df['경도'] = df['연안명칭'].map(lambda x: coords.get(x, (None, None))[1])

# 유효 좌표 필터링
df_valid = df.dropna(subset=['위도', '경도'])

# 사용자 선택 수질 지표
options = ['수소이온농도 표층', '용존산소량 표층']
selected_metric = st.selectbox("표시할 수질 지표를 선택하세요:", options)

# 지도 시각화
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=36.3,
        longitude=127.8,
        zoom=5.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_valid,
            get_position='[경도, 위도]',
            get_radius=15000,
            get_fill_color=f'[255 - ({selected_metric} * 30), ({selected_metric} * 30), 150]',
            pickable=True,
        )
    ],
    tooltip={"text": "{연안명칭}\n" + selected_metric + ": {" + selected_metric + "}"}
))
