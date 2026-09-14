"""Admin dashboard: student stats plus contact inbox with process/delete."""
from __future__ import annotations

import html
from typing import Any

import streamlit as st

import student_cloud_sync as sync

GRADE_LABELS = {
    6: "السادس",
    7: "السابع",
    8: "الثامن",
    9: "التاسع",
    10: "العاشر",
    11: "الحادي عشر",
    12: "الثاني عشر",
}

_CSS = r"""
<style id="samed-admin-ui-v5">
:root{--ink:#173b3d;--muted:#6f827e;--line:#dce6e3;--teal:#245e65;--paper:#fff;--bg:#f4f8f7;--gold:#f1bf50;--danger:#b42318}
html,body,.stApp,[data-testid="stAppViewContainer"]{direction:rtl!important;text-align:right!important;background:var(--bg)!important;color:var(--ink)!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container{max-width:1100px!important;padding:16px 18px 40px!important}
.admin-nav{display:flex;align-items:center;justify-content:space-between;gap:12px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:10px 14px;margin-bottom:14px}
.admin-brand{display:flex;align-items:center;gap:10px}
.admin-mark{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(145deg,#173f44,#347d78);font-size:20px}
.admin-brand b{display:block;font-size:16px}.admin-brand small{display:block;color:var(--muted);font-size:11px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:0 0 16px}
.kpi{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 12px;text-align:center}
.kpi b{display:block;font-size:26px;color:#173f44}.kpi small{color:var(--muted);font-size:12px;font-weight:700}
.msg-card,.stu-row{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px;margin-bottom:10px}
.msg-top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.msg-top b{font-size:15px}.msg-top small{color:var(--muted)}
.msg-body{white-space:pre-wrap;line-height:1.8;margin:8px 0;color:#244}
.page-title{margin:0 0 6px;font-size:22px}.page-sub{color:var(--muted);margin:0 0 16px;font-size:13px}
.empty{background:#fff;border:1px dashed var(--line);border-radius:16px;padding:28px;text-align:center;color:var(--muted)}
.stButton>button{border-radius:12px!important;min-height:42px!important;font-weight:800!important}
.st-key-admin_open_messages button,.st-key-admin_open_processed button{min-height:88px!important;background:#fff!important;border:1px solid var(--line)!important;color:#173b3d!important}
.banner{background:#fff8e8;border:1px solid #eedcae;color:#735b20;border-radius:12px;padding:10px 12px;margin-bottom:12px;font-size:13px}
@media(max-width:800px){.kpis{grid-template-columns:1fr 1fr}}
</style>
"""


def _esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _grade_label(raw: str) -> str:
    parts = []
    for bit in str(raw or "").replace("|", ",").split(","):
        bit = bit.strip()
        if not bit:
            continue
        try:
            g = int(bit)
        except Exception:
            parts.append(bit)
            continue
        parts.append("الصف " + GRADE_LABELS.get(g, str(g)))
    return " · ".join(parts) or "—"


def _num(value: Any) -> float:
    try:
        return float(str(value).replace("%", "").strip() or 0)
    except Exception:
        return 0.0


def _demo_students() -> list[dict[str, Any]]:
    return [
        {"id": "demo-1", "name": "أحمد خالد", "grade": "12", "subjects": "phys,chem", "xp": "240", "progress": "68", "badges": "3", "last_seen": "—"},
        {"id": "demo-2", "name": "سارة علي", "grade": "11,12", "subjects": "phys", "xp": "120", "progress": "41", "badges": "1", "last_seen": "—"},
        {"id": "demo-3", "name": "يوسف منير", "grade": "6,7", "subjects": "chem", "xp": "80", "progress": "22", "badges": "0", "last_seen": "—"},
    ]


def _students() -> tuple[list[dict[str, Any]], bool]:
    if sync.is_configured():
        try:
            return sync.list_students(), True
        except Exception:
            return _demo_students(), False
    return _demo_students(), False


def _login() -> bool:
    if st.session_state.get("samed_admin_ok"):
        return True
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="admin-nav"><div class="admin-brand"><span class="admin-mark">🛡️</span>'
        "<span><b>لوحة الإدارة</b><small>دخول محمي</small></span></div></div>",
        unsafe_allow_html=True,
    )
    expected = ""
    try:
        expected = str((st.secrets.get("admin") or {}).get("password") or "").strip()
    except Exception:
        expected = ""
    if not expected:
        st.warning("أضف كلمة مرور الأدمن في Streamlit Cloud عبر Settings → Secrets ثم أعد تشغيل التطبيق.")
        return False
    pwd = st.text_input("كلمة مرور الأدمن", type="password", key="admin_password_input")
    if st.button("دخول", type="primary", use_container_width=True, key="admin_login_btn"):
        if pwd == expected:
            st.session_state["samed_admin_ok"] = True
            st.rerun()
        st.error("كلمة المرور غير صحيحة.")
    return False


