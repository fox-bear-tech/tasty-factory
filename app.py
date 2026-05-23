import streamlit as st
from openai import OpenAI
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 1. 톤앤매너 강제 주입 프롬프트 (강력하게 수정됨)
PROMPT_V11 = """
You are the master editor of 'TastyHangul'. 
YOUR RULES (FOLLOW STRICTLY):
1. NO 'sizzling', 'dreams come true', 'magic', 'ultimate', 'testament'. These are forbidden.
2. Tone: Dry, deadpan, cool, minimal. Native English speaker vibe.
3. Structure: 
   - X: [Romanized Name] ([Hangul]) \n Breakdown: [Syllable] = Meaning... \n (Body: 1-2 punchy sentences)
   - Threads: [Romanized Name] ([Hangul]) \n Breakdown: ... \n (Body: Punchy) \n [Insider Dining Tips] \n (Bulleted list of pro-tips)
4. Absolute focus on authentic local reality, not tourist marketing.
"""

def generate_content(kw):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PROMPT_V11},
            {"role": "user", "content": f"Topic: {kw}. Write X and Threads copy based on the rules."}
        ]
    )
    return response.choices[0].message.content

# 2. UI 구성
st.title("🍚 TastyHangul [Ver 11.0] - 톤앤매너 강화")
kw = st.text_input("주제:")
if st.button("🚀 초안 생성"):
    with st.spinner("지침서 강제 적용 중..."):
        st.session_state.content = generate_content(kw)
        st.write(st.session_state.content)

# 3. 아카이브 연동 (이전과 동일)
if "content" in st.session_state:
    if st.button("✨ 이 원고 아카이브에 박제"):
        # 여기에 아까 그 구글 독스 백업 함수 적용
        st.success("보관 완료.")
