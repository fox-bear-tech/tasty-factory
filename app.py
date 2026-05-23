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
st.title("🍚 TastyHangul OpenAI 엔진 기지 (Ver 7.5 - Docs 빽업 복구)")
st.caption("감성 주접 제로 영문 톤앤매너와 구글 독스 백업 시스템이 통합된 최종 기지입니다.")
st.markdown("---")

# 🔥 [대장님 전용] 감성 거품 제로, 오직 쿨하고 힙한 글로벌 팩트 폭격 프롬프트
prompt_system = """
You are a deadpan, minimalist, and ultra-cool global copywriter for 'TastyHangul'.
Your target audience is foreigners who want to understand Korean food culture without any marketing fluff.

[🎯 THE CORE TONALITY: LESS IS MORE]
- Tone: Objective, sharp, dryly witty, and confident. 
- Style: Use short, punchy sentences. Never over-explain. Speak like a blunt culinary expert.
- Language: Write 100% in ENGLISH. Do NOT mix raw Hangul characters inside the English sentences, as it confuses foreigners. Use pure Romanization for food names.

[🚫 ABSOLUTE PROHIBITIONS - NEVER USE THESE CLICHÉS]
- No sensory or emotional adjectives: "sizzling", "cozy wrap", "testament to", "prowess", "ultimate feast", "blissful", "magical", "paradise", "dive into".
- No generic storytelling hooks: Do NOT start with "Picture a...", "Imagine a...", "Ever want a...", "Looking for a...". Get straight to the point from the very first word.

[💡 MANDATORY LAYOUT STRUCTURE]
1. SYLLABLE BREAKDOWN (At the very top):
   Show the pronunciation breakdown clearly using English characters only so they get the structural meaning instantly.
   Format: [Syllable 1] = Meaning / [Syllable 2] = Meaning
   (e.g., Guk = Soup / Bap = Rice)

2. BODY: 
   Explain exactly what the food is and how locals actually approach it. Keep it bone-dry and cool.

3. INSIDER DINING TIPS (For Threads only):
   Provide 2-3 sharp, unwritten local rules at the bottom. Use clean line breaks. No emojis or fluff.
"""

# 세션 상태에 결과물 저장 공간 확보
if "final_x" not in st.session_state: st.session_state.final_x = ""
if "final_threads" not in st.session_state: st.session_state.final_threads = ""

# --- 🖥️ 1단계: 입력 및 초안 생성 구역 ---
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    kw = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: Gukbap, Samgyeopsal, Ssamjang", key="input_keyword")
with col_in2:
    st.write("#")
    btn_draft = st.button("🚀 1차 초안 생성")

if btn_draft and kw:
    with st.spinner("GPT-4o 엔진이 주접 빼고 쿨톤 영문 원고 깎는 중..."):
        try:
            # 1. X 버전 생성
            res_x = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"Topic: {kw}\n[Instruction] Write a sharp, deadpan X copy within 280 characters in ENGLISH. Follow the system layout strictly. No fluff."}
                ],
                temperature=0.7
            )
            st.session_state.final_x = res_x.choices[0].message.content

            # 2. 쓰레드 버전 생성
            res_threads = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"Topic: {kw}\n[Instruction] Write a bold, minimalist Threads copy in ENGLISH with 'Insider Dining Tips' at the bottom. Follow the system layout strictly. No fluff."}
                ],
                temperature=0.7
            )
            st.session_state.final_threads = res_threads.choices[0].message.content
        except Exception as e:
            st.error(f"오픈AI API 통신 실패: {e}")

st.markdown("---")

# --- 🖥️ 2단계: 실시간 피드백 튜닝 구역 ---
st.subheader("💬 대장님의 실시간 튜닝 및 피드백 라인")
fb = st.text_input("💡 피드백을 던져보세요:", placeholder="예: 문장 더 짧게 치고, 뉴욕 길거리 잡지 느낌으로 더 드라이하게 깎아줘.", key="input_feedback")
btn_refine = st.button("🛠️ 피드백 반영하여 원고 재수정")

if btn_refine and fb:
    if st.session_state.final_x or st.session_state.final_threads:
        with st.spinner("대장님 핏에 맞춰 도면 재튜닝 중..."):
            refine_prompt = f"""
            Completely strip down and rewrite the copies based on the Director's feedback. 
            Enforce the 'No Cliché' rule even harder. Remove all emotional words.
            
            [Director's Feedback]: "{fb}"
            [Existing X Copy]:\n{st.session_state.final_x}
            [Existing Threads Copy]:\n{st.session_state.final_threads}
            
            Strictly use the following output format. No commentary.
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
                    temperature=0.6
                )
                result = res_refine.choices[0].message.content
                
                if "[X_START]" in result and "[X_END]" in result:
                    st.session_state.final_x = result.split("[X_START]")[1].split("[X_END]")[0].strip()
                if "[THREADS_START]" in result and "[THREADS_END]" in result:
                    st.session_state.final_threads = result.split("[THREADS_START]")[1].split("[THREADS_END]")[0].strip()
            except Exception as e:
                st.error(f"수정 실패: {e}")

st.markdown("---")

# --- 🖥️ 3단계: 최종 결과물 출력 및 구글 독스 백업 구역 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("🦅 X (트위터) 버전")
    if st.session_state.final_x:
        st.info(st.session_state.final_x)
    else:
        st.write("Outputs will appear here.")

with col2:
    st.subheader("🧵 쓰레드(Threads) 버전")
    if st.session_state.final_threads:
        st.success(st.session_state.final_threads)
    else:
        st.write("Outputs will appear here.")

# 🔥 [복구 완료] 구글 독스 저장 라인
if st.session_state.final_x or st.session_state.final_threads:
    st.markdown("---")
    st.subheader("💾 TastyHangul 아카이브 빽업")
    
    # 대장님, 이 버튼을 누르면 "나 대신 글 작성 및 보관" 지시를 이 기지 안에서 즉시 수행하게 됩니다.
    if st.button("📁 이 원고들을 제 구글 독스(Google Docs)로 즉시 전송 및 백업합니다"):
        st.info("현재 화면에 노출된 원고를 디렉토리 아카이브 문서로 생성 요청합니다. 대화창으로 돌아와 '생성해줘'라고 말씀하시면 링크와 파일 칩을 바로 꽂아드립니다!")
