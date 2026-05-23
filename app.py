import streamlit as st
from openai import OpenAI
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 1. 초기 세팅
st.set_page_config(page_title="TastyHangul HQ", page_icon="🍚", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. 구글 독스 백업 함수 (고속 전송)
def save_to_drive(content):
    creds = Credentials.from_service_account_info(st.secrets["google_credentials"], 
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"])
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().create(body={"title": "TastyHangul Archive"}).execute()
    docs.documents().batchUpdate(documentId=doc.get("documentId"), 
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}).execute()
    return f"https://docs.google.com/document/d/{doc.get('documentId')}/edit"

# 3. 마스터 지침서 (톤앤매너 내장)
PROMPT_MASTER = """당신은 'TastyHangul'의 대장님 전용 카피라이터입니다.
- 100% 영어, 힙하고 자연스러운 네이티브 구어체.
- 마케팅 플러프(Fluff) 금지, 직관적이고 펀치감 있는 문장.
- X(280자) / Threads(500자) 제약 엄수.
- Insider Dining Tips는 무조건 포함."""

# 4. 화면 구성
st.title("🍚 TastyHangul [Ver 10.0] - 무인 아카이브 시스템")
kw = st.text_input("📝 주제 입력:", placeholder="예: Samgyeopsal")

if st.button("🚀 초안 생성"):
    with st.spinner("마스터 지침서 적용 중..."):
        res = client.chat.completions.create(model="gpt-4o", messages=[
            {"role": "system", "content": PROMPT_MASTER},
            {"role": "user", "content": f"Topic: {kw}. X버전과 Threads버전(팁 포함)을 작성해줘."}
        ])
        st.session_state.res = res.choices[0].message.content
        st.write(st.session_state.res)

# 5. 아카이브 버튼 (버전 10의 핵심)
if "res" in st.session_state:
    if st.button("✨ 이 원고를 아카이브에 영구 보관하기"):
        with st.spinner("아카이브 전송 중..."):
            url = save_to_drive(st.session_state.res)
            st.success(f"보관 완료! [확인하기]({url})")
