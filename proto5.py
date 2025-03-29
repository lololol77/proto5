import sqlite3
import streamlit as st

# DB 연결
conn = sqlite3.connect('/mnt/data/job_matching_fixed.db')
cursor = conn.cursor()

# 장애유형 데이터를 불러오기
cursor.execute("SELECT DISTINCT name FROM disabilities")
disabilities = cursor.fetchall()

# 구직자 장애유형 선택
disability_type = st.selectbox("장애유형 선택", [disability[0] for disability in disabilities])

# 구직자 장애정도 선택
disability_degree = st.radio("장애정도 선택", ["심하지 않은", "심한"])

# 해당 장애유형과 정도에 맞는 일자리 정보 불러오기
cursor.execute("""
    SELECT job_title, required_skills FROM jobs 
    WHERE disability_type = ? 
    AND disability_degree = ?
""", (disability_type, disability_degree))

jobs = cursor.fetchall()

# 장애유형 점수 계산 함수
def calculate_score(abilities):
    score = 0
    for ability in abilities:
        if ability == '○':  # 동그라미: 2점
            score += 2
        elif ability == '△':  # 세모: 1점
            score += 1
    return score

# 구직자 장애유형과 일자리 능력 매칭 점수 계산
job_scores = {job[0]: calculate_score(job[1].split(", ")) for job in jobs}

# 구직자에게 적합한 일자리 표시
sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)

st.write(f"추천 일자리 ({disability_type}, {disability_degree}):")
st.write(sorted_jobs)

# 구인자의 능력 요구 사항을 기반으로 구직자 매칭하기
required_skills = st.multiselect("필요한 능력 선택", ["주의력", "기억력", "아이디어 발상", "지각능력", "수리능력"])

# 구인자가 요구한 능력 기반으로 구직자 매칭
cursor.execute("""
    SELECT disability_type, disability_degree FROM disabilities
    WHERE skills_required LIKE ?
""", (f"%{required_skills}%",))  # 예시로 필요한 능력 기반 조회

candidates = cursor.fetchall()

# 구인자에게 적합한 구직자 표시
st.write(f"추천 구직자:")
st.write(candidates)

# 유료 서비스 여부 확인 (구직자/구인자)
if st.button("대화 종료"):
    if role == "구직자":
        use_service = st.radio("유료 취업준비 서비스 이용하시겠습니까?", ["네", "아니요"])
    else:
        use_service = st.radio("유료 직무개발 서비스 이용하시겠습니까?", ["네", "아니요"])
    
    if use_service == "네":
        st.write("서비스를 이용해 주셔서 감사합니다!")
    else:
        st.write("대화를 종료합니다.")



