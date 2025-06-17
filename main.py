import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌡️ 우리나라 대기 온도 변화 시각화 앱")

# 파일 업로드 받기
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

# 데이터 불러오기 함수
def load_data(file):
    encodings = ['utf-8', 'cp949', 'utf-8-sig']
    delimiters = [',', '\t', ';']

    for enc in encodings:
        for delim in delimiters:
            try:
                df = pd.read_csv(file, encoding=enc, delimiter=delim)
                if df.shape[1] > 1:
                    return df
            except:
                continue
    return None

# 파일이 업로드된 경우
if uploaded_file is not None:
    df = load_data(uploaded_file)

    if df is None:
        st.error("❌ CSV 파일을 읽는 데 실패했습니다. 인코딩 또는 형식을 확인해주세요.")
    else:
        st.success("✅ 데이터가 성공적으로 불러와졌습니다!")

        # 컬럼 정리
        df.columns = df.columns.str.strip()
        st.write("📋 데이터 미리보기:")
        st.dataframe(df.head())

        # 날짜 컬럼 추정
        date_col_candidates = [col for col in df.columns if '일' in col or '날짜' in col or 'date' in col.lower()]
        if date_col_candidates:
            date_col = st.selectbox("🗓️ 날짜 컬럼 선택", date_col_candidates)
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col])
        else:
            st.error("날짜 정보를 가진 컬럼을 찾을 수 없습니다.")
            st.stop()

        # 지역 선택
        if '지점명' in df.columns:
            regions = df['지점명'].unique()
            selected_region = st.selectbox("📍 지역 선택", regions)
            df = df[df['지점명'] == selected_region]

        # 기온 컬럼 선택
        temp_cols = [col for col in df.columns if '기온' in col or '온도' in col]
        if not temp_cols:
            st.error("기온 관련 컬럼을 찾을 수 없습니다.")
            st.stop()

        selected_temp_col = st.selectbox("🌡️ 기온 컬럼 선택", temp_cols)

        # 시각화
        fig = px.line(df, x=date_col, y=selected_temp_col,
                      title=f"{selected_region}의 기온 변화 추이" if 'selected_region' in locals() else "기온 변화 추이",
                      labels={selected_temp_col: "기온 (°C)", date_col: "날짜"})
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽에서 CSV 파일을 업로드해주세요.")
