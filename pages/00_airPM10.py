import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("미세먼지(PM10)+월별+도시별+대기오염도+.csv", encoding="cp949")
    df = df.dropna(how="any")
    df["측정일"] = pd.to_datetime(df["측정일"], format="%Y-%m")
    return df

df = load_data()

st.title("🌫️ 도시별 미세먼지(PM10) 월별 오염도 시각화")

# 도시 선택
cities = df["도시"].unique()
selected_cities = st.multiselect("도시를 선택하세요", options=sorted(cities), default=["서울"])

# 기간 선택
min_date = df["측정일"].min()
max_date = df["측정일"].max()
date_range = st.slider(
    "기간을 선택하세요",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM"
)

# 필터링
filtered = df[
    (df["도시"].isin(selected_cities)) &
    (df["측정일"] >= date_range[0]) &
    (df["측정일"] <= date_range[1])
]

# Plotly 그래프
fig = px.line(
    filtered,
    x="측정일",
    y="PM10",
    color="도시",
    markers=True,
    title="도시별 월별 미세먼지(PM10) 농도 변화",
    labels={"측정일": "측정일", "PM10": "미세먼지(PM10)", "도시": "도시"}
)
fig.update_layout(xaxis_title="측정일", yaxis_title="PM10 농도 (㎍/㎥)", hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

# 데이터 보기
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(filtered)
