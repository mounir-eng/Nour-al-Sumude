"""لوحة الأستاذ: متابعة القسم، وإضافة الطلبة من صفحة إعدادات مستقلة."""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from accounts import add_student_for_teacher, reset_student_password
from student_cloud_sync import is_configured, list_students

_CSS = r"""
<style id="samed-teacher-panel-v3">
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{
  direction:rtl!important;text-align:right!important;
  font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important
}
.stApp,[data-testid="stAppViewContainer"]{background:#f3f7f6!important;color:#16383b!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{
  max-width:1160px!important;padding:20px 16px 32px!important
}
.tp-hero{
  display:flex;align-items:center;justify-content:space-between;gap:16px;
  background:linear-gradient(135deg,#14383d 0%,#1f585e 58%,#2f7a76 120%);
  color:#fff;border-radius:24px;padding:22px 24px;margin-bottom:14px;
  box-shadow:0 18px 40px rgba(20,56,61,.18)
}
.tp-hero-copy{display:flex;align-items:center;gap:14px}
.tp-mark{
  width:54px;height:54px;border-radius:16px;flex:0 0 auto;
  display:grid;place-items:center;background:rgba(255,255,255,.12)
}
.tp-hero b{display:block;font-size:24px;line-height:1.35;letter-spacing:-.3px}
.tp-hero small{display:block;margin-top:4px;color:#d5ece8;font-size:13px;font-weight:700}
.tp-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0 0 16px}
.tp-kpi{
  background:#fff;border:1px solid #dbe7e4;border-radius:18px;padding:16px 18px;
  box-shadow:0 8px 20px rgba(22,56,61,.05)
}
.tp-kpi span{display:block;color:#6a7f7b;font-size:12px;font-weight:800}
.tp-kpi b{display:block;margin-top:6px;color:#14383d;font-size:28px;line-height:1}
.tp-card{
  background:#fff;border:1px solid #dbe7e4;border-radius:22px;
  padding:20px 20px 8px;margin-bottom:14px;box-shadow:0 10px 24px rgba(22,56,61,.05)
}
.tp-card h3{margin:0 0 6px;font-size:20px}
.tp-card p.lead{margin:0 0 14px;color:#6a7f7b;font-size:13px;line-height:1.85}
.tp-section-head{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}
.tp-section-icon{
  width:44px;height:44px;border-radius:14px;flex:0 0 auto;
  display:grid;place-items:center;background:#eaf6f3;color:#1f585e
}
.tp-hint{
  display:flex;gap:8px;align-items:flex-start;background:#fff8e8;border:1px solid #eedcae;
  border-radius:14px;padding:11px 12px;color:#735b20;font-size:12px;line-height:1.8;margin:0 0 8px
}
.stButton>button{
  border-radius:14px!important;min-height:48px!important;font-weight:800!important;
  border:1px solid #d5e3e0!important;background:#fff!important;color:#16383b!important
}
.st-key-tp_learn button{
  background:linear-gradient(135deg,#1f585e,#2f7a76)!important;color:#fff!important;border:0!important
}
.st-key-tp_add_student button{
  background:#fff!important;color:#14383d!important;border:1px solid #cfe0dc!important;
  box-shadow:0 8px 18px rgba(22,56,61,.06)!important
}
.st-key-tp_back button{
  background:linear-gradient(135deg,#1f585e,#2f7a76)!important;color:#fff!important;border:0!important
}
.stFormSubmitButton>button{
  background:#14383d!important;color:#fff!important;border:0!important;
  border-radius:14px!important;min-height:48px!important;font-weight:800!important
}
.stTextInput label,.stSelectbox label,.stMultiSelect label{font-weight:800!important;font-size:13px!important;color:#16383b!important}
.stTextInput input,.stSelectbox [data-baseweb="select"]>div{min-height:46px!important;border-radius:12px!important}
@media(max-width:800px){
  .tp-hero{display:grid}.tp-kpis{grid-template-columns:1fr}
}
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


def _hero(title: str, subtitle: str, icon: str) -> None:
    st.markdown(
        f'<div class="tp-hero"><div class="tp-hero-copy">'
        f'<span class="tp-mark">{icon}</span>'
        f'<span><b>{title}</b><small>{subtitle}</small></span></div></div>',
        unsafe_allow_html=True,
    )


def _render_settings(teacher: dict, students: list[dict]) -> None:
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(
            '<div class="tp-card"><div class="tp-section-head">'
            '<span class="tp-section-icon">👤+</span>'
            '<span><h3>إضافة طالب</h3>'
            '<p class="lead">أنشئ حسابًا لطالب القسم. أعطه الاسم وكلمة المرور بنفسك؛ لن تظهر الكلمة هنا بعد الحفظ.</p></span>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        with st.form("add_student_form"):
            student_name = st.text_input("اسم الطالب", placeholder="مثال: أحمد خالد")
            grade = st.selectbox("الصف الدراسي", list(range(6, 13)), index=6)
            subjects = st.multiselect("المواد", ["فيزياء", "كيمياء"], default=["فيزياء", "كيمياء"])
            password = st.text_input("كلمة المرور", type="password")
            confirm = st.text_input("تأكيد كلمة المرور", type="password")
            submitted = st.form_submit_button("حفظ حساب الطالب", type="primary", use_container_width=True)
        if submitted:
            mapped = []
            if "فيزياء" in subjects:
                mapped.append("phys")
            if "كيمياء" in subjects:
                mapped.append("chem")
            ok, message = add_student_for_teacher(
                teacher["id"], student_name, int(grade), mapped or ["phys"], password, confirm
            )
            if ok:
                st.success(message)
                st.session_state["teacher_panel_view"] = "home"
                st.rerun()
            else:
                st.error(message)
        st.markdown(
            '<div class="tp-hint">🔒 لا تكتب كلمة المرور في الدردشة أو أمام الصف. سلّمها للطالب مباشرة.</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div class="tp-card"><div class="tp-section-head">'
            '<span class="tp-section-icon">🔑</span>'
            '<span><h3>تغيير كلمة المرور</h3>'
            '<p class="lead">إذا نسي الطالب كلمته، عيّن كلمة جديدة هنا ثم أخبره بها. الكلمات القديمة لا تُعرض.</p></span>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        if students:
            labels = {str(s.get("name") or s.get("id")): str(s.get("id")) for s in students}
            with st.form("reset_student_form"):
                chosen = st.selectbox("اختر الطالب", list(labels.keys()))
                new_pw = st.text_input("كلمة المرور الجديدة", type="password")
                new_cf = st.text_input("تأكيد الكلمة الجديدة", type="password")
                reset_ok = st.form_submit_button("حفظ الكلمة الجديدة", use_container_width=True)
            if reset_ok:
                ok, message = reset_student_password(str(teacher["id"]), labels[chosen], new_pw, new_cf)
                if ok:
                    st.success(message)
                else:
                    st.error(message)
        else:
            st.info("لا يوجد طلبة في القسم بعد. أضف طالبًا من البطاقة المجاورة أولًا.")


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
        _hero("إعدادات القسم", f"{name} · إضافة طالب أو تغيير كلمة المرور", "👤")
        c1, c2, c3 = st.columns([1.4, 1, 1])
        with c1:
            if st.button("عودة إلى لوحة الأستاذ", key="tp_back", use_container_width=True):
                st.session_state["teacher_panel_view"] = "home"
                st.rerun()
        with c2:
            if st.button("الرئيسية", key="tp_home_settings", use_container_width=True):
                st.session_state["samed_view"] = "home"
                st.rerun()
        with c3:
            if st.button("تسجيل الخروج", key="tp_logout_settings", use_container_width=True):
                _logout()
        _render_settings(teacher, students)
        return

    _hero("لوحة الأستاذ", f"{name} · متابعة قسمك فقط", "🛡️")
    a1, a2, a3, a4 = st.columns([1.25, 1.15, 1, 1])
    with a1:
        if st.button("المحتوى التعليمي", key="tp_learn", type="primary", use_container_width=True):
            _open_learning(teacher)
    with a2:
        if st.button("إضافة طالب", key="tp_add_student", use_container_width=True):
            st.session_state["teacher_panel_view"] = "manage"
            st.rerun()
    with a3:
        if st.button("الرئيسية", key="tp_home", use_container_width=True):
            st.session_state["samed_view"] = "home"
            st.rerun()
    with a4:
        if st.button("تسجيل الخروج", key="tp_logout", use_container_width=True):
            _logout()

    st.markdown(
        f'<div class="tp-kpis">'
        f'<div class="tp-kpi"><span>طلبة القسم</span><b>{count}</b></div>'
        f'<div class="tp-kpi"><span>متوسط التقدم</span><b>{avg}%</b></div>'
        f'<div class="tp-kpi"><span>الأوسمة</span><b>{badges}</b></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tp-card"><h3>نشاط الطلبة</h3>'
        '<p class="lead">مستوى التقدم والأوسمة لطلبة قسمك. لإضافة طالب أو تغيير كلمة مروره اضغط «إضافة طالب».</p></div>',
        unsafe_allow_html=True,
    )
    components.html(_dashboard_html(students, name), height=820, scrolling=True)
