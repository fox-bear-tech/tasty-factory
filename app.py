import streamlit as st

st.set_page_config(layout="wide")
st.title("🍚 TastyHangul 콘텐츠 생산 기지 (Ver 1.0)")
st.caption("대장님전용 무인 공장 라인입니다.")

st.markdown("---")

keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 공기밥, 국밥, 반찬")

if st.button("🚀 X & 쓰레드 콘텐츠 동시 생성"):
    if keyword:
        st.info(f"'{keyword}' 주제로 AI 원고를 뽑아내는 중입니다...")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🐦 X (트위터) 버전")
            st.text_area("280자 최적화 원고", value=f"In Korea, {keyword} isn't a side dish... (X 원고 예시)", height=250)
            st.button("💾 X 원고 독스로 전송")
        with col2:
            st.subheader("🧵 쓰레드(Threads) 버전")
            st.text_area("500자 타래 분리형 원고", value=f"You sit down at a K-bbq spot and order {keyword}... (쓰레드 원고 예시)", height=250)
            st.button("💾 쓰레드 원고 독스로 전송")
    else:
        st.warning("주제를 입력하셔야 공장이 돌아갑니다, 대장님!")
