"""Premium admin dashboard at ?admin=1"""
from __future__ import annotations

import hashlib
import html
from typing import Any

import streamlit as st

from student_cloud_sync import (
    create_managed_spreadsheet,
    delete_message,
    last_created_url,
    last_sheets_error,
    list_messages,
    list_students,
    sheets_configured,
    spreadsheet_key,
    update_message_status,
)

CSS = r"""
<style id="samed-admin-ui-v6">
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap');
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f4f8f7!important;direction:rtl!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{
  max-width:1180px!important;padding:18px 18px 48px!important;font-family:Cairo,sans-serif!important}
[data-testid="InputInstructions"]{display:none!important}
.admin-hero{background:linear-gradient(135deg,#173f44 0%,#245e65 58%,#1c4c52 100%);
  color:#fff;border-radius:28px;padding:26px 28px;margin-bottom:18px;
  box-shadow:0 18px 40px rgba(23,63,68,.22);position:relative;overflow:hidden}
.admin-hero:after{content:"";position:absolute;inset:auto -40px -50px auto;width:180px;height:180px;
  border-radius:50%;background:rgba(245,198,90,.18)}
.admin-hero h1{margin:0;font-size:30px;font-weight:900}
.admin-hero p{margin:8px 0 0;opacity:.88;font-size:14px}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:4px 0 18px}
.kpi{background:#fff;border:1px solid #dce8e5;border-radius:20px;padding:16px 18px;
  box-shadow:0 8px 22px rgba(23,63,68,.06)}
.kpi small{display:block;color:#6f827e;font-weight:800;font-size:12px}
.kpi b{display:block;margin-top:6px;font-size:30px;color:#173f44;line-height:1}
.kpi em{display:block;margin-top:6px;font-style:normal;color:#b08a2a;font-size:11px;font-weight:800}
.nav-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:8px 0 22px}
.nav-card{background:#fff;border:1px solid #dce8e5;border-radius:24px;padding:18px 16px 14px;
  text-align:center;box-shadow:0 10px 24px rgba(23,63,68,.06)}
.nav-card .mark{width:58px;height:58px;margin:0 auto 10px;border-radius:18px;display:grid;place-items:center;
  background:linear-gradient(180deg,#eef8f4,#fff);border:1px solid #d7ece6;font-size:26px}
.nav-card b{display:block;color:#173f44;font-size:16px}
.nav-card small{display:block;margin-top:4px;color:#6f827e;font-size:12px}
.section-head{display:flex;align-items:end;justify-content:space-between;gap:12px;margin:8px 0 12px}
.section-head h2{margin:0;color:#173f44;font-size:22px}
.section-head small{color:#6f827e;font-weight:700}
.table-wrap{background:#fff;border:1px solid #dce8e5;border-radius:24px;overflow:hidden;
  box-shadow:0 12px 28px rgba(23,63,68,.06)}
.admin-table{width:100%;border-collapse:collapse}
.admin-table th{background:#173f44;color:#fff;font-size:12px;padding:12px 14px;text-align:right;font-weight:800}
.admin-table td{padding:13px 14px;border-top:1px solid #edf3f1;font-size:13px;color:#24484c;vertical-align:middle}
.admin-table tr:hover td{background:#f7fbfa}
.bar{width:110px;height:8px;background:#e7efed;border-radius:99px;overflow:hidden;display:inline-block;vertical-align:middle}
.bar i{display:block;height:100%;background:linear-gradient(90deg,#f5c65a,#245e65)}
.chip{display:inline-block;background:#eef8f4;color:#245e65;border-radius:999px;padding:3px 9px;
  font-size:11px;font-weight:800;margin-left:4px}
.gold{background:#fff6e0;color:#8a6a16}
.msg{background:#fff;border:1px solid #dce8e5;border-radius:22px;padding:18px;margin-bottom:12px;
  box-shadow:0 8px 20px rgba(23,63,68,.05)}
.msg h4{margin:8px 0 6px;color:#173f44}
.msg p{margin:0;color:#35595c;line-height:1.75}
.login-card{max-width:460px;margin:48px auto;background:#fff;border:1px solid #dce8e5;border-radius:28px;
  padding:28px;box-shadow:0 18px 40px rgba(23,63,68,.08)}
@media(max-width:900px){.kpi-grid,.nav-grid{grid-template-columns:1fr 1fr}.admin-table{font-size:12px}}
@media(max-width:640px){.kpi-grid,.nav-grid{grid-template-columns:1fr}}
</style>
"""


