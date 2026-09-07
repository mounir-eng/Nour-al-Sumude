"""لوحة الأستاذ: إضافة طلبة القسم ومتابعة تقدمهم وأوسمتهم."""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from accounts import add_student_for_teacher
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


def render_teacher_panel() -> None:
    teacher = st.session_state.get("teacher_profile") or {}
    if not teacher.get("id"):
        st.session_state["samed_role"] = None
        st.session_state["samed_view"] = "home"
        st.rerun()

    st.markdown(_CSS, unsafe_allow_html=True)
    name = teacher.get("name") or "الأستاذ"
    top, action = st.columns([4, 1])
    with top:
        st.markdown(
            f'<div class="t-head"><span><b>لوحة الأستاذ</b><small>{name} · طلبة قسمك فقط</small></span></div>',
            unsafe_allow_html=True,
        )
    with action:
        if st.button("تسجيل الخروج", use_container_width=True):
            st.session_state["teacher_profile"] = None
            st.session_state["samed_role"] = None
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

    components.html(_dashboard_html(students, name), height=880, scrolling=True)
