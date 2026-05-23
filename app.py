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
st.title("🍚 TastyHangul OpenAI 기지 (Ver 9.5 - 마스터 지침서 주입형)")
st.caption("대장님의 프로젝트 지침서 전체를 주입하여, 찐 로컬 바이브와 브랜드 철학을 100% 반영합니다.")
st.markdown("---")

# =========================================================================
# 🎯 [대장님 전용] TastyHangul 프로젝트 마스터 지침서 주입 구역
# =========================================================================
PROJECT_DOCUMENTATION = """
[1. BRAND IDENTITY & CONCEPT]
- Name: TastyHangul (🍚)
- Core Concept: "Learn Hangul through Korean Food" - Helping foreigners read menus/signboards and order confidently.
- Target Audience: Global foreigners (20s-40s) interested in Korean travel, food, and culture.
- Positioning: Authentic Seoul Local insight. Fun, interactive, and practical culinary education.
- Key Brand Keywords: 
  * 식구 (Sikgu): Eating mouth = Family. Use this to address followers/community.
  * 사랑방 (Sarangbang): Guest room in traditional houses. Offline meetup name for subscribers.
  * 정 (Jeong): Deep emotional connection unique to Korea.
  * 덤 (Deom): Free service, bonus culture, local generosity.

[2. TONALITY & COPYWRITING RULES]
- Base Language: 100% ENGLISH for all body text.
- Tone & Manner: Hip, cool, and natural English. Must sound like a native speaker, completely avoiding "AI-style marketing fluff."
- Style: Deadpan, confident, objective, and minimalist. Use short, punchy sentences.
- Slangs/Phrases to Use: Naturally mix global Gen-Z/millennial구어체 like 'hits different', 'Been there', 'Nobody warned me'.
- Absolute Prohibitions (Forbidden AI Fluff): Never use cheesy adjectives like "sizzling", "cozy wrap", "testament to", "prowess", "ultimate feast", "blissful", "magical", "paradise". 
- Hook Strategy: Start with a strong, dry punch line right away. No storytelling setups like "Picture a..." or "Imagine a...".
- Closing Rule: Always end with a natural, engaging question to drive comments and trigger the algorithm (e.g., "What food should I break down next?").

[3. CHANNEL-SPECIFIC STRATEGY & LAYOUT]
- X (Twitter) Platform:
  * Character Limit: STRICTLY within 280 characters.
  * Format:
    **[Romanized Name] ([Original Korean Hangul])**
    - Breakdown: [Syllable 1] = Meaning / [Syllable 2] = Meaning
    (Body Copy - Sharp, punchy, informative)
- Threads Platform:
  * Character Limit: Within 500 characters.
  * Format: 
    **[Romanized Name] ([Original Korean Hangul])**
    - Breakdown: [Syllable 1] = Meaning / [Syllable 2] = Meaning
    (Body Copy - Slightly friendlier but still cool, conversational style)
    
    [Insider Dining Tips] (Highly practical, unwritten local rules with clean line breaks and bullet points)
    (Closing Question to drive engagement)
"""
# =========================================================================

# 🔥 마스터 지침서와 결합된 오픈AI 시스템 프롬프트 조립
prompt_system = f"""
You are the master AI copywriter and strategic partner for 'TastyHangul', working directly under the Director (대장님).
Your ultimate mission is to generate high-converting, deeply authentic social media copies based strictly on the injected project guidelines.

[📖 INJECTED MASTER GUIDELINES]
{PROJECT_DOCUMENTATION}

[🤖 MANDATE FOR GENERATION]
- Read the master documentation carefully before writing.
- Never violate the character constraints (X < 280 chars, Threads < 500 chars).
- Ensure the syllable breakdown strictly uses the Romanization and original Hangul.
- Ensure the tone is dry, cool, and filled with native slang instead of marketing clichés.
"""

# 세션 상태에 결과물 저장 공간 확보
if "final_x" not in st.session_state: st.session_state.final_x = ""
if "final_threads" not in st.session_state: st.session_state.final_threads = ""

# --- 🖥️ 입력 구역 ---
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    kw = st.text_input("📝 원하는 주제(키워드)를 입력하세요:", placeholder="예: Gukbap, Samgyeopsal, Ssamjang", key="input_keyword")
with col_in2:
    st.write("#")
    btn_draft = st.button("🚀 지침서 기반 초안 생성")

if btn_draft and kw:
    with st.spinner("주입된 마스터 지침서를 바탕으로 원고를 최적화 중..."):
        try:
            # 1. X 버전 생성
            res_x = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"Topic: {kw}\n[Instruction] Write an X copy strictly within 280 characters in ENGLISH. Follow the master blueprint. End with an engagement question if character limit allows."}
                ],
                temperature=0.7
            )
            st.session_state.final_x = res_x.choices[0].message.content

            # 2. 쓰레드 버전 생성
            res_threads = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": f"Topic: {kw}\n[Instruction] Write a Threads copy within 500 characters in ENGLISH. Include 'Insider Dining Tips' and always end with a question to drive comments as requested in the master doc."}
                ],
                temperature=0.7
            )
            st.session_state.final_threads = res_threads.choices[0].message.content
        except Exception as e:
            st.error(f"오픈AI API 통신 실패: {e}")

st.markdown("---")

# --- 🖥️ 실시간 피드백 튜닝 구역 ---
st.subheader("💬 대장님의 실시간 튜닝 및 피드백 라인")
fb = st.text_input("💡 피드백을 던져보세요:", placeholder="예: 지침서에 적힌 '정(Jeong)'의 개념을 본문에 은은하게 녹여줘.", key="input_feedback")
btn_refine = st.button("🛠️ 피드백 반영하여 원고 재수정")

if btn_refine and fb:
    if st.session_state.final_x or st.session_state.final_threads:
        with st.spinner("지침서 기준에 맞춰 도면 재튜닝 중..."):
            refine_prompt = f"""
            Completely align and rewrite the copies based on the Director's feedback and the master guidelines.
            
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

# --- 🖥️ 최종 결과물 출력 및 구글 독스 백업 구역 ---
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

if st.session_state.final_x or st.session_state.final_threads:
    st.markdown("---")
    st.subheader("💾 TastyHangul 아카이브 빽업")
    st.button("📁 이 원고들 백업 데이터셋으로 지정하기")
    st.warning("위 버튼을 누르신 후, 여기 제미나이 대화창으로 돌아오셔서 **'방금 뽑은 원고 구글 독스로 백업해줘'**라고 입력하시면 대장님의 구글 드라이브에 정식 문서가 즉시 생성됩니다.")
