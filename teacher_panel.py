"""لوحة الأستاذ: متابعة القسم، وإدارة الطلبة من شاشة مستقلة."""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from accounts import add_student_for_teacher, reset_student_password
from student_cloud_sync import is_configured, list_students

_CSS = """
<style id="samed-teacher-panel-v2">
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f4f7f6!important;color:#173b3d!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{max-width:1180px!important;padding:18px 16px 28px!important}
.tp-hero{display:flex;justify-content:space-between;gap:16px;align-items:center;background:linear-gradient(135deg,#173f44,#245e65 62%,#347d78);color:#fff;border-radius:22px;padding:20px 22px;margin-bottom:16px;box-shadow:0 16px 36px rgba(23,63,68,.16)}
.tp-hero b{display:block;font-size:22px;line-height:1.4}
.tp-hero small{display:block;color:#d6e7e4;font-size:12px;margin-top:4px}
.tp-mark{width:52px;height:52px;border-radius:16px;display:grid;place-items:center;background:rgba(255,255,255,.12);font-size:24px;flex:0 0 auto}
.tp-add{width:52px;height:52px;border-radius:16px;border:1px dashed rgba(255,255,255,.45);background:rgba(255,255,255,.12);color:#fff;font-size:28px;line-height:1;display:grid;place-items:center}
.tp-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0 0 16px}
.tp-kpi{background:#fff;border:1px solid #dce6e3;border-radius:18px;padding:16px 18px;box-shadow:0 8px 22px rgba(23,63,68,.05)}
.tp-kpi span{display:block;color:#6f827e;font-size:12px;font-weight:800}
.tp-kpi b{display:block;font-size:28px;margin-top:4px;color:#173f44}
.tp-card{background:#fff;border:1px solid #dce6e3;border-radius:20px;padding:18px 18px 8px;margin-bottom:14px;box-shadow:0 8px 22px rgba(23,63,68,.05)}
.tp-card h3{margin:0 0 4px;font-size:18px}
.tp-card p{margin:0 0 12px;color:#6f827e;font-size:13px;line-height:1.8}
.stButton>button{border-radius:12px!important;min-height:44px!important;font-weight:800!important}
.stFormSubmitButton>button{background:#173f44!important;color:#fff!important;border:0!important;border-radius:12px!important;min-height:46px!important}
@media(max-width:800px){.tp-hero{display:grid}.tp-kpis{grid-template-columns:1fr}}
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
    st.session_state["teacher_panel_view"] = "home"
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


def _logout() -> None:
    for key in ("student_profile", "teacher_profile", "samed_role", "student_name"):
        st.session_state[key] = None
    st.session_state["samed_teacher_learn"] = False
    st.session_state["teacher_panel_view"] = "home"
    st.session_state["samed_view"] = "home"
    st.rerun()


def _class_stats(students: list[dict]) -> tuple[int, int, int]:
    count = len(students)
    if not count:
        return 0, 0, 0
    progress = 0
    badges = 0
    for row in students:
        try:
            progress += int(row.get("progress") or 0)
        except (TypeError, ValueError):
            pass
        raw = row.get("badges") or []
        if isinstance(raw, str):
            badges += len([part for part in raw.replace("،", ",").split(",") if part.strip()])
        elif isinstance(raw, list):
            badges += len(raw)
    return count, int(round(progress / count)), badges


def _render_manage(teacher: dict, students: list[dict]) -> None:
    st.markdown('<div class="tp-card">', unsafe_allow_html=True)
    st.markdown("<h3>إضافة طالب جديد</h3><p>عيّن الاسم وكلمة المرور ثم أعطه البيانات سرًا. لا تظهر كلمات المرور لاحقًا.</p>", unsafe_allow_html=True)
    with st.form("add_student_form"):
        c1, c2 = st.columns(2)
        with c1:
            student_name = st.text_input("اسم الطالب")
            grade = st.selectbox("الصف الدراسي", list(range(6, 13)), index=6)
        with c2:
            password = st.text_input("كلمة مرور الطالب", type="password")
            confirm = st.text_input("تأكيد كلمة المرور", type="password")
        subjects = st.multiselect("المواد", ["فيزياء", "كيمياء"], default=["فيزياء", "كيمياء"])
        submitted = st.form_submit_button("حفظ الطالب", type="primary", use_container_width=True)
    if submitted:
        mapped = []
        if "فيزياء" in subjects:
            mapped.append("phys")
        if "كيمياء" in subjects:
            mapped.append("chem")
        ok, message = add_student_for_teacher(teacher["id"], student_name, int(grade), mapped or ["phys"], password, confirm)
        if ok:
            st.success(message)
            st.session_state["teacher_panel_view"] = "home"
            st.rerun()
        else:
            st.error(message)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tp-card">', unsafe_allow_html=True)
    st.markdown("<h3>تغيير كلمة مرور طالب</h3><p>اختر الطالب وعيّن كلمة جديدة. أعطِه الكلمة مباشرة، فهي لا تُعرض في اللوحة.</p>", unsafe_allow_html=True)
    if students:
        labels = {str(s.get("name") or s.get("id")): str(s.get("id")) for s in students}
        with st.form("reset_student_form"):
            chosen = st.selectbox("الطالب", list(labels.keys()))
            new_pw = st.text_input("كلمة المرور الجديدة", type="password")
            new_cf = st.text_input("تأكيد كلمة المرور", type="password")
            reset_ok = st.form_submit_button("حفظ الكلمة الجديدة", use_container_width=True)
        if reset_ok:
            ok, message = reset_student_password(str(teacher["id"]), labels[chosen], new_pw, new_cf)
            if ok:
                st.success(message)
            else:
                st.error(message)
    else:
        st.caption("لا يوجد طلبة بعد. أضف طالبًا أولًا.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_teacher_panel() -> None:
    teacher = st.session_state.get("teacher_profile") or {}
    if not teacher.get("id"):
        st.session_state["samed_role"] = None
        st.session_state["samed_view"] = "home"
        st.rerun()

    if "teacher_panel_view" not in st.session_state:
        st.session_state["teacher_panel_view"] = "home"

    st.markdown(_CSS, unsafe_allow_html=True)
    name = teacher.get("name") or "الأستاذ"
    view = st.session_state.get("teacher_panel_view") or "home"

    students: list[dict] = []
    if is_configured():
        try:
            students = list_students(teacher_id=str(teacher["id"]))
        except Exception as exc:
            st.error("تعذر قراءة طلبة القسم من Google Sheets.")
            st.caption(str(exc)[:240])
    else:
        st.warning("اربط Google Sheets ليظهر طلبة قسمك هنا.")

    count, avg, badges = _class_stats(students)
    if view == "manage":
        st.markdown(
            f'<div class="tp-hero"><div style="display:flex;gap:14px;align-items:center">'
            f'<span class="tp-mark">⚙️</span><span><b>إعدادات القسم</b><small>{name} · إضافة طالب أو تغيير كلمة المرور</small></span></div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="tp-hero"><div style="display:flex;gap:14px;align-items:center">'
            f'<span class="tp-mark">🛡️</span><span><b>لوحة الأستاذ</b><small>{name} · متابعة قسمك فقط</small></span></div></div>',
            unsafe_allow_html=True,
        )

    if view == "home":
        a1, a2, a3, a4, a5 = st.columns([1.4, 0.7, 1.1, 1, 1])
        with a1:
            if st.button("📚 المحتوى التعليمي", type="primary", use_container_width=True):
                _open_learning(teacher)
        with a2:
            if st.button("➕", help="إضافة طالب", use_container_width=True):
                st.session_state["teacher_panel_view"] = "manage"
                st.rerun()
        with a3:
            if st.button("إعدادات القسم", use_container_width=True):
                st.session_state["teacher_panel_view"] = "manage"
                st.rerun()
        with a4:
            if st.button("الرئيسية", use_container_width=True):
                st.session_state["samed_view"] = "home"
                st.rerun()
        with a5:
            if st.button("تسجيل الخروج", use_container_width=True):
                _logout()
    else:
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("→ عودة للوحة الأستاذ", type="primary", use_container_width=True):
                st.session_state["teacher_panel_view"] = "home"
                st.rerun()
        with b2:
            if st.button("الرئيسية", use_container_width=True):
                st.session_state["samed_view"] = "home"
                st.rerun()
        with b3:
            if st.button("تسجيل الخروج", use_container_width=True):
                _logout()
        _render_manage(teacher, students)
        return

    st.markdown(
        f'<div class="tp-kpis">'
        f'<div class="tp-kpi"><span>طلبة القسم</span><b>{count}</b></div>'
        f'<div class="tp-kpi"><span>متوسط التقدم</span><b>{avg}%</b></div>'
        f'<div class="tp-kpi"><span>الأوسمة</span><b>{badges}</b></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tp-card"><h3>نشاط الطلبة</h3><p>مستوى التقدم والأوسمة لطلبة قسمك. لإضافة طالب أو تغيير كلمة مروره اضغط أيقونة ➕ أو افتح إعدادات القسم.</p></div>',
        unsafe_allow_html=True,
    )
    components.html(_dashboard_html(students, name), height=820, scrolling=True)
