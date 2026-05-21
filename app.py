import streamlit as st
from openai import OpenAI

# 1. 스트림릿 비밀금고에서 열쇠 꺼내기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 웹사이트 기본 세팅
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 콘텐츠 생산 기지 (Ver 3.0 - 크리에이티브 오피셜)")
st.caption("대장님전용 무인 공장 라인입니다. 매번 단어의 특성에 맞춰 새로운 위트와 카피를 창작합니다.")

st.markdown("---")

# 키워드 입력창
keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 국밥, 막걸리, 치맥, 쌈")

if st.button("🚀 X & 쓰레드 콘텐츠 동시 생성"):
    if keyword:
        with st.spinner(f"'{keyword}'의 매력을 힙하게 분석하여 카피를 창작 중입니다..."):
            
            # --- 🎯 [자율성 부여 & 페르소나 강화] 프롬프트 튜닝 ---
            prompt_base = f"""
            너는 외국인들이 한국어 메뉴판을 마주했을 때, 단 1초 만에 단어의 구조를 직관적으로 깨닫고 그 맛과 문화에 빠져들게 만드는 글로벌 브랜드 'TastyHangul'의 천재 카피라이터야.
            
            [💡 핵심 정체성: 한글 해부]
            - 입력된 키워드 단어의 '글자 하나하나'를 쪼개서 직관적인 뜻을 알려주는 구조(Parsing)는 반드시 포함해야 해.
            
            [❌ 절대 금지 사항: 복사 붙여넣기 금지]
            - 기존에 썼던 "You see this on every menu...", "Simple, right?", "Now you'll never forget it!" 같은 고정된 문장 형식을 다른 단어에 똑같이 반복하지 마라. 3-4개 글을 연달아 봐도 전혀 복붙 느낌이 나지 않아야 한다.
            
            [🎯 크리에이티브 지침]
            1. **오프닝 훅(Hook):** 해당 음식/단어가 가진 고유한 특징, 맛, 혹은 한국인들이 이 음식을 대하는 리얼한 분위기를 살려 매번 다르고 기발한 영문 훅으로 시작해라.
            2. **위트와 뉘앙스:** 단순 번역기가 아니다. 외국인이 읽었을 때 "아! 힙하다, 재밌다"라고 느낄 만한 세련된 글로벌 감성의 위트(Wit)를 믹스해라.
            3. **언어:** 모든 본문 카피는 세련된 영어(English)로 작성한다.
            
            현재 입력된 주제 키워드: {keyword}
            """

            # X 버전: 짧고 강렬한 숏폼 (단어별 맞춤형 드립)
            prompt_x = prompt_base + """
            [X 버전 조건]
            - 글자 수 280자 이내 최적화.
            - 단어 구조를 깔끔하게 줄바꿈하여 보여주되, 앞뒤 문장은 이 단어만을 위해 새롭게 창작된 카피여야 함.
            - 해시태그는 #TastyHangul 과 키워드 영어 표기 딱 2개만 깔끔하게 조합할 것.
            """
            
            # 쓰레드 버전: 숏폼 구조 + 무릎을 탁 치게 만드는 로컬 팁
            prompt_threads = prompt_base + """
            [쓰레드 버전 조건]
            - X 버전의 힙한 레이아웃을 공유하되, 하단에 '진짜 한국인들만 아는 리얼한 로컬 다이닝 매너나 꿀팁(Insider Tip)'을 2~3줄 추가할 것.
            - "마늘과 쌈장을 곁들여라" 같은 뻔하고 지루한 가이드 절대 금지. 
            - 예: (국밥이면 부추무침이나 다대기 조합 매너, 막걸리면 비 오는 날 파전과의 상관관계나 흔들어 마시는 타이밍 등) 그 음식에 특화된 진짜 재밌는 문화를 짚어줄 것.
            """

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

                # 화면에 양옆으로 이쁘게 배치
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🦅 X (트위터) 버전")
                    st.caption("단어 맞춤형 크리에이티브 숏폼")
                    st.text_area("X 원고", value=text_x, height=450)

                with col2:
                    st.subheader("🧵 쓰레드(Threads) 버전")
                    st.caption("숏폼 구조 + 진짜 로컬 인사이더 팁")
                    st.text_area("쓰레드 원고", value=text_threads, height=450)

            except Exception as e:
                st.error(f"AI 가동 중 에러가 발생했습니다: {e}")
    else:
        st.warning("⚠️ 키워드를 입력하셔야 공장이 돌아갑니다!")
