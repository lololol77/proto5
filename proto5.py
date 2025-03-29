import sqlite3
import streamlit as st

# DB 파일 경로 수정
db_path = 'job_matching_fixed.db'  # 파일이 있는 디렉토리로 경로 설정

# DB 연결
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 장애유형 데이터를 불러오기
cursor.execute("SELECT DISTINCT name FROM disabilities")
disabilities = cursor.fetchall()


# 구직자 장애유형 선택
disability_type = st.selectbox("장애유형 선택", [disability[0] for disability in disabilities])

# 구직자 장애정도 선택
disability_degree = st.radio("장애정도 선택", ["심하지 않은", "심한"])

# 구인자가 기입한 능력
required_skills = st.multiselect("구인자가 요구하는 능력", ["주의력", "기억력", "공간지각력", "아이디어 발상", "지각능력"])

# 매칭 테이블에서 해당 장애유형에 맞는 능력 상태 불러오기
cursor.execute("""
    SELECT * FROM matching WHERE disability_type = ?
""", (disability_type,))
matching_data = cursor.fetchall()

# 점수 계산 함수
def calculate_score(skills, matching_data):
    score = 0
    for skill in skills:
        for entry in matching_data:
            if entry[1] == skill:  # 능력명 일치
                if entry[2] == '○':  # 동그라미: 2점
                    score += 2
                elif entry[2] == '△':  # 세모: 1점
                    score += 1
                elif entry[2] == 'X':  # 엑스: 부적합
                    return "부적합"
    return score

# 구인자가 요구한 능력에 맞는 점수 계산
job_score = calculate_score(required_skills, matching_data)

# 결과 출력
if job_score == "부적합":
    st.write("이 일자리는 부적합입니다.")
else:
    st.write(f"추천 일자리 점수: {job_score}점")

# 예시로 일부 일자리 리스트를 작성 (DB에서 불러오는 일자리 목록을 예시로 사용)
cursor.execute("""
    SELECT job_title, required_skills FROM jobs
    WHERE disability_type = ? AND disability_degree = ?
""", (disability_type, disability_degree))

jobs = cursor.fetchall()

# 점수 높은 순으로 일자리 정렬
job_scores = {}
for job in jobs:
    job_skills = job[1].split(", ")
    score = calculate_score(required_skills, matching_data)
    job_scores[job[0]] = score

# 적합도 순으로 정렬된 일자리 목록
sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)

st.write("추천 일자리:")
for idx, job in enumerate(sorted_jobs, start=1):
    st.write(f"{idx}. {job[0]}: {job[1]}점")

# 유료 서비스 여부 확인 (구직자/구인자)
if st.button("대화 종료"):
    role = st.radio("구직자/구인자 선택", ["구직자", "구인자"])
    if role == "구직자":
        use_service = st.radio("유료 취업준비 서비스 이용하시겠습니까?", ["네", "아니요"])
    else:
        use_service = st.radio("유료 직무개발 서비스 이용하시겠습니까?", ["네", "아니요"])

    if use_service == "네":
        st.write("서비스를 이용해 주셔서 감사합니다!")
    else:
        st.write("대화를 종료합니다.")


