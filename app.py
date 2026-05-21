import streamlit as st
from openai import OpenAI

# 1. API 열쇠 세팅
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 대화형 카피라이팅 기지 (Ver 4.0)")
st.caption("대장님과 실시간으로 대화하며 톤을 맞춰가는 크리에이티브 엔진입니다.")

st.markdown("---")

# 세션 상태(기억 창고) 초기화 - 생성된 원고를 보관하기 위함
if "text_x" not in st.session_state:
    st.session_state.text_x = ""
if "text_threads" not in st.session_state:
    st.session_state.text_threads = ""

# 상단: 키워드 입력 라인
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    keyword = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겹살, 국밥, 막걸리, 치맥")
with col_in2:
    st.write("#")
    generate_btn = st.button("🚀 1차 초안 생성")

# --- 프롬프트 베이스 설정 (미사여구 절대 금지 필터) ---
prompt_system = """
너는 외국인들이 한글 메뉴판을 마주했을 때 1초 만에 단어 구조를 직관적으로 깨닫게 만드는 'TastyHangul'의 힙한 글로벌 카피라이터야.

[🚫 절대 쓰지 말아야 할 AI 미사여구 (금지어)]
- sizzling, ultimate, ultimate feast, blissful, explosion, discover the magic, dive into, stepping into a world, journey 등의 뻔하고 오글거리는 마케팅 수식어는 절대 금지한다.
- 담백하고, 쿨하고, 위트 있게 팩트와 문화만 툭 던져라. 주접떨지 마라.

[💡 필수 형태소 분해 레이아웃]
- 반드시 단어를 한 글자씩 쪼개서 직관적인 뜻을 매칭할 것.
  (예: 삼 (Sam) = 3 / 겹 (Gyeop) = Layer / 살 (Sal) = Meat)
- 오프닝 훅과 엔딩 멘트는 매번 이 단어의 유래나 한국인의 리얼한 분위기에 맞게 '완전 새로' 창작해야 한다.
"""

# 1차 생성 로직
if generate_btn and keyword:
    with st.spinner(f"'{keyword}' 초안 깎는 중..."):
        prompt_x = f"{prompt_system}\n주제: {keyword}\n[지시] 위 금지어 필터를 준수하여 280자 이내의 담백하고 힙한 X(트위터) 버전 원고를 출력해라."
        prompt_threads = f"{prompt_system}\n주제: {keyword}\n[지시] 위 금지어 필터를 준수하되, 하단에 진짜 한국인들만 아는 기발하고 실용적인 '인사이더 다이닝 팁'을 2~3줄 줄바꿈하여 추가한 쓰레드 원고를 출력해라."
        
        try:
            res_x = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt_x}])
            st.session_state.text_x = res_x.choices[0].message.content
            
            res_threads = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt_threads}])
            st.session_state.text_threads = res_threads.choices[0].message.content
        except Exception as e:
            st.error(f"에러 발생: {e}")

# --- 🎯 [핵심] 대장님의 실시간 피드백 및 튜닝 섹션 ---
st.markdown("---")
st.subheader("💬 대장님의 실시간 튜닝 및 피드백 라인")
feedback = st.text_input("💡 '오프닝을 더 짧게 해줘', '좀 더 은근한 드립 쳐줘' 등 피드백을 던져보세요:", placeholder="예: 야 너무 광고 같다. 수식어 다 빼고 더 차갑고 담백하게 가자.")

if st.button("🛠️ 피드백 반영하여 원고 재수정"):
    if feedback and (st.session_state.text_x or st.session_state.text_threads):
        with st.spinner("대장님 지시 사항 접수하여 원고 재조직 중..."):
            refine_prompt = f"""
            기존에 생성된 원고가 마음에 안 든다는 브랜드 디렉터(대장님)의 긴급 피드백이 내려왔다. 
            피드백을 완벽하게 수용해서 기존 원고들을 완전히 뜯어고쳐라.
            
            [대장님의 피드백]: "{feedback}"
            
            [기존 X 원고]:\n{st.session_state.text_x}
            [기존 쓰레드 원고]:\n{st.session_state.text_threads}
            
            출력 형식은 반드시 아래 구조를 지켜라. 다른 말은 일절 하지 마라.
            [X_START]
            (수정된 X 원고 내용)
            [X_END]
            [THREADS_START]
            (수정된 쓰레드 원고 내용)
            [THREADS_END]
            """
            try:
                res_refine = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": refine_prompt}])
                result = res_refine.choices[0].message.content
                
                # 결과 파싱해서 세션에 재저장
                if "[X_START]" in result and "[X_END]" in result:
                    st.session_state.text_x = result.split("[X_START]")[1].split("[X_END]")[0].strip()
                if "[THREADS_START]" in result and "[THREADS_END]" in result:
                    st.session_state.text_threads = result.split("[THREADS_START]")[1].split("[THREADS_END]")[0].strip()
            except Exception as e:
                st.error(f"수정 중 에러 발생: {e}")

# 화면 결과 배치
col1, col2 = st.columns(2)
with col1:
    st.subheader("🦅 X (트위터) 버전")
    st.text_area("X 결과물", value=st.session_state.text_x, height=400, key="display_x")

with col2:
    st.subheader("🧵 쓰레드(Threads) 버전")
    st.text_area("쓰레드 결과물", value=st.session_state.text_threads, height=400, key="display_threads")
