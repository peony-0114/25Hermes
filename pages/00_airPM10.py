import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기 및 정리
@st.cache_data
def load_data():
    df_raw = pd.read_csv("연도별 배출량.csv", encoding='cp949', skiprows=1)
    df_raw = df_raw.rename(columns={df_raw.columns[0]: "연도"})
    df_raw = df_raw.dropna(how='all')  # 전부 비어 있는 행 제거
    df_raw["연도"] = df_raw["연도"].astype(str)

    # 모든 수치형 열을 정수로 변환
    for col in df_raw.columns[1:]:
        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')
    
    return df_raw

df = load_data()

st.title("📊 연도별 대기오염물질 배출량 시각화")

# 시각화할 오염물질 선택
pollutants = df.columns[1:]
selected = st.multiselect("📌 시각화할 오염물질을 선택하세요", pollutants, default=["PM-2.5", "NOx", "CO"])

# 선택된 오염물질만 시각화
if selected:
    df_melted = df.melt(id_vars="연도", value_vars=selected, var_name="오염물질", value_name="배출량")
    
    fig = px.line(df_melted,
                  x="연도", y="배출량", color="오염물질",
                  markers=True,
                  title="연도별 오염물질 배출량 (톤/yr)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("하나 이상의 오염물질을 선택해주세요.")

# 원본 데이터 보기
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df)
