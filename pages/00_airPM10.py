import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    # skiprows 제거하고 기본 헤더 읽기 시도
    df = pd.read_csv("연도별 배출량.csv", encoding='cp949')
    df.columns = df.columns.str.strip()  # 혹시 모를 공백 제거
    df["연도"] = df["연도"].astype(str)

    # 숫자형 변환
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

st.title("📊 연도별 대기오염물질 배출량")

options = df.columns[1:]
selected = st.multiselect("📌 시각화할 항목 선택", options, default=list(options[:3]))

if selected:
    df_melted = df.melt(id_vars="연도", value_vars=selected, var_name="오염물질", value_name="배출량")
    fig = px.line(df_melted, x="연도", y="배출량", color="오염물질", markers=True,
                  title="연도별 오염물질 배출량 추이")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("표시할 오염물질을 선택해주세요.")
