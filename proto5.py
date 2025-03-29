import sqlite3
import streamlit as st

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

# 점수 계산 함수 (
