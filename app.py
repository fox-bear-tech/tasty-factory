import streamlit as st
from openai import OpenAI

# 1. 스트림릿 비밀금고에서 열쇠 꺼내기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 웹사이트 기본 세팅
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 콘텐츠 생산 기지 (Ver 1.2)")
st.caption("대장님전용 무인 공장 라인입니다. '테이스티 한글' 브랜드 철학이 완벽 패치되었습니다.")

st.markdown("---")

# 키워드 입력창
keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겁살, 국밥, 쌈")

if st.button("🚀 X & 쓰레드 콘텐츠 동시 생성"):
    if keyword:
        with st.spinner(f"'{keyword}' 주제로 브랜드 철학을 담은 원고를 정밀 정제 중입니다..."):
            
            # --- 🎯 [브랜드 세계관 완벽 주입] 'TastyHangul' 오피셜 프롬프트 튜닝 ---
            prompt_base = f"""
            너는 외국인에게 한국의 깊이 있는 식문화, 메뉴 해석, 올바른 다이닝 에티켓을 우아하고 위트 있게 스토리텔링하는 'TastyHangul'의 브랜드 디렉터이자 수석 카피라이터야.
            
            [💡 브랜드 네이밍 정의 및 철학 - 원고에 반드시 반영할 것]
            - 우리 브랜드 이름은 'TastyHangul (테이스티 한글)'이야.
            - 단순한 '한식(Hansik) 소개'가 아니라, 한국어 메뉴판에 적힌 '한글(Hangul)' 단어 자체에 담긴 흥미로운 어원, 문화적 맥락, 그리고 그 안에 녹아있는 진짜 '맛(Tasty)'을 외국인에게 직관적으로 연결해 주는 고품격 가이드야.
            - 따라서 모든 원고에는 해당 음식의 '한글 단어(예: 삼겹살, 막걸리 등)'가 가진 진짜 의미나 언어적 뉘앙스를 위트 있게 풀어내어, 외국인이 한국 식당에 가서 기가 죽지 않고 "주도적으로 주문하고 문화를 즐길 수 있게" 만들어야 해.
            
            [❌ 절대 금지 및 교정 사항 - 필수 준수]
            1. 한국 주류나 음식을 영어로 번역할 때 절대 엉터리 정보(예: 맥주를 rice wine으로 매칭하는 끔찍한 오류)를 작성하지 마라.
               - 맥주는 'Beer', 막걸리는 'Makgeolli (Korean rice wine)', 소주는 'Soju'로 칼같이 구분해라.
            2. "Hey there, food explorers!" 같은 너무 가볍고 흔해 빠진 인스타 인플루언서식 싸구려 호객 톤은 절대 금지한다. 지적이고 세련된 에디터의 톤을 유지해라.
            
            주제 키워드: {keyword}
            """

            # X(트위터)용 요청 (지적이고 임팩트 있는 '한글 한 줄 훅' + 정보)
            prompt_x = prompt_base + """
            [X 버전 조건]
            - 글자 수 280자 이내 최적화.
            - 타겟의 호기심을 자극하는 세련된 훅(Hook) 문장으로 시작하되, '한글 키워드'의 직관적인 의미나 매력을 임팩트 있게 던질 것.
            - 해시태그는 #TastyHangul 과 키워드 관련 딱 2개만 깔끔하게 조합할 것.
            - 가벼운 이모지 1~2개만 세련되게 사용할 것.
            """
            
            # 쓰레드용 요청 (깊이 있는 한글 단어 스토리텔링 + 에티켓 타래)
            prompt_threads = prompt_base + """
            [쓰레드 버전 조건]
            - 호흡이 깊고 매끄러운 에세이/스토리텔링형 원고 (500자 내외).
            - 문단 사이에 가독성을 위한 줄바꿈을 확실히 할 것.
            - [필수 세부 내용]: 
              1) 왜 이 음식의 '한글 이름'이 그렇게 지어졌는지 언어적/문화적 재미 요소를 풀어줄 것.
              2) 외국인이 실제 한국 식당에서 이 음식을 먹을 때 무릎을 탁 칠 만한 한국인만의 진짜 다이닝 팁이나 문화적 에티켓(예: 불판 매너, 쌈 싸 먹는 정석 등)을 품격 있게 포함할 것.
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
                    st.caption("브랜드 훅 + 링구얼 인포그래픽")
                    st.text_area("X 원고", value=text_x, height=450)

                with col2:
                    st.subheader("🧵 쓰레드(Threads) 버전")
                    st.caption("한글 네이밍 스토리 + 고품격 다이닝 에티켓")
                    st.text_area("쓰레드 원고", value=text_threads, height=450)

            except Exception as e:
                st.error(f"AI 가동 중 에러가 발생했습니다: {e}")
    else:
        st.warning("⚠️ 키워드를 입력하셔야 공장이 돌아갑니다!")
