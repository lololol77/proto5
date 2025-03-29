# Streamlit 기반 장애인 일자리 매칭 시스템 (수정)
import streamlit as st
import sqlite3

# DB 연결 함수
def connect_db():
    conn = sqlite3.connect("job_matching_fixed.db")
    return conn

# 구인자/구직자 입력 내역 별도 DB 연결
def connect_user_db():
    conn = sqlite3.connect("user_data.db")
    return conn

# 구인자 입력 내역 저장 함수 (일자리)
def save_job_posting(job_title, abilities):
    conn = connect_user_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS job_postings (id INTEGER PRIMARY KEY, title TEXT, abilities TEXT)")
    cur.execute("INSERT INTO job_postings (title, abilities) VALUES (?, ?)", (job_title, ", ".join(abilities)))
    conn.commit()
    conn.close()

# 구직자 입력 내역 저장 함수 (프로필)
def save_job_seeker(name, disability, severity):
    conn = connect_user_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS job_seekers (id INTEGER PRIMARY KEY, name TEXT, disability TEXT, severity TEXT)")
    cur.execute("INSERT INTO job_seekers (name, disability, severity) VALUES (?, ?, ?)", (name, disability, severity))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("장애인 일자리 매칭 시스템")

role = st.selectbox("사용자 역할 선택", ["구직자", "구인자"])

if role == "구직자":
    name = st.text_input("이름 입력")
    disability = st.selectbox("장애유형", ["시각장애", "청각장애", "지체장애", "뇌병변장애", "언어장애", "안면장애", "신장장애", "심장장애", "간장애", "호흡기장애", "장루·요루장애", "뇌전증장애", "지적장애", "자폐성장애", "정신장애"])
    severity = st.selectbox("장애 정도", ["심하지 않은", "심한"])
    if st.button("매칭 결과 보기"):
        save_job_seeker(name, disability, severity)
        conn = connect_user_db()
        cur = conn.cursor()
        cur.execute("SELECT title, abilities FROM job_postings")
        jobs = cur.fetchall()
        st.write("### 적합한 일자리 목록:")
        for job in jobs:
            # 적합도 확인
            if disability in job[1]:
                st.write(f"- {job[0]}: 적합")
            else:
                st.write(f"- {job[0]}: 적합하지 않음")
        conn.close()

elif role == "구인자":
    job_title = st.text_input("일자리 제목 입력")
    abilities = st.multiselect("필요한 능력 선택", ["주의력", "아이디어 발상 및 논리적 사고", "기억력", "지각능력", "수리능력", "공간능력", "언어능력", "지구력", "유연성 · 균형 및 조정", "체력", "움직임 통제능력", "정밀한 조작능력", "반응시간 및 속도", "청각 및 언어능력", "시각능력"])
    if st.button("매칭 결과 보기"):
        save_job_posting(job_title, abilities)
        st.success("구인자 정보가 저장되었습니다!")
        st.write("일자리 제목:", job_title)
        st.write("필요 능력:", abilities)

# 유료 서비스 여부 확인
if st.button("대화 종료"):
    if role == "구직자":
        use_service = st.radio("유료 취업준비 서비스 이용하시겠습니까?", ["네", "아니요"])
    else:
        use_service = st.radio("유료 직무개발 서비스 이용하시겠습니까?", ["네", "아니요"])
        
        if use_service == "네":
            st.write("서비스를 이용해 주셔서 감사합니다!")
        else:
            st.write("대화를 종료합니다.")

