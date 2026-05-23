import streamlit as st
from openai import OpenAI
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- [초기 설정] ---
st.set_page_config(page_title="TastyHangul", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- [핵심 지침: 한국어 금지 및 스타일 강제] ---
PROMPT_FORCE = """
You are 'TastyHangul'. 
Respond ONLY in English. 
Never use Korean in the body, except for the required Hangul word itself.
Follow this structure:
- X: [Name] ([Hangul]) | Breakdown: [Syllable]=Meaning / ... | (Raw vibe, 2 sentences)
- Threads: [Name] ([Hangul]) | Breakdown: ... | (Cool narrative + 1 witty tip)
"""

# --- [백업 로직] ---
def save_to_drive(content):
    creds = Credentials.from_service_account_info(st.secrets["google_credentials"], 
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"])
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().create(body={"title": "TastyHangul Archive"}).execute()
    docs.documents().batchUpdate(documentId=doc.get("documentId"), 
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}).execute()
    return f"https://docs.google.com/document/d/{doc.get('documentId')}/edit"

# --- [앱 화면] ---
st.title("🍚 TastyHangul")
kw = st.text_input("Topic:")

if st.button("Generate"):
    # 강제 지침 적용
    res = client.chat.completions.create(model="gpt-4o", messages=[
        {"role": "system", "content": PROMPT_FORCE},
        {"role": "user", "content": f"Topic: {kw}"}
    ])
    st.session_state.res = res.choices[0].message.content

if "res" in st.session_state:
    st.write(st.session_state.res)
    if st.button("Save to Google Docs"):
        url = save_to_drive(st.session_state.res)
        st.success(f"Archived: {url}")