def _nav(title: str, subtitle: str) -> None:
    st.markdown(
        '<div class="admin-nav"><div class="admin-brand"><span class="admin-mark">🛡️</span>'
        f"<span><b>الطالب الصامد</b><small>{_esc(subtitle)}</small></span></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(f'<h1 class="page-title">{_esc(title)}</h1>', unsafe_allow_html=True)


def _render_home() -> None:
    students, live = _students()
    n = len(students)
    avg = int(round(sum(_num(s.get("progress")) for s in students) / n)) if n else 0
    badges = int(sum(_num(s.get("badges")) for s in students))
    grades = set()
    for s in students:
        for bit in str(s.get("grade") or "").split(","):
            if bit.strip():
                grades.add(bit.strip())
    if not live:
        st.markdown('<div class="banner">لم يُضبط Google Sheets بعد، لذلك تُعرض بيانات تجريبية.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kpis">'
        f'<div class="kpi"><b>{n}</b><small>طالب مسجّل</small></div>'
        f'<div class="kpi"><b>{len(grades)}</b><small>صفوف نشطة</small></div>'
        f'<div class="kpi"><b>{avg}%</b><small>متوسط التقدم</small></div>'
        f'<div class="kpi"><b>{badges}</b><small>أوسمة</small></div></div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📬 الرسائل", key="admin_open_messages", use_container_width=True):
            st.session_state["admin_view"] = "messages"
            st.rerun()
    with c2:
        if st.button("✅ الرسائل المعالجة", key="admin_open_processed", use_container_width=True):
            st.session_state["admin_view"] = "processed"
            st.rerun()
    st.markdown('<p class="page-sub">تقدم الطلبة</p>', unsafe_allow_html=True)
    if not students:
        st.markdown('<div class="empty">لا يوجد طلبة مسجّلون بعد.</div>', unsafe_allow_html=True)
        return
    for s in students:
        subjects = str(s.get("subjects") or "").replace("phys", "فيزياء").replace("chem", "كيمياء")
        st.markdown(
            f'<div class="stu-row"><div class="msg-top"><b>{_esc(s.get("name") or "طالب")}</b>'
            f'<small>{_esc(_grade_label(s.get("grade") or ""))}</small></div>'
            f'<small>المواد: {_esc(subjects or "—")} · التقدم: {_esc(s.get("progress") or 0)}% · '
            f'أوسمة: {_esc(s.get("badges") or 0)} · نقاط: {_esc(s.get("xp") or 0)}</small></div>',
            unsafe_allow_html=True,
        )


def _render_messages(*, processed: bool) -> None:
    title = "الرسائل المعالجة" if processed else "رسائل التواصل"
    _nav(title, "لوحة الإدارة")
    if st.button("← رجوع", key="admin_back_" + ("processed" if processed else "messages")):
        st.session_state["admin_view"] = "home"
        st.rerun()
    rows = []
    if sync.is_configured():
        try:
            rows = [m for m in sync.list_contact_messages() if ((m.get("status") or "new") == "processed") is processed]
        except Exception:
            st.error("تعذّر قراءة الرسائل من Google Sheets.")
            return
    else:
        st.markdown('<div class="banner">لم يُضبط Google Sheets بعد، لذلك لا تظهر رسائل حقيقية.</div>', unsafe_allow_html=True)
    if not rows:
        st.markdown('<div class="empty">لا توجد رسائل هنا حاليًا.</div>', unsafe_allow_html=True)
        return
    for msg in rows:
        mid = str(msg.get("id") or "")
        st.markdown(
            f'<div class="msg-card"><div class="msg-top"><div><b>{_esc(msg.get("name") or "بدون اسم")}</b>'
            f'<br><small>{_esc(msg.get("subject") or "بدون موضوع")} · {_esc(msg.get("created_at") or "")}</small></div>'
            f'<small>{_esc(msg.get("email") or "")}</small></div>'
            f'<div class="msg-body">{_esc(msg.get("message") or "")}</div>'
            f'<small>المؤسسة: {_esc(msg.get("institution") or "—")}</small></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2 if not processed else 1)
        if not processed:
            with cols[0]:
                if st.button("تمت المعالجة", key=f"admin_done_{mid}", use_container_width=True):
                    sync.update_message_status(mid, "processed")
                    st.rerun()
            with cols[1]:
                if st.button("حذف الرسالة", key=f"admin_del_{mid}", use_container_width=True):
                    sync.delete_message(mid)
                    st.rerun()
        else:
            with cols[0]:
                if st.button("حذف الرسالة", key=f"admin_delp_{mid}", use_container_width=True):
                    sync.delete_message(mid)
                    st.rerun()


def render_admin_panel() -> None:
    if "admin_view" not in st.session_state:
        st.session_state["admin_view"] = "home"
    if not _login():
        st.stop()
    st.markdown(_CSS, unsafe_allow_html=True)
    view = st.session_state.get("admin_view") or "home"
    if view == "messages":
        _render_messages(processed=False)
    elif view == "processed":
        _render_messages(processed=True)
    else:
        _nav("لوحة الإدارة", "إحصائيات الطلبة والرسائل")
        _render_home()
