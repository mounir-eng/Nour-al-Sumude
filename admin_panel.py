"""Hidden admin dashboard at ?admin=1"""
from __future__ import annotations

import hashlib
from typing import Any

import streamlit as st

from student_cloud_sync import (
    delete_message,
    list_messages,
    list_students,
    sheets_configured,
    update_message_status,
)

CSS = """
<style id="samed-admin-ui-v5">
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f4f8f7!important;direction:rtl!important}
section[data-testid="stMain"] .block-container{max-width:1120px!important;padding:18px 18px 40px!important}
.admin-hero{background:linear-gradient(135deg,#173f44,#245e65);color:#fff;border-radius:24px;padding:22px 24px;margin-bottom:16px}
.admin-hero h1{margin:0;font-size:26px}.admin-hero p{margin:6px 0 0;opacity:.86;font-size:14px}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:14px 0 18px}
.kpi{background:#fff;border:1px solid #dce8e5;border-radius:18px;padding:16px}
.kpi b{display:block;font-size:28px;color:#173f44}.kpi small{color:#6f827e;font-weight:700}
.icon-row{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:8px 0 20px}
.icon-card{background:#fff;border:1px solid #dce8e5;border-radius:20px;padding:18px;text-align:center}
.icon-card .mark{width:52px;height:52px;border-radius:16px;background:#eef8f4;margin:0 auto 8px;display:grid;place-items:center;font-size:22px}
.icon-card b{display:block;color:#173f44}.icon-card small{color:#6f827e}
.msg{background:#fff;border:1px solid #dce8e5;border-radius:18px;padding:16px;margin-bottom:12px}
.msg h4{margin:0 0 6px;color:#173f44}.msg p{margin:0;color:#35595c;line-height:1.7}
.badge{display:inline-block;background:#eef8f4;color:#245e65;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:800}
@media(max-width:800px){.kpi-row,.icon-row{grid-template-columns:1fr 1fr}}
</style>
"""


def _admin_password() -> str:
    try:
        return str(st.secrets.get("admin", {}).get("password") or "").strip()
    except Exception:
        return ""


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _login() -> bool:
    expected = _admin_password()
    if not expected:
        st.warning("أضف كلمة مرور الأدمن في Streamlit Cloud عبر Settings → Secrets ثم أعد تشغيل التطبيق.")
        st.code('[admin]\npassword = "••••••••"', language="toml")
        return False
    if st.session_state.get("admin_ok"):
        return True
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<div class="admin-hero"><h1>لوحة الإدارة</h1><p>أدخل كلمة المرور للمتابعة.</p></div>', unsafe_allow_html=True)
    pwd = st.text_input("كلمة مرور الأدمن", type="password", key="admin_pwd")
    if st.button("دخول", type="primary", use_container_width=True):
        if pwd and (_hash(pwd) == _hash(expected) or pwd == expected):
            st.session_state["admin_ok"] = True
            st.rerun()
        st.error("كلمة المرور غير صحيحة.")
    return False


def _set_view(view: str) -> None:
    st.session_state["admin_view"] = view
    st.rerun()


def _kpis(students: list[dict[str, Any]]) -> None:
    n = len(students)
    grades = set()
    for s in students:
        for g in str(s.get("grade") or "").replace(";", ",").split(","):
            if g.strip():
                grades.add(g.strip())
    xp = 0
    for s in students:
        try:
            xp += int(float(str(s.get("xp") or 0)))
        except Exception:
            pass
    inbox = len(list_messages("new")) if sheets_configured() else 0
    st.markdown(
        f'<div class="kpi-row"><div class="kpi"><small>الطلبة</small><b>{n}</b></div>'
        f'<div class="kpi"><small>الصفوف</small><b>{len(grades)}</b></div>'
        f'<div class="kpi"><small>النقاط</small><b>{xp}</b></div>'
        f'<div class="kpi"><small>رسائل جديدة</small><b>{inbox}</b></div></div>',
        unsafe_allow_html=True,
    )


def _home(students: list[dict[str, Any]]) -> None:
    _kpis(students)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✉️ رسائل التواصل", key="admin_open_messages", use_container_width=True):
            _set_view("messages")
    with c2:
        if st.button("✓ الرسائل المعالجة", key="admin_open_processed", use_container_width=True):
            _set_view("processed")
    st.markdown("### تقدم الطلبة")
    if not students:
        st.info("لا يوجد طلبة مسجّلون بعد." if sheets_configured() else "لم يُضبط Google Sheets بعد.")
        return
    rows = []
    for s in students:
        rows.append({
            "الاسم": s.get("name"),
            "الصف": s.get("grade"),
            "المواد": s.get("subjects"),
            "التقدم": s.get("progress"),
            "النقاط": s.get("xp"),
            "الأوسمة": s.get("badges"),
            "آخر ظهور": s.get("last_seen"),
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)


def _messages(status: str) -> None:
    title = "رسائل التواصل" if status == "new" else "الرسائل المعالجة"
    st.markdown(f"### {title}")
    if st.button("← العودة", key=f"admin_back_{status}"):
        _set_view("home")
    msgs = list_messages(status) if sheets_configured() else []
    if not msgs:
        st.info("لا توجد رسائل في هذه الصفحة.")
        return
    for msg in msgs:
        mid = msg.get("id") or ""
        st.markdown(
            f'<div class="msg"><span class="badge">{msg.get("subject") or "رسالة"}</span>'
            f'<h4>{msg.get("name") or "بدون اسم"}</h4>'
            f'<p>{msg.get("message") or ""}</p>'
            f'<small>{msg.get("created_at") or ""} · {msg.get("email") or ""} · {msg.get("institution") or ""}</small></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        if status == "new":
            with cols[0]:
                if st.button("تمت المعالجة", key=f"admin_done_{mid}", use_container_width=True):
                    update_message_status(mid, "processed")
                    st.rerun()
            with cols[1]:
                if st.button("حذف", key=f"admin_del_{mid}", use_container_width=True):
                    delete_message(mid)
                    st.rerun()
        else:
            if st.button("حذف", key=f"admin_delp_{mid}", use_container_width=True):
                delete_message(mid)
                st.rerun()


def render_admin_panel() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    if not _login():
        st.stop()
    view = st.session_state.get("admin_view") or "home"
    top1, top2 = st.columns([4, 1])
    with top1:
        st.markdown('<div class="admin-hero"><h1>لوحة الإدارة</h1><p>إحصائيات الطلبة والرسائل — للأدمن فقط.</p></div>', unsafe_allow_html=True)
    with top2:
        if st.button("خروج", key="admin_logout"):
            st.session_state["admin_ok"] = False
            st.rerun()
    students = list_students() if sheets_configured() else []
    if view == "messages":
        _messages("new")
    elif view == "processed":
        _messages("processed")
    else:
        _home(students)
    st.stop()
