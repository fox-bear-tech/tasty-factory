import streamlit as st
from openai import OpenAI

# 1. 스트림릿 비밀금고(Secrets)에서 열쇠 꺼내서 AI 비서 깨우기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 웹사이트 기본 세팅
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 콘텐츠 생산 기지 (Ver 1.0)")
st.caption("대장님전용 무인 공장 라인입니다. 실시간 AI가 가동됩니다.")

st.markdown("---")

# 키워드 입력창
keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겹살, 국밥, 반찬")

if st.button("🚀 X & 쓰레드 콘텐츠 동시 생성"):
    if keyword:
        with st.spinner(f"'{keyword}' 주제로 AI가 실시간 원고를 쥐어짜는 중입니다... 잠시만 기다려주세요! ☕"):
            
            # --- 2. 대장님만의 'TastyHangul' 영혼(프롬프트) 주입 공간 ---
            prompt_base = f"""
            너는 외국인에게 한국의 매력적인 식문화와 한식을 전문적으로 소개하는 최고의 카피라이터이자 'TastyHangul'의 메인 디렉터야.
            사용자가 제시한 한국 음식 키워드를 바탕으로, 외국인들이 흥미진진해할 만한 식문화 스토리텔링, 유용한 다이닝 팁, 
            그리고 특유의 위트 있고 세련된 말투를 가미해서 소셜 미디어용 원고를 작성해줘.
            
            주제 키워드: {keyword}
            """

            # X(트위터)용 요청
            prompt_x = prompt_base + "\n[조건] 280자 이내의 짧고 강렬한 한 줄 훅(Hook)과 핵심 요약 형태로 영어로 작성해줘. 적절한 이모지 포함."
            # 쓰레드용 요청
            prompt_threads = prompt_base + "\n[조건] 500자 내외로, 호흡이 친근하고 스토리텔링이 풍부한 타래 분리형 원고로 영어로 작성해줘. 적절한 이모지 포함."

            try:
                # X 원고 실시간 생성
                response_x = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_x}]
                )
                text_x = response_x.choices[0].message.content

                # 쓰레드 원고 실시간 생성
                response_threads = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_threads}]
                )
                text_threads = response_threads.choices[0].message.content

                # 3. 화면에 양옆으로 멋지게 뿌려주기
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🦅 X (트위터) 버전")
                    st.caption("280자 최적화 훅 스타일")
                    st.text_area("X 원고", value=text_x, height=300)
                    st.button("💾 X 원고 독스로 전송 (준비중)")

                with col2:
                    st.subheader("🧵 쓰레드(Threads) 버전")
                    st.caption("스토리텔링형 타래 스타일")
                    st.text_area("쓰레드 원고", value=text_threads, height=300)
                    st.button("💾 쓰레드 원고 독스로 전송 (준비중)")

            except Exception as e:
                st.error(f"AI 가동 중 에러가 발생했습니다: {e}")
    else:
        st.warning("⚠️ 키워드를 입력하셔야 공장이 돌아갑니다!")
