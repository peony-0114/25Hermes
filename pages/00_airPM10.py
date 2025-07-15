import streamlit as st

# 🌍 10개 국가별 환경지표 데이터와 이미지
country_data = {
    "South Korea": {
        "Forest Area (%)": 63,
        "Main Policy": "2050 탄소중립 전략, 도시숲 조성 사업",
        "Goal": "2030년까지 산림 흡수원 강화",
        "Image": "https://flagcdn.com/w320/kr.png"
    },
    "Brazil": {
        "Forest Area (%)": 59,
        "Main Policy": "아마존 벌채 감축 정책",
        "Goal": "2028년까지 불법 벌목 제로",
        "Image": "https://flagcdn.com/w320/br.png"
    },
    "Indonesia": {
        "Forest Area (%)": 49,
        "Main Policy": "팜유 농장 확장 금지 조치",
        "Goal": "2035년까지 열대우림 복원",
        "Image": "https://flagcdn.com/w320/id.png"
    },
    "United States": {
        "Forest Area (%)": 33,
        "Main Policy": "산림 관리 및 화재 방지 프로그램",
        "Goal": "2050년까지 탄소배출 50% 감축",
        "Image": "https://flagcdn.com/w320/us.png"
    },
    "Germany": {
        "Forest Area (%)": 32,
        "Main Policy": "에너지 전환 정책(Energiewende)",
        "Goal": "2030년까지 재생에너지 65% 확대",
        "Image": "https://flagcdn.com/w320/de.png"
    },
    "India": {
        "Forest Area (%)": 24,
        "Main Policy": "2025년까지 녹지 면적 33% 목표",
        "Goal": "2030년까지 탄소배출 40% 감축",
        "Image": "https://flagcdn.com/w320/in.png"
    },
    "China": {
        "Forest Area (%)": 22,
        "Main Policy": "대규모 조림사업(Great Green Wall)",
        "Goal": "2060년 탄소중립 달성",
        "Image": "https://flagcdn.com/w320/cn.png"
    },
    "Australia": {
        "Forest Area (%)": 17,
        "Main Policy": "산림 복원 및 화재 방지 프로그램",
        "Goal": "2050년까지 탄소중립 달성",
        "Image": "https://flagcdn.com/w320/au.png"
    },
    "Canada": {
        "Forest Area (%)": 38,
        "Main Policy": "지속가능한 산림 관리 전략",
        "Goal": "2030년까지 온실가스 45% 감축",
        "Image": "https://flagcdn.com/w320/ca.png"
    },
    "Norway": {
        "Forest Area (%)": 34,
        "Main Policy": "열대우림 보호를 위한 국제지원",
        "Goal": "2050년까지 탄소배출 제로",
        "Image": "https://flagcdn.com/w320/no.png"
    }
}

# 🌱 Streamlit 앱 시작
st.title("🌍 국가별 환경지표 카드 UI")
st.write("국가별 산림 면적 비율, 주요 정책 및 목표를 확인하세요.")

# 국가 선택 드롭다운
selected_country = st.selectbox("국가를 선택하세요", list(country_data.keys()))

# 선택한 국가의 데이터 표시
info = country_data[selected_country]

# 카드 UI 표시
st.image(info['Image'], width=150)  # 국가 이미지 표시
st.markdown(f"""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
        <h2 style="color:#2c7a7b;">🌿 {selected_country}</h2>
        <p><b>🌳 Forest Area (%):</b> {info['Forest Area (%)']}%</p>
        <p><b>🛡️ Main Policy:</b> {info['Main Policy']}</p>
        <p><b>🚀 Goal:</b> {info['Goal']}</p>
    </div>
""", unsafe_allow_html=True)
