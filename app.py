import streamlit as st
from openai import OpenAI
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- 1. 설정 및 초기화 ---
st.set_page_config(page_title="TastyHangul HQ", page_icon="🍚", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 2. 브랜드 지침서 (Tone & Manner 강화형) ---
PROMPT_V12 = """
You are the master editor of 'TastyHangul'. 
YOUR MISSION: Write social media copies that sound like a cool Seoul local talking to a foreign friend.

[TONE RULES - CRITICAL]
- DEADPAN & COOL: Use slang, be brief. No textbook explanations or marketing fluff.
- FORBIDDEN: NEVER use 'means', 'is defined as', 'variety of textures', 'perfect', 'sizzling', 'dreams come true', 'ultimate', 'magical'.
- STYLE: Punchy. Use phrases like 'hits different', 'Game changer', 'Nobody warned me', 'Trust me'.
- FORMAT: Follow the structure below strictly.

[STRUCTURE]
- X: [Romanized Name] ([Hangul]) \n Breakdown: [Syllable 1] = Meaning / [Syllable 2] = Meaning \n (Raw, punchy body copy)
- Threads: [Romanized Name] ([Hangul]) \n Breakdown: [Syllable 1] = Meaning / [Syllable 2] = Meaning \n (Cool body copy) \n [Insider Dining Tips] \n (Bulleted list of punchy pro-tips ending with a question)
"""

# --- 3. 구글 독스 백업 함수 ---
def save_to_drive(content):
    creds = Credentials.from_service_account_info(st.secrets["google_credentials"], 
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"])
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().create(body={"title": "TastyHangul Archive"}).execute()
    docs.documents().batchUpdate(documentId=doc.get("documentId"), 
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}).execute()
    return f"https://docs.google.com/document/d/{doc.get('documentId')}/edit"

# --- 4. 메인 화면 및 로직 ---
st.title("🍚 TastyHangul [Ver 12.0] - 무인 아카이브 시스템")
kw = st.text_input("📝 주제 입력:", placeholder="예: Samgyeopsal")

if st.button("🚀 초안 생성"):
    with st.spinner("지침서 강제 적용 중..."):
        res = client.chat.completions.create(model="gpt-4o", messages=[
            {"role": "system", "content": PROMPT_V12},
            {"role": "user", "content": f"Topic: {kw}. Write X and Threads copy based on the rules."}
        ])
        st.session_state.res = res.choices[0].message.content

if "res" in st.session_state:
    st.markdown("---")
    st.write(st.session_state.res)
    if st.button("✨ 이 원고 아카이브에 영구 박제"):
        with st.spinner("아카이브 전송 중..."):
            url = save_to_drive(st.session_state.res)
            st.success(f"보관 완료! [확인하기]({url})")
