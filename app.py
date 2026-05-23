import streamlit as st
from openai import OpenAI
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- [초기 설정] ---
st.set_page_config(page_title="TastyHangul Simple", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- [구글 독스 저장 함수] ---
def save_to_drive(content):
    creds = Credentials.from_service_account_info(st.secrets["google_credentials"], 
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"])
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().create(body={"title": "TastyHangul Archive"}).execute()
    docs.documents().batchUpdate(documentId=doc.get("documentId"), 
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}).execute()
    return f"https://docs.google.com/document/d/{doc.get('documentId')}/edit"

# --- [화면 구성] ---
st.title("🍚 TastyHangul 단순 아카이브")
kw = st.text_input("주제(단어) 입력:")

if st.button("생성"):
    # 최대한 단순하게 구조만 잡도록 지시
    prompt = f"'{kw}'에 대해 TastyHangul 스타일로 X(280자 내)와 Threads(500자 내) 콘텐츠를 구조(Breakdown/Insider Tips)에 맞춰 작성해줘."
    res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    st.session_state.res = res.choices[0].message.content

if "res" in st.session_state:
    st.write(st.session_state.res)
    if st.button("구글 독스에 저장"):
        url = save_to_drive(st.session_state.res)
        st.success(f"저장 완료: {url}")
