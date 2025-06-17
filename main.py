import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", encoding="cp949", skiprows=6)
    except Exception:
        try:
            df = pd.read_csv("data.csv", encoding="utf-8-sig", skiprows=6)
        except Exception:
            df = pd.read_csv("data.csv", encoding="utf-8-sig")  # 마지막 시도
    df["일시"] = pd.to_datetime(df["일시"], format="%m-%d", errors='coerce')
    df = df.dropna(subset=["일시", "지점명"])  # 파싱 실패한 날짜 제거
    return df

df = load_data()

st.title("📊 우리나라 기후 평년값 시각화 (1991~2020)")

regions = df["지점명"].dropna().unique()
selected_region = st.selectbox("🌍 지역을 선택하세요", sorted(regions))

filtered = df[df["지점명"] == selected_region].sort_values("일시")

# 기온 그래프
st.subheader(f"🌡️ {selected_region}의 일별 기온 변화")
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=filtered["일시"], y=filtered["평균기온(°C)"], name="평균기온"))
fig_temp.add_trace(go.Scatter(x=filtered["일시"], y=filtered["최고기온(°C)"], name="최고기온"))
fig_temp.add_trace(go.Scatter(x=filtered["일시"], y=filtered["최저기온(°C)"], name="최저기온"))
fig_temp.update_layout(title="기온 변화", xaxis_title="날짜", yaxis_title="°C", hovermode="x unified")
st.plotly_chart(fig_temp, use_container_width=True)

# 강수량 + 습도 그래프
st.subheader("🌧️ 강수량 및 습도")
fig_rain = go.Figure()
fig_rain.add_trace(go.Bar(x=filtered["일시"], y=filtered["강수량(mm)"], name="강수량", marker_color="lightblue"))
fig_rain.add_trace(go.Scatter(x=filtered["일시"], y=filtered["습도(%)"], name="습도", yaxis="y2", marker_color="green"))
fig_rain.update_layout(
    title="강수량 및 습도",
    xaxis_title="날짜",
    yaxis=dict(title="강수량 (mm)"),
    yaxis2=dict(title="습도 (%)", overlaying="y", side="right"),
    hovermode="x unified"
)
st.plotly_chart(fig_rain, use_container_width=True)

# 데이터 보기
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(filtered)
