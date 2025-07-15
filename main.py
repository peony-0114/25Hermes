import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 불러오기
try:
    data = pd.read_csv("combined_deforestation_species.csv")
    st.success("✅ 데이터 로드 성공")
except FileNotFoundError:
    st.error("❌ 데이터 파일을 찾을 수 없습니다.")
    st.stop()

st.title("🌳 Deforestation & Threatened Species Trends")
st.write("연도별 산림 파괴율(%)과 멸종위기종 개체 수 시각화")

# 연도 슬라이더
years = data['Year']
start_year, end_year = st.slider(
    "연도 범위 선택",
    min_value=int(years.min()),
    max_value=int(years.max()),
    value=(int(years.min()), int(years.max()))
)

# 데이터 필터링
filtered = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

if filtered.empty:
    st.warning("⚠️ 선택한 연도 범위에 데이터가 없습니다.")
else:
    fig = go.Figure()

    # Forest Loss (%) - 꺾은선
    fig.add_trace(go.Scatter(
        x=filtered['Year'],
        y=filtered['Forest Loss (%)'],
        name='Forest Loss Rate (%)',
        mode='lines+markers',
        line=dict(color='green', width=3)
    ))

    # Threatened Species - 막대그래프 (같은 Y축)
    fig.add_trace(go.Bar(
        x=filtered['Year'],
        y=filtered['Threatened Species'],
        name='Threatened Species Count',
        marker=dict(color='rgba(255, 0, 0, 0.5)')
    ))

    # 레이아웃
    fig.update_layout(
        title="Deforestation (Line) vs Threatened Species (Bar)",
        xaxis=dict(title='Year'),
        yaxis=dict(title='Value'),
        legend=dict(x=0.01, y=0.99),
        bargap=0.3,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
