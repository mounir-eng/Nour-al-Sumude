"""صفحة أدمن محمية — تُفتح عبر ?admin=1 ولا تظهر للطلبة."""
from __future__ import annotations

import hmac
import html
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from student_cloud_sync import is_configured, list_contact_messages, list_students

_ADMIN_CSS = r"""
<style id="samed-admin-ui-v4">
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{
  direction:rtl!important;text-align:right!important;
  font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important
}
.stApp,[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1200px 420px at 100% -10%, rgba(47,122,118,.10), transparent 55%),
    radial-gradient(900px 380px at 0% 0%, rgba(241,191,80,.10), transparent 50%),
    #eef3f1 !important;
  color:#122f32!important
}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{
  max-width:1180px!important;padding:22px 18px 40px!important
}
.admin-box{
  background:#fff;border:1px solid #d9e6e2;border-radius:28px;padding:32px 28px;
  max-width:420px;margin:14vh auto 0;box-shadow:0 24px 60px rgba(18,47,50,.10);text-align:center
}
.admin-box h1{font-size:28px;margin:0 0 8px;letter-spacing:-.4px}
.admin-box p{color:#6a7f7b;font-size:14px;line-height:1.9;margin:0 0 18px}
.ad-hero{
  display:flex;align-items:center;gap:16px;
  background:linear-gradient(135deg,#123438 0%,#1c5459 52%,#2f7a76 120%);
  color:#fff;border-radius:28px;padding:26px 28px;margin-bottom:18px;
  box-shadow:0 22px 50px rgba(18,47,50,.20)
}
.ad-hero .mark{
  width:64px;height:64px;border-radius:22px;flex:0 0 auto;
  display:grid;place-items:center;font-size:28px;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.14)
}
.ad-hero b{display:block;font-size:28px;letter-spacing:-.5px;line-height:1.25}
.ad-hero small{display:block;margin-top:6px;color:#d7ece8;font-size:14px;font-weight:700}
.ad-kicker{
  margin:4px 4px 12px;color:#5f7773;font-size:12px;font-weight:800;letter-spacing:.4px
}
.ad-card{
  background:#fff;border:1px solid #dce8e4;border-radius:24px;
  padding:20px 20px 16px;margin:0 0 14px;
  box-shadow:0 12px 30px rgba(18,47,50,.06)
}
.ad-person{display:flex;align-items:center;gap:14px;margin-bottom:14px}
.ad-avatar{
  width:52px;height:52px;border-radius:18px;flex:0 0 auto;
  display:grid;place-items:center;color:#fff;font-weight:800;font-size:18px;
  background:linear-gradient(145deg,#173f44,#2f7a76)
}
.ad-person b{display:block;font-size:18px;color:#122f32}
.ad-person small{display:block;margin-top:3px;color:#6a7f7b;font-size:13px}
.ad-pill{
  margin-right:auto;background:#fff6df;color:#8a6a1d;border:1px solid #f1dd9a;
  border-radius:999px;padding:4px 10px;font-size:11px;font-weight:800
}
.ad-msg h3{margin:0 0 6px;font-size:18px}
.ad-msg .meta{margin:0 0 12px;color:#6a7f7b;font-size:13px}
.ad-msg .body{
  margin:0;background:#f7fbfa;border:1px solid #e4eeeb;border-radius:16px;
  padding:14px 16px;line-height:1.9;color:#1b3c3f;white-space:pre-wrap
}
.ad-empty{
  background:#fff;border:1px dashed #c9ddd8;border-radius:28px;
  padding:56px 24px;text-align:center;color:#6a7f7b;
  box-shadow:0 10px 28px rgba(18,47,50,.04)
}
.ad-empty .ico{
  width:72px;height:72px;margin:0 auto 14px;border-radius:24px;
  display:grid;place-items:center;font-size:32px;background:#eaf6f3
}
.ad-empty b{display:block;color:#122f32;font-size:20px;margin-bottom:6px}
.ad-empty p{margin:0;line-height:1.8}
.stButton>button{
  border-radius:16px!important;min-height:48px!important;font-weight:800!important;
  border:1px solid #d5e3e0!important;background:#fff!important;color:#16383b!important
}
.st-key-admin_open_teachers,.st-key-admin_open_messages{max-width:170px}
.st-key-admin_open_teachers button,.st-key-admin_open_messages button{
  width:158px!important;height:158px!important;min-height:158px!important;
  display:flex!important;flex-direction:column!important;align-items:center!important;
  justify-content:flex-end!important;gap:0!important;padding:18px 10px 16px!important;
  border-radius:32px!important;background:#fff!important;border:1px solid #dce8e4!important;
  box-shadow:0 16px 36px rgba(18,47,50,.08)!important;font-size:14px!important;line-height:1.35!important
}
.st-key-admin_open_teachers button:hover,.st-key-admin_open_messages button:hover{
  transform:translateY(-2px);box-shadow:0 20px 40px rgba(18,47,50,.12)!important;border-color:#c5ddd7!important
}
.st-key-admin_open_teachers button::before,.st-key-admin_open_messages button::before{
  display:grid;place-items:center;width:68px;height:68px;border-radius:22px;
  font-size:32px;margin:0 auto 12px;content:""
}
.st-key-admin_open_teachers button::before{
  content:"👨‍🏫";background:linear-gradient(160deg,#e7f6f2,#cfeee6)
}
.st-key-admin_open_messages button::before{
  content:"✉️";background:linear-gradient(160deg,#fff6df,#f7e7b8)
}
.st-key-admin_back_teachers button,.st-key-admin_back_messages button{
  background:#fff!important;min-height:44px!important
}
.st-key-admin_approve button{
  background:linear-gradient(135deg,#1f585e,#2f7a76)!important;color:#fff!important;border:0!important
}
.st-key-admin_reject button,.stButton button[kind="secondary"]{
  background:#fff6f5!important;color:#9a3d38!important;border:1px solid #f0d0cd!important
}
@media(max-width:800px){
  .ad-hero{display:grid;padding:20px}
  .st-key-admin_open_teachers button,.st-key-admin_open_messages button{width:100%!important}
}
</style>
"""


