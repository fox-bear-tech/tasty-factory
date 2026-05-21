import streamlit as st
from openai import OpenAI

# 1. 스트림릿 비밀금고에서 열쇠 꺼내기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 웹사이트 기본 세팅
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 콘텐츠 생산 기지 (Ver 2.0 - 오리지널 숏폼 패치)")
st.caption("대장님전용 무인 공장 라인입니다. 군더더기를 빼고 직관적인 '한글 분해 레이아웃'으로 전면 고정되었습니다.")

st.markdown("---")

# 키워드 입력창
keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겹살, 국밥, 막걸리")

if st.button("🚀 X & 쓰레드 콘텐츠 동시 생성"):
    if keyword:
        with st.spinner(f"'{keyword}' 주제로 직관적인 숏폼 원고를 추출 중입니다..."):
            
            # --- 🎯 [레퍼런스 양식 강제 고정] 프롬프트 튜닝 ---
            prompt_base = f"""
            너는 외국인들이 한국어 메뉴판을 쉽게 읽고 이해할 수 있도록 한글 단어의 구조를 직관적이고 심플하게 분해해 주는 'TastyHangul'의 브랜드 카피라이터야.
            
            [💡 핵심 작성 원칙]
            1. 구구절절 긴 문장으로 설명하는 에세이나 칼럼 스타일은 절대 금지한다.
            2. 무조건 스크롤을 내리다 1초 만에 시선이 꽂히도록 **심플하고 직관적인 레이아웃(줄바꿈과 단어 분해)**을 사용해라.
            3. 본문은 무조건 세련된 영어(English)로 작성하되, 타겟 메뉴의 '한글 발음'과 '글자별 의미'를 명확하게 매칭해 주어야 한다.
            
            [🎯 X(트위터) 버전 필수 양식 예시]
            아래 샘플과 완벽하게 동일한 톤앤매너와 레이아웃 구조로만 작성해라:
            
            You see this on every Korean BBQ menu. But can you actually read it? 
            삼겹살 (Sam-gyeop-sal)
            
            삼 (Sam) = 3
            겹 (Gyeop) = Layer
            살 (Sal) = Meat
            
            It means "Three-layer meat." Simple, right? 
            Now you'll never forget it!
            #TastyHangul #Samgyeopsal
            
            [🎯 쓰레드(Threads) 버전 필수 양식]
            - X 버전과 결을 같이 하되, 하단에 외국인이 실제 식당에서 활용할 수 있는 짧고 임팩트 있는 '원포인트 컬처/다이닝 팁'을 딱 2~3줄만 심플하게 추가할 것. (이 역시 긴 문장 금지, 줄바꿈 확실히)
            
            현재 입력된 주제 키워드: {keyword}
            """

            try:
                # X 원고 실시간 생성
                response_x = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_base + "\n\n[지시] 위 규칙과 샘플 양식을 바탕으로 입력된 키워드에 맞는 'X 버전' 원고를 정확히 출력해라."}]
                )
                text_x = response_x.choices[0].message.content

                # 쓰레드 원고 실시간 생성
                response_threads = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_base + "\n\n[지시] 위 규칙과 샘플 양식을 바탕으로 하단에 원포인트 다이닝 팁이 깔끔하게 추가된 '쓰레드 버전' 원고를 정확히 출력해라."}]
                )
                text_threads = response_threads.choices[0].message.content

                # 화면에 양옆으로 이쁘게 배치
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🦅 X (트위터) 버전")
                    st.caption("직관적인 한글 형태소 분해 숏폼")
                    st.text_area("X 원고", value=text_x, height=400)

                with col2:
                    st.subheader("🧵 쓰레드(Threads) 버전")
                    st.caption("한글 분해 숏폼 + 원포인트 다이닝 팁")
                    st.text_area("쓰레드 원고", value=text_threads, height=400)

            except Exception as e:
                st.error(f"AI 가동 중 에러가 발생했습니다: {e}")
    else:
        st.warning("⚠️ 키워드를 입력하셔야 공장이 돌아갑니다!")
