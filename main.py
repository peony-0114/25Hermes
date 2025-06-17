import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("우리나라 대기 온도 변화 시각화")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("STCS_우리나라기후평년값_DD_20250617144904.csv", encoding="cp949")
    df.columns = df.columns.str.strip()  # 혹시 모를 공백 제거
    return df

df = load_data()

# 날짜 처리 (일자 컬럼이 있다면)
if '일자' in df.columns:
    df['일자'] = pd.to_datetime(df['일자'], errors='coerce')

# 온도 관련 컬럼 찾기
temp_cols = [col for col in df.columns if '기온' in col or '온도' in col]

# 지역 선택
if '지점명' in df.columns:
    regions = df['지점명'].unique()
    selected_region = st.selectbox("지역 선택", regions)
    df = df[df['지점명'] == selected_region]

# 온도 컬럼 선택
if temp_cols:
    selected_temp_col = st.selectbox("기온 데이터 선택", temp_cols)
else:
    st.error("기온 관련 컬럼을 찾을 수 없습니다.")
    st.stop()

# 시각화
if '일자' in df.columns:
    fig = px.line(df, x='일자', y=selected_temp_col,
                  title=f"{selected_region}의 기온 변화",
                  labels={selected_temp_col: "기온 (°C)", '일자': "날짜"})
    st.plotly_chart(fig)
else:
    st.error("날짜 정보를 찾을 수 없습니다.")