def _esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _admin_password() -> str:
    try:
        return str(st.secrets.get("admin", {}).get("password") or "").strip()
    except Exception:
        return ""


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _pct(value: Any) -> int:
    try:
        return max(0, min(100, int(float(str(value).replace("%", "")))))
    except Exception:
        return 0


def _login() -> bool:
    expected = _admin_password()
    st.markdown(CSS, unsafe_allow_html=True)
    if not expected:
        st.markdown('<div class="admin-hero"><h1>لوحة الإدارة</h1><p>أضف كلمة المرور في Secrets ثم أعد التشغيل.</p></div>', unsafe_allow_html=True)
        st.code('[admin]\npassword = "••••••••"', language="toml")
        return False
    if st.session_state.get("admin_ok"):
        return True
    st.markdown(
        '<div class="admin-hero"><h1>لوحة الإدارة</h1><p>دخول محمي لمتابعة الطلبة والرسائل.</p></div>'
        '<div class="login-card">',
        unsafe_allow_html=True,
    )
    pwd = st.text_input("كلمة مرور الأدمن", type="password", key="admin_pwd", label_visibility="visible")
    if st.button("دخول إلى اللوحة", type="primary", use_container_width=True):
        if pwd and (_hash(pwd) == _hash(expected) or pwd == expected):
            st.session_state["admin_ok"] = True
            st.rerun()
        st.error("كلمة المرور غير صحيحة.")
    st.markdown("</div>", unsafe_allow_html=True)
    return False


def _set_view(view: str) -> None:
    st.session_state["admin_view"] = view
    st.rerun()


def _subject_label(raw: str) -> str:
    text = str(raw or "")
    text = text.replace("phys", "فيزياء").replace("chem", "كيمياء")
    text = text.replace("physics", "فيزياء").replace("chemistry", "كيمياء")
    return text or "—"


