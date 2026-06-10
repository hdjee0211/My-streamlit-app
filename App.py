import streamlit as st
import pandas as pd

st.title("📚 고등학교 내신 등급 계산기")

grade_to_point = {
    "1등급": 1, "2등급": 2, "3등급": 3, "4등급": 4, "5등급": 5
}

if "subjects" not in st.session_state:
    st.session_state.subjects = []

st.subheader("과목 추가")

col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
with col1:
    name = st.text_input("과목명", key="name")
with col2:
    credit = st.number_input("단위수", min_value=1, max_value=10, value=3, key="credit")
with col3:
    grade = st.selectbox("등급", list(grade_to_point.keys()), key="grade")
with col4:
    semester = st.selectbox("학기", ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2"], key="semester")

if st.button("추가"):
    if name:
        st.session_state.subjects.append({
            "학기": semester,
            "과목명": name,
            "단위수": credit,
            "등급": grade,
            "등급점수": grade_to_point[grade]
        })

if st.session_state.subjects:
    df = pd.DataFrame(st.session_state.subjects)

    total_credit = sum(s["단위수"] for s in st.session_state.subjects)
    total_weighted = sum(s["단위수"] * s["등급점수"] for s in st.session_state.subjects)
    overall_avg = total_weighted / total_credit

    st.subheader("📊 전체 합산")
    col1, col2 = st.columns(2)
    col1.metric("총 이수단위", f"{total_credit}단위")
    col2.metric("평균 등급", f"{overall_avg:.2f}등급")

    st.subheader("📅 학기별 평균 등급")
    for sem in sorted(df["학기"].unique()):
        sem_df = df[df["학기"] == sem]
        sem_credit = sem_df["단위수"].sum()
        sem_weighted = (sem_df["단위수"] * sem_df["등급점수"]).sum()
        sem_avg = sem_weighted / sem_credit
        st.markdown(f"**{sem}학기** — 평균 {sem_avg:.2f}등급 ({sem_credit}단위)")
        st.dataframe(sem_df[["과목명", "단위수", "등급"]].reset_index(drop=True), use_container_width=True)

    if st.button("전체 초기화"):
        st.session_state.subjects = []
        st.rerun()
