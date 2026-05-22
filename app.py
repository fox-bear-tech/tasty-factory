import streamlit as st
import anthropic  # OpenAI 대신 Anthropic 라이브러리 탑재!

# 1. Claude API 열쇠 세팅
# 스트림릿 클라우드 세팅의 Secrets에 ANTHROPIC_API_KEY가 등록되어 있어야 합니다.
api_key = st.secrets["ANTHROPIC_API_KEY"]
client = anthropic.Anthropic(api_key=api_key)

st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul 클로드 엔진 기지 (Ver 5.0)")
st.caption("인간적인 톤앤매너의 최강자, Claude 3.5 Sonnet으로 심장을 완전히 교체했습니다.")

st.markdown("---")

# [보안관 변수] 기억 창고 세팅 (화면 새로고침 시 데이터 증발 방지)
if "text_x" not in st.session_state:
    st.session_state.text_x = ""
if "text_threads" not in st.session_state:
    st.session_state.text_threads = ""

# Claude 전용 고정 프롬프트 뼈대
prompt_system = """
너는 외국인들이 한글 메뉴판을 마주했을 때 1초 만에 단어 구조를 직관적으로 깨닫게 만드는 'TastyHangul'의 힙한 글로벌 카피라이터야.

[🚫 절대 금지 수식어]
- sizzling, ultimate, ultimate feast, blissful, explosion, discover the magic, dive into, stepping into a world, journey 등 오글거리는 광고성 미사여구 절대 금지.
- 주접떨지 말고 담백하고, 쿨하고, 위트 있게 팩트와 문화만 툭 던져라. 과장하지 마라.

[💡 필수 레이아웃]
- 반드시 단어를 한 글자씩 쪼개서 직관적인 뜻을 매칭할 것.
  (예: 삼 (Sam) = 3 / 겹 (Gyeop) = Layer / 살 (Sal) = Meat)
- 오프닝과 엔딩 멘트는 고정하지 말고, 매번 이 단어의 유래나 한국인의 리얼한 분위기에 맞게 완전 새로 담백하게 창작해라.
"""

# 🎯 [콜백 함수 1] Claude 3.5 Sonnet 기반 1차 초안 생성
def generate_draft():
    kw = st.session_state.input_keyword
    if kw:
        try:
            # 1. X(트위터) 버전 생성
            res_x = client.messages.create(
                model="claude-3-5-sonnet-20241022",  # 클로드 최신 플래그십 모델
                max_tokens=1000,
                system=prompt_system,
                messages=[{"role": "user", "content": f"주제: {kw}\n[지시] 280자 이내의 담백하고 힙한 X(트위터) 버전 원고를 출력해라. 다른 잡설은 생략한다."}]
            )
            st.session_state.text_x = res_x.content[0].text
            
            # 2. 쓰레드 버전 생성
            res_threads = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=prompt_system,
                messages=[{"role": "user", "content": f"주제: {kw}\n[지시] 하단에 진짜 한국인들만 아는 기발하고 실용적인 '인사이더 다이닝 팁'을 2~3줄 줄바꿈하여 추가한 쓰레드 원고를 출력해라. 다른 잡설은 생략한다."}]
            )
            st.session_state.text_threads = res_threads.content[0].text
            
        except Exception as e:
            st.error(f"클로드 API 에러: {e}")

# 🎯 [콜백 함수 2] Claude 기반 피드백 반영 및 원고 재수정
def refine_draft():
    fb = st.session_state.input_feedback
    if fb and (st.session_state.text_x or st.session_state.text_threads):
        refine_prompt = f"""
        브랜드 디렉터의 피드백을 완벽하게 수용해서 기존 원고들을 완전히 뜯어고쳐라.
        
        [대장님의 피드백]: "{fb}"
        [기존 X 원고]:\n{st.session_state.text_x}
        [기존 쓰레드 원고]:\n{st.session_state.text_threads}
        
        출력 형식은 반드시 아래 구조를 지켜라. 다른 설명이나 인사말은 일절 하지 마라.
        [X_START]
        (수정된 X 원고 내용)
        [X_END]
        [THREADS_START]
        (수정된 쓰레드 원고 내용)
        [THREADS_END]
        """
        try:
            res_refine = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                system=prompt_system,
                messages=[{"role": "user", "content": refine_prompt}]
            )
            result = res_refine.content[0].text
            
            if "[X_START]" in result and "[X_END]" in result:
                st.session_state.text_x = result.split("[X_START]")[1].split("[X_END]")[0].strip()
            if "[THREADS_START]" in result and "[THREADS_END]" in result:
                st.session_state.text_threads = result.split("[THREADS_START]")[1].split("[THREADS_END]")[0].strip()
        except Exception as e:
            st.error(f"수정 중 에러 발생: {e}")

# --- 🖥️ 화면 레이아웃 렌더링 ---
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겹살, 국밥, 쌈장", key="input_keyword")
with col_in2:
    st.write("#")
    st.button("🚀 1차 초안 생성", on_click=generate_draft)

st.markdown("---")

st.subheader("💬 대장님의 실시간 튜닝 및 피드백 라인")
st.text_input("💡 피드백을 던져보세요:", placeholder="예: 완전히 힘 빼고 리얼한 동네 형 톤으로 깎아줘.", key="input_feedback")
st.button("🛠️ 피드백 반영하여 원고 재수정", on_click=refine_draft)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🦅 X (트위터) 버전")
    st.text_area("X 결과물", value=st.session_state.text_x, height=450, key="display_x")

with col2:
    st.subheader("🧵 쓰레드(Threads) 버전")
    st.text_area("쓰레드 결과물", value=st.session_state.text_threads, height=450, key="display_threads")
