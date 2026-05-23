import streamlit as st
from openai import OpenAI

# 1. API 클라이언트 초기화
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("스트림릿 Secrets에 'OPENAI_API_KEY'가 등록되어 있지 않습니다.")
    st.stop()

# --- 화면 기본 세팅 ---
st.set_page_config(page_title="TastyHangul 기지", page_icon="🍚", layout="wide")
st.title("🍚 TastyHangul OpenAI 엔진 기지 (Ver 6.5)")
st.caption("글로벌 타겟 맞춤형! 무조건 영어(English)로 카피를 뽑아내는 버전입니다.")
st.markdown("---")

# 🔥 [글로벌 맞춤형] 대장님 전용 영문 출력 톤앤매너 프롬프트
prompt_system = """
You are a hip, global copywriter for 'TastyHangul', a brand that helps foreigners intuitively understand Korean food menus and dining culture.

[🎯 CRITICAL MANDATE: LANGUAGE]
- You MUST write all opening, body, and closing sentences entirely in ENGUSH.
- The target audience is foreigners who do not know Korean.

[🚫 FORBIDDEN WORDS]
- Never use cheesy, over-the-top marketing clichés like: "sizzling", "ultimate", "ultimate feast", "blissful", "explosion", "discover the magic", "dive into", "stepping into a world", "journey", etc.
- Keep the tone cool, calm, witty, and factual. Do not hype it up.

[💡 REQUIRED LAYOUT]
- You MUST break down the Korean name syllable by syllable to show its direct meaning.
  (e.g., Sam (Sam) = 3 / Gyeop (Gyeop) = Layer / Sal (Sal) = Meat)
- Never fix or reuse the opening and closing remarks. Completely reinvent them every time based on the specific food's origin, history, or the real, authentic atmosphere of Korean local diners.
"""

# 세션 상태에 결과물 저장 공간 확보
if "final_x" not in st.session_state: st.session_state.final_x = ""
if "final_threads" not in st.session_state: st.session_state.final_threads = ""

# --- 🖥️ 입력 구역 ---
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    kw = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: Samgyeopsal, 삼겹살, 국밥, 쌈장", key="input_keyword")
with col_in2:
    st.write("#")
    btn_draft = st.button("🚀 1차 초안 생성")

# 초안 생성 버튼 클릭 시 작동
if btn_draft and kw:
    with st.spinner("GPT-4o가 영문 원고를 작성 중입니다..."):
        try:
            # 1. X 버전 생성
            res_x = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"Topic: {kw}\n[Instruction] Write a cool, concise X (Twitter) copy within 280 characters in ENGLISH. Do not include any other commentary."}
                ],
                temperature=0.8
            )
            st.session_state.final_x = res_x.choices[0].message.content

            # 2. 쓰레드 버전 생성
            res_threads = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"Topic: {kw}\n[Instruction] Write a Threads copy in ENGLISH. At the bottom, add 2-3 lines of witty and highly practical 'Insider Dining Tips' that only real Koreans know (use line breaks). Do not include any other commentary."}
                ],
                temperature=0.8
            )
            st.session_state.final_threads = res_threads.choices[0].message.content
        except Exception as e:
            st.error(f"오픈AI API 통신 실패: {e}")

st.markdown("---")

# --- 🖥️ 실시간 피드백 튜닝 구역 ---
st.subheader("💬 대장님의 실시간 튜닝 및 피드백 라인")
fb = st.text_input("💡 피드백을 던져보세요 (한글로 편하게 적으셔도 됩니다):", placeholder="예: 좀 더 미국 브루클린 형들이 쓸 법한 힙한 슬랭을 섞어줘.", key="input_feedback")
btn_refine = st.button("🛠️ 피드백 반영하여 원고 재수정")

if btn_refine and fb:
    if st.session_state.final_x or st.session_state.final_threads:
        with st.spinner("대장님 피드백 반영하여 영문 도면 다시 깎는 중..."):
            refine_prompt = f"""
            Completely rewrite the existing English copies based on the Brand Director's feedback below.
            Maintain the core system rules (write in English, break down syllables, no clichés).
            
            [Director's Feedback]: "{fb}"
            [Existing X Copy]:\n{st.session_state.final_x}
            [Existing Threads Copy]:\n{st.session_state.final_threads}
            
            Strictly use the following output format. Do not write any other introduction or conclusion.
            [X_START]
            (Revised English X copy)
            [X_END]
            [THREADS_START]
            (Revised English Threads copy)
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
                    st.session_state.final_x = result.split("[X_START]")[1].split("[X_END]")[0].strip()
                if "[THREADS_START]" in result and "[THREADS_END]" in result:
                    st.session_state.final_threads = result.split("[THREADS_START]")[1].split("[THREADS_END]")[0].strip()
            except Exception as e:
                st.error(f"수정 실패: {e}")

st.markdown("---")

# --- 🖥️ 최종 결과물 출력 구역 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("🦅 X (트위터) 버전")
    if st.session_state.final_x:
        st.info(st.session_state.final_x)
    else:
        st.write("Outputs will appear here in English once generated.")

with col2:
    st.subheader("🧵 쓰레드(Threads) 버전")
    if st.session_state.final_threads:
        st.success(st.session_state.final_threads)
    else:
        st.write("Outputs will appear here in English once generated.")