def _kpis(students: list[dict[str, Any]]) -> None:
    grades = set()
    xp = 0
    progressed = 0
    for s in students:
        for g in str(s.get("grade") or "").replace(";", ",").split(","):
            if g.strip():
                grades.add(g.strip())
        try:
            xp += int(float(str(s.get("xp") or 0)))
        except Exception:
            pass
        if _pct(s.get("progress")) > 0:
            progressed += 1
    inbox = len(list_messages("new")) if sheets_configured() else 0
    st.markdown(
        f'<div class="kpi-grid">'
        f'<div class="kpi"><small>الطلبة المسجّلون</small><b>{len(students)}</b><em>من المنصة</em></div>'
        f'<div class="kpi"><small>الصفوف النشطة</small><b>{len(grades)}</b><em>10 / 11 / 12</em></div>'
        f'<div class="kpi"><small>مجموع النقاط</small><b>{xp}</b><em>{progressed} يتقدمون</em></div>'
        f'<div class="kpi"><small>رسائل جديدة</small><b>{inbox}</b><em>تحتاج متابعة</em></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _sheets_help() -> None:
    created = last_created_url() or st.session_state.get("admin_created_sheet_url", "")
    if created:
        st.success("تم إنشاء جدول جديد. انسخ المعرّف إلى Secrets ثم أعد التشغيل.")
        st.code(created)
        return
    if not sheets_configured():
        st.warning("لم يُضبط Google Sheets بعد. أضف [gsheets] و [gcp_service_account] في Secrets.")
        return
    err = last_sheets_error()
    if not err:
        return
    st.warning(err)
    key = spreadsheet_key()
    if key:
        st.caption("المعرّف المستخدم حاليًا")
        st.code(key)
    share_with = st.text_input("إيميل لمشاركة الجدول بعد إنشائه", value="techn47@gmail.com", key="admin_share_email")
    if st.button("إنشاء جدول جديد وربطه", key="admin_create_sheet"):
        try:
            info = create_managed_spreadsheet(share_with)
            st.session_state["admin_created_sheet_url"] = info.get("url", "")
            st.success("ضع هذا المعرّف في Secrets ثم Reboot")
            st.code(info.get("id", ""))
        except Exception:
            st.error("تعذر إنشاء الجدول. فعّل Google Drive API و Google Sheets API.")


def _home(students: list[dict[str, Any]]) -> None:
    _kpis(students)
    new_count = len(list_messages("new")) if sheets_configured() else 0
    done_count = len(list_messages("processed")) if sheets_configured() else 0
    left, right = st.columns(2)
    with left:
        st.markdown(
            f'<div class="nav-card"><div class="mark">✉️</div><b>رسائل التواصل</b><small>{new_count} رسالة جديدة</small></div>',
            unsafe_allow_html=True,
        )
        if st.button("فتح الرسائل", key="admin_open_messages", use_container_width=True):
            _set_view("messages")
    with right:
        st.markdown(
            f'<div class="nav-card"><div class="mark">✓</div><b>الرسائل المعالجة</b><small>{done_count} تمت معالجتها</small></div>',
            unsafe_allow_html=True,
        )
        if st.button("فتح الأرشيف", key="admin_open_processed", use_container_width=True):
            _set_view("processed")
    st.markdown(
        f'<div class="section-head"><h2>تقدم الطلبة</h2><small>{len(students)} طالب</small></div>',
        unsafe_allow_html=True,
    )
    if not students:
        st.info("لا توجد تسجيلات بعد. بعد رفع هذا التحديث ستظهر حسابات الطلبة هنا مباشرة عند إنشائها.")
        return
    rows = []
    for s in students:
        pct = _pct(s.get("progress"))
        badges = str(s.get("badges") or "").strip()
        badge_html = "".join(f'<span class="chip gold">{_esc(b)}</span>' for b in badges.split(",") if b.strip()) or '<span class="chip">بدون أوسمة بعد</span>'
        rows.append(
            "<tr>"
            f"<td><b>{_esc(s.get('name'))}</b><br><span class=\"chip\">{_esc(s.get('id'))}</span></td>"
            f"<td>{_esc(s.get('grade') or '—')}</td>"
            f"<td>{_esc(_subject_label(str(s.get('subjects') or '')))}</td>"
            f"<td><span class=\"bar\"><i style=\"width:{pct}%\"></i></span> {pct}%</td>"
            f"<td>{_esc(s.get('xp') or 0)}</td>"
            f"<td>{badge_html}</td>"
            f"<td>{_esc(s.get('last_seen') or '—')}</td>"
            "</tr>"
        )
    st.markdown(
        '<div class="table-wrap"><table class="admin-table"><thead><tr>'
        "<th>الطالب</th><th>الصف</th><th>المواد</th><th>التقدم</th><th>النقاط</th><th>الأوسمة</th><th>آخر ظهور</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>",
        unsafe_allow_html=True,
    )


def _messages(status: str) -> None:
    title = "رسائل التواصل" if status == "new" else "الرسائل المعالجة"
    st.markdown(f'<div class="section-head"><h2>{title}</h2></div>', unsafe_allow_html=True)
    if st.button("← العودة إلى اللوحة", key=f"admin_back_{status}"):
        _set_view("home")
    msgs = list_messages(status) if sheets_configured() else []
    if not msgs:
        st.info("لا توجد رسائل في هذه الصفحة.")
        return
    for msg in msgs:
        mid = msg.get("id") or ""
        st.markdown(
            f'<div class="msg"><span class="chip">{_esc(msg.get("subject") or "رسالة")}</span>'
            f'<h4>{_esc(msg.get("name") or "بدون اسم")}</h4>'
            f'<p>{_esc(msg.get("message") or "")}</p>'
            f'<small>{_esc(msg.get("created_at") or "")} · {_esc(msg.get("email") or "")} · {_esc(msg.get("institution") or "")}</small></div>',
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
    if not _login():
        st.stop()
    view = st.session_state.get("admin_view") or "home"
    top1, top2 = st.columns([5, 1])
    with top1:
        st.markdown(
            '<div class="admin-hero"><h1>لوحة الإدارة</h1><p>متابعة الطلبة والتقدم والأوسمة والرسائل — للأدمن فقط.</p></div>',
            unsafe_allow_html=True,
        )
    with top2:
        if st.button("خروج", key="admin_logout"):
            st.session_state["admin_ok"] = False
            st.rerun()
    students = list_students() if sheets_configured() else []
    _sheets_help()
    if view == "messages":
        _messages("new")
    elif view == "processed":
        _messages("processed")
    else:
        _home(students)
    st.stop()
