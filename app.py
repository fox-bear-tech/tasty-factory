import streamlit as st
from openai import OpenAI

# 1. API 클라이언트 초기화
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("스트림릿 Secrets에 'OPENAI_API_KEY'를 등록해주세요.")
    st.stop()

# --- 화면 기본 세팅 ---
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul OpenAI 엔진 기지 (Ver 5.5)")
st.caption("화면 새로고침 버그를 완전히 박살낸 직공법 엔진 레이아웃입니다.")
st.markdown("---")

# 대장님 전용 톤앤매너 프롬프트
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

# 기억 창고 초기화 (피드백 수정용)
if "x_result" not in st.session_state: st.session_state.x_result = ""
if "threads_result" not in st.session_state: st.session_state.threads_result = ""

# --- 🖥️ 1단계: 초안 생성 구역 ---
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    kw = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: 삼겹살, 국밥, 쌈장")
with col_in2:
    st.write("#")
    btn_draft = st.button("🚀 1차 초안 생성")

# [핵심 변경] 버튼이 클릭되면 '그 자리에서 즉시' 통신하고 결과를 화면에 고정
if btn_draft and kw:
    with st.spinner("GPT-4o 엔진 가동 중..."):
        try:
            # 1. X 버전 생성
            res_x = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"주제: {kw}\n[지시] 280자 이내의 담백하고 힙한 X(트위터) 버전 원고를 출력해라. 다른 잡설은 생략한다."}
                ],
                temperature=0.8
            )
            st.session_state.x_result = res_x.choices[0].message.content

            # 2. 쓰레드 버전 생성
            res_threads = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"주제: {kw}\n[지시] 하단에 진짜 한국인들만 아는 기발하고 실용적인 '인사이더 다이닝 팁'을 2~3줄 줄바꿈하여 추가한 쓰레드 원고를 출력해라. 다른 잡설은 생략한다."}
                ],
                temperature=0.8
            )
            st.session_state.threads_result = res_threads.choices[0].message.content
        except Exception as e:
            st.error(f"API 통신 에러: {e}")

st.markdown("---")

# --- 🖥️ 2단계: 실시간 피드백 튜닝 구역 ---
st.subheader("💬 대장님의 실시간 튜닝 및 피드백 라인")
fb = st.text_input("💡 피드백을 던져보세요:", placeholder="예: 완전히 힘 빼고 리얼한 동네 형 톤으로 깎아줘.")
btn_refine = st.button("🛠️ 피드백 반영하여 원고 재수정")

if btn_refine and fb:
    if st.session_state.x_result or st.session_state.threads_result:
        with st.spinner("피드백 반영하여 도면 깎는 중..."):
            refine_prompt = f"""
            브랜드 디렉터의 피드백을 완벽하게 수용해서 기존 원고들을 완전히 뜯어고쳐라.
            
            [대장님의 피드백]: "{fb}"
            [기존 X 원고]:\n{st.session_state.x_result}
            [기존 쓰레드 원고]:\n{st.session_state.threads_result}
            
            출력 형식은 반드시 아래 구조를 지켜라. 다른 설명이나 인사말은 일절 하지 마라.
            [X_START]
            (수정된 X 원고 내용)
            [X_END]
            [THREADS_START]
            (수정된 쓰레드 원고 내용)
            [THREADS_END]
            """
            try:
                res_refine = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": refine_prompt}
                    ],
                    temperature=0.7
                )
                result = res_refine.choices[0].message.content
                
                if "[X_START]" in result and "[X_END]" in result:
                    st.session_state.x_result = result.split("[X_START]")[1].split("[X_END]")[0].strip()
                if "[THREADS_START]" in result and "[THREADS_END]" in result:
                    st.session_state.threads_result = result.split("[THREADS_START]")[1].split("[THREADS_END]")[0].strip()
            except Exception as e:
                st.error(f"수정 중 에러 발생: {e}")

st.markdown("---")

# --- 🖥️ 3단계: 최종 결과물 렌더링 구역 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("🦅 X (트위터) 버전")
    st.text_area("X 결과물", value=st.session_state.x_result, height=450, key="display_x")

with col2:
    st.subheader("🧵 쓰레드(Threads) 버전")
    st.text_area("쓰레드 결과물", value=st.session_state.threads_result, height=450, key="display_threads")
