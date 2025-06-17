import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (시스템에 따라 다름, 예: 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 읽기
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="cp949", skiprows=6)
    df["일시"] = pd.to_datetime(df["일시"], format="%m-%d")
    return df

df = load_data()

# Streamlit 앱 제목
st.title("📊 우리나라 기후 평년값 시각화 (1991~2020)")

# 지역 선택
regions = df["지점명"].unique()
selected_region = st.selectbox("지역을 선택하세요", sorted(regions))

# 선택된 지역의 데이터 필터링
filtered = df[df["지점명"] == selected_region].sort_values("일시")

# 그래프 그리기
st.subheader(f"📈 {selected_region}의 일별 기후 평년값")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered["일시"], filtered["평균기온(°C)"], label="평균기온 (°C)", marker='o')
ax.plot(filtered["일시"], filtered["최고기온(°C)"], label="최고기온 (°C)", linestyle='--')
ax.plot(filtered["일시"], filtered["최저기온(°C)"], label="최저기온 (°C)", linestyle='--')
ax.set_title(f"{selected_region}의 기온 추이")
ax.set_xlabel("날짜")
ax.set_ylabel("기온 (°C)")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# 강수량 및 습도
st.subheader("☔ 강수량 및 습도")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(filtered["일시"], filtered["강수량(mm)"], color='skyblue', label="강수량 (mm)")
ax2.set_ylabel("강수량 (mm)")
ax2.set_xlabel("날짜")
ax2_twin = ax2.twinx()
ax2_twin.plot(filtered["일시"], filtered["습도(%)"], color='green', label="습도 (%)", marker='x')
ax2_twin.set_ylabel("습도 (%)")
fig2.legend(loc="upper right")
plt.xticks(rotation=45)
st.pyplot(fig2)

# 데이터 테이블 보기
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(filtered)