def is_admin_request() -> bool:
    try:
        value = st.query_params.get("admin", "")
    except Exception:
        value = ""
    if isinstance(value, list):
        value = value[0] if value else ""
    return str(value).strip().lower() in {"1", "true", "yes"}


def _admin_password() -> str:
    try:
        return str(st.secrets.get("admin", {}).get("password", "")).strip()
    except Exception:
        return ""


def _passwords_match(entered: str, expected: str) -> bool:
    left = entered.encode("utf-8")
    right = expected.encode("utf-8")
    if len(left) != len(right):
        return False
    return hmac.compare_digest(left, right)


def _esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def _initial(name: str) -> str:
    text = (name or "؟").strip()
    return text[:1].upper() if text else "؟"


def _hero(title: str, subtitle: str, icon: str) -> None:
    st.markdown(
        f'<div class="ad-hero"><span class="mark">{icon}</span>'
        f'<span><b>{_esc(title)}</b><small>{_esc(subtitle)}</small></span></div>',
        unsafe_allow_html=True,
    )


def _pending_teachers() -> list[dict]:
    try:
        from accounts import list_pending_teachers
        return list_pending_teachers() or []
    except Exception:
        return []


def _contact_rows() -> list[dict]:
    if not is_configured():
        return []
    try:
        return list_contact_messages() or []
    except Exception:
        return []


def _render_teachers_page() -> None:
    _hero("طلبات الأساتذة", "راجع كل طلب على حدة ثم وافق أو ارفض", "👨‍🏫")
    top, _ = st.columns([1.1, 3])
    with top:
        if st.button("← عودة إلى لوحة الإدارة", key="admin_back_teachers", use_container_width=True):
            st.session_state["admin_view"] = "home"
            st.rerun()
    try:
        from accounts import approve_teacher, reject_teacher
        pending = _pending_teachers()
    except Exception:
        st.error("تعذر تحميل الطلبات الآن. حاول مرة أخرى لاحقًا.")
        return
    if not pending:
        st.markdown(
            '<div class="ad-empty"><div class="ico">✅</div>'
            "<b>لا توجد طلبات جديدة</b><p>عندما يسجّل أستاذ سيظهر طلبه في هذه الصفحة فقط.</p></div>",
            unsafe_allow_html=True,
        )
        return
    for row in pending:
        name = row.get("name") or "أستاذ"
        email = row.get("email") or ""
        st.markdown(
            f'<div class="ad-card"><div class="ad-person">'
            f'<span class="ad-avatar">{_esc(_initial(str(name)))}</span>'
            f'<span><b>{_esc(name)}</b><small>{_esc(email)}</small></span>'
            f'<span class="ad-pill">بانتظار المراجعة</span></div></div>',
            unsafe_allow_html=True,
        )
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            if st.button("موافقة", key=f"ok-{row['id']}", use_container_width=True):
                approve_teacher(row["id"])
                st.rerun()
        with c2:
            if st.button("رفض", key=f"no-{row['id']}", use_container_width=True):
                reject_teacher(row["id"])
                st.rerun()


