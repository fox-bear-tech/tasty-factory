import streamlit as st
from openai import OpenAI

# 1. 스트림릿 비밀금고에서 열쇠 꺼내기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 웹사이트 기본 세팅
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 콘텐츠 생산 기지 (Ver 1.3)")
st.caption("대장님전용 무인 공장 라인입니다. 영문 전용 및 다이닝 에티켓 필터가 강화되었습니다.")

st.markdown("---")

# 키워드 입력창
keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겹살, 국밥, 쌈")

if st.button("🚀 X & 쓰레드 콘텐츠 동시 생성"):
    if keyword:
        with st.spinner(f"'{keyword}' 주제로 글로벌 타겟 고품격 원고를 생성 중입니다..."):
            
            # --- 🎯 [브랜드 세계관 & 언어 통제] 프롬프트 최종 고도화 ---
            prompt_base = f"""
            너는 외국인에게 한국의 깊이 있는 식문화, 메뉴 해석, 올바른 다이닝 에티켓을 우아하고 위트 있게 스토리텔링하는 'TastyHangul'의 글로벌 브랜드 디렉터이자 수석 카피라이터야.
            
            [⚠️ 언어 및 국가 타겟 지침 - 필수 준수]
            - 모든 원고의 본문은 반드시 **세련되고 매끄러운 영어(English)**로만 작성해야 한다. 한국어로 본문을 작성하는 것은 절대 금지한다.
            - 타겟 독자는 한국 식문화에 호기심이 많고, 제대로 된 로컬 문화를 배우고 싶어 하는 지적인 외국인들이다.
            
            [💡 브랜드 네이밍 및 철학 반영]
            - 브랜드 이름 'TastyHangul'의 핵심은 한국어 메뉴판에 적힌 '한글(Hangul)' 단어 그 자체에 담긴 흥미로운 언어적 의미나 문화적 배경을 짚어내고, 이를 진짜 '맛(Tasty)'과 연결해 주는 것이다.
            - 따라서 영문 본문 중에 핵심 키워드(예: Samgyeopsal, Makgeolli 등)의 한글 단어 뜻(예: 'Sam' means 'three', 'Gyeop' means 'layers')을 위트 있게 설명하는 구간을 반드시 포함시켜라.
            
            [❌ 절대 금지 사항]
            1. 엉터리 번역 및 매칭 절대 금지 (맥주는 'Beer', 막걸리는 'Makgeolli (Korean rice wine)', 소주는 'Soju'로 명확히 구분할 것).
            2. "Hey there, food explorers!" 또는 유치한 서바이벌 한국어 가이드("이것 좀 주세요라고 말하세요" 등) 같은 가볍고 싸구려 톤은 절대 금지한다. 잡지 에디터처럼 고급스럽고 통찰력 있는 톤을 유지해라.
            
            주제 키워드: {keyword}
            """

            # X(트위터)용 요청 (글로벌 지적 타겟향 영문 훅)
            prompt_x = prompt_base + """
            [X 버전 조건]
            - 글자 수 280자 이내의 영문(English) 최적화.
            - 키워드 한글 단어가 가진 매력을 임팩트 있게 던지는 세련된 영문 훅(Hook)으로 시작할 것.
            - 해시태그는 #TastyHangul 과 키워드 관련 딱 2개만 깔끔하게 조합할 것.
            - 가벼운 이모지 1~2개만 세련되게 믹스할 것.
            """
            
            # 쓰레드용 요청 (고품격 스토리텔링 + 진짜 다이닝 에티켓)
            prompt_threads = prompt_base + """
            [쓰레드 버전 조건]
            - 호흡이 깊고 매끄러운 영문(English) 에세이/스토리텔링형 원고 (500자 내외).
            - 문단 사이에 가독성을 위한 줄바꿈을 확실히 할 것.
            - [필수 내용 구조]: 
              1) 이 음식의 '한글 이름'이 왜 그렇게 지어졌는지 언어적/문화적 재미 요소를 영문으로 품격 있게 풀어줄 것.
              2) 외국인이 실제 식당에서 이 문화를 즐길 때 무릎을 탁 칠 만한 한국인만의 진짜 다이닝 매너나 에티켓(예: 고기 굽는 주도권 매너, 쌈을 조화롭게 즐기는 법 등)을 고급스러운 인사이더 팁으로 포함할 것.
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
                    st.caption("글로벌 훅 + 링구얼 인포그래픽 (영문)")
                    st.text_area("X 원고", value=text_x, height=450)

                with col2:
                    st.subheader("🧵 쓰레드(Threads) 버전")
                    st.caption("한글 스토리 + 고품격 에티켓 에세이 (영문)")
                    st.text_area("쓰레드 원고", value=text_threads, height=450)

            except Exception as e:
                st.error(f"AI 가동 중 에러가 발생했습니다: {e}")
    else:
        st.warning("⚠️ 키워드를 입력하셔야 공장이 돌아갑니다!")
