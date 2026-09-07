"""لوحة الأستاذ: إضافة طلبة القسم ومتابعة تقدمهم وأوسمتهم."""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from accounts import add_student_for_teacher, reset_student_password
from student_cloud_sync import is_configured, list_students

_CSS = """
<style id="samed-teacher-panel">
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f7f8f6!important;color:#173b3d!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{max-width:1280px!important;padding:16px 14px 24px!important}
.t-head{display:flex;justify-content:space-between;gap:12px;align-items:center;background:#173f44;color:#fff;border-radius:16px;padding:14px 16px;margin-bottom:14px}
.t-head b{display:block;font-size:18px}
.t-head small{display:block;color:#d6e7e4;font-size:12px;margin-top:2px}
.t-card{background:#fff;border:1px solid #dce6e3;border-radius:16px;padding:16px;margin-bottom:14px}
</style>
"""


def _dashboard_html(students: list[dict], teacher_name: str) -> str:
    html_path = Path(__file__).with_name("admin_dashboard.html")
    html = html_path.read_text(encoding="utf-8")
    payload = json.dumps(students, ensure_ascii=False)
    inject = (
        f"window.SAMED_LIVE=true;window.SAMED_ROLE='teacher';"
        f"window.SAMED_TEACHER_NAME={json.dumps(teacher_name, ensure_ascii=False)};"
        f"window.SAMED_STUDENTS={payload};"
    )
    return html.replace("/*__STUDENTS_INJECT__*/", inject)


def _open_learning(teacher: dict) -> None:
    st.session_state["samed_teacher_learn"] = True
    st.session_state["samed_role"] = "teacher"
    st.session_state["samed_view"] = "dashboard"
    st.session_state["student_profile"] = {
        "id": "tchlearn-" + str(teacher.get("id") or ""),
        "name": teacher.get("name") or "الأستاذ",
        "grade": 12,
        "subjects": ["phys", "chem"],
        "teacher_id": teacher.get("id"),
        "mode": "teacher_preview",
    }
    st.session_state["student_name"] = teacher.get("name") or "الأستاذ"
    st.rerun()


def render_teacher_panel() -> None:
    teacher = st.session_state.get("teacher_profile") or {}
    if not teacher.get("id"):
        st.session_state["samed_role"] = None
        st.session_state["samed_view"] = "home"
        st.rerun()

    st.markdown(_CSS, unsafe_allow_html=True)
    name = teacher.get("name") or "الأستاذ"
    st.markdown(
        f'<div class="t-head"><span><b>لوحة الأستاذ</b><small>{name} · طلبة قسمك فقط</small></span></div>',
        unsafe_allow_html=True,
    )
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("المحتوى التعليمي", type="primary", use_container_width=True):
            _open_learning(teacher)
    with b2:
        st.caption("كلمات المرور لا تُعرض. عيّن كلمة جديدة للطالب إن نسيها.")
    with b3:
        if st.button("تسجيل الخروج", use_container_width=True):
            st.session_state["teacher_profile"] = None
            st.session_state["samed_role"] = None
            st.session_state["samed_teacher_learn"] = False
            st.session_state["samed_view"] = "home"
            st.rerun()

    st.markdown('<div class="t-card">', unsafe_allow_html=True)
    st.subheader("إضافة طالب إلى القسم")
    st.caption("عيّن اسم الطالب وكلمة المرور ثم أعطه هذه البيانات لتسجيل الدخول.")
    with st.form("add_student_form"):
        c1, c2 = st.columns(2)
        with c1:
            student_name = st.text_input("اسم الطالب")
            grade = st.selectbox("الصف الدراسي", list(range(6, 13)), index=6)
        with c2:
            password = st.text_input("كلمة مرور الطالب", type="password")
            confirm = st.text_input("تأكيد كلمة المرور", type="password")
        subjects = st.multiselect("المواد", ["فيزياء", "كيمياء"], default=["فيزياء", "كيمياء"])
        submitted = st.form_submit_button("إضافة الطالب", type="primary", use_container_width=True)
    if submitted:
        mapped = []
        if "فيزياء" in subjects:
            mapped.append("phys")
        if "كيمياء" in subjects:
            mapped.append("chem")
        ok, message = add_student_for_teacher(teacher["id"], student_name, int(grade), mapped or ["phys"], password, confirm)
        if ok:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
    st.markdown("</div>", unsafe_allow_html=True)

    students: list[dict] = []
    if is_configured():
        try:
            students = list_students(teacher_id=str(teacher["id"]))
        except Exception as exc:
            st.error("تعذر قراءة طلبة القسم من Google Sheets.")
            st.caption(str(exc)[:240])
    else:
        st.warning("اربط Google Sheets ليظهر طلبة قسمك هنا.")

    st.markdown('<div class="t-card">', unsafe_allow_html=True)
    st.subheader("إعادة ضبط كلمة مرور طالب")
    st.caption("لا تُحفظ كلمة المرور كنص ولا تظهر في اللوحة. أعطِ الطالب الكلمة الجديدة مباشرة.")
    if students:
        labels = {f"{s.get('name')} ({s.get('id')})": str(s.get("id")) for s in students}
        with st.form("reset_student_form"):
            chosen = st.selectbox("الطالب", list(labels.keys()))
            new_pw = st.text_input("كلمة المرور الجديدة", type="password")
            new_cf = st.text_input("تأكيد كلمة المرور", type="password")
            reset_ok = st.form_submit_button("ضبط كلمة المرور", use_container_width=True)
        if reset_ok:
            ok, message = reset_student_password(str(teacher["id"]), labels[chosen], new_pw, new_cf)
            if ok:
                st.success(message)
            else:
                st.error(message)
    else:
        st.caption("أضف طلبة أولًا لإعادة ضبط كلمات مرورهم.")
    st.markdown("</div>", unsafe_allow_html=True)

    components.html(_dashboard_html(students, name), height=880, scrolling=True)