def _render_messages_page() -> None:
    _hero("رسائل التواصل", "كل رسالة في بطاقة مستقلة وواضحة", "✉️")
    top, _ = st.columns([1.1, 3])
    with top:
        if st.button("← عودة إلى لوحة الإدارة", key="admin_back_messages", use_container_width=True):
            st.session_state["admin_view"] = "home"
            st.rerun()
    try:
        messages = _contact_rows()
    except Exception:
        st.error("تعذر تحميل الرسائل الآن. حاول مرة أخرى لاحقًا.")
        return
    if not messages:
        st.markdown(
            '<div class="ad-empty"><div class="ico">✉️</div>'
            "<b>لا توجد رسائل بعد</b><p>ستظهر هنا الرسائل القادمة من صفحة التواصل.</p></div>",
            unsafe_allow_html=True,
        )
        return
    for row in messages[:60]:
        name = row.get("name") or "بدون اسم"
        subject = row.get("subject") or "بدون موضوع"
        created = str(row.get("created_at") or "")[:19].replace("T", " ")
        email = row.get("email") or "—"
        institution = row.get("institution") or "—"
        body = row.get("message") or ""
        st.markdown(
            f'<div class="ad-card ad-msg"><div class="ad-person">'
            f'<span class="ad-avatar">{_esc(_initial(str(name)))}</span>'
            f'<span><b>{_esc(subject)}</b><small>{_esc(name)} · {_esc(email)}</small></span>'
            f'<span class="ad-pill">{_esc(created)}</span></div>'
            f'<p class="meta">{_esc(institution)}</p>'
            f'<p class="body">{_esc(body)}</p></div>',
            unsafe_allow_html=True,
        )


def _render_home() -> None:
    pending = _pending_teachers()
    messages = _contact_rows()
    _hero("لوحة الإدارة", "أيقونات سريعة، ثم متابعة تقدّم الطلبة", "🛡️")
    st.markdown('<div class="ad-kicker">اختصارات الإدارة</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<style>
.st-key-admin_open_teachers button::after{{
  content:"{len(pending)} بانتظار المراجعة";display:block;margin-top:6px;
  color:#6a7f7b;font-size:11px;font-weight:700
}}
.st-key-admin_open_messages button::after{{
  content:"{len(messages)} رسالة";display:block;margin-top:6px;
  color:#6a7f7b;font-size:11px;font-weight:700
}}
</style>
""",
        unsafe_allow_html=True,
    )
    d1, d2, d3 = st.columns([1, 1, 2])
    with d1:
        if st.button("طلبات الأساتذة", key="admin_open_teachers", use_container_width=True):
            st.session_state["admin_view"] = "teachers"
            st.rerun()
    with d2:
        if st.button("رسائل التواصل", key="admin_open_messages", use_container_width=True):
            st.session_state["admin_view"] = "messages"
            st.rerun()

    live = False
    students: list[dict] | None = None
    if is_configured():
        try:
            students = list_students()
            live = True
        except Exception:
            st.error("تعذر تحميل بيانات الطلبة الآن. حاول مرة أخرى لاحقًا.")
            students = []
            live = True

    html_path = Path(__file__).with_name("admin_dashboard.html")
    page = html_path.read_text(encoding="utf-8")
    if live:
        payload = json.dumps(students or [], ensure_ascii=False)
        page = page.replace(
            "/*__STUDENTS_INJECT__*/",
            f"window.SAMED_LIVE=true;window.SAMED_ROLE='admin';window.SAMED_STUDENTS={payload};",
        )
    else:
        page = page.replace("/*__STUDENTS_INJECT__*/", "window.SAMED_ROLE='admin';")
    components.html(page, height=900, scrolling=True)


def render_admin_panel() -> None:
    st.markdown(_ADMIN_CSS, unsafe_allow_html=True)
    expected = _admin_password()
    if not expected:
        st.markdown(
            '<div class="admin-box"><h1>لوحة الإدارة</h1>'
            "<p>أضف كلمة مرور الأدمن من إعدادات التطبيق ثم أعد التشغيل.</p></div>",
            unsafe_allow_html=True,
        )
        st.code('[admin]\npassword = "كلمة-مرور-خاصة-بك"', language="toml")
        st.stop()

    if not st.session_state.get("samed_admin_ok"):
        st.markdown(
            '<div class="admin-box"><h1>دخول الأدمن</h1>'
            "<p>هذه الصفحة للمشرف فقط.</p></div>",
            unsafe_allow_html=True,
        )
        entered = st.text_input("كلمة مرور الأدمن", type="password", key="samed_admin_password")
        if st.button("دخول", type="primary"):
            if _passwords_match(entered.strip(), expected):
                st.session_state["samed_admin_ok"] = True
                st.rerun()
            st.error("كلمة المرور غير صحيحة.")
        st.stop()

    if "admin_view" not in st.session_state:
        st.session_state["admin_view"] = "home"
    view = st.session_state.get("admin_view") or "home"
    if view == "teachers":
        _render_teachers_page()
        return
    if view == "messages":
        _render_messages_page()
        return
    _render_home()
