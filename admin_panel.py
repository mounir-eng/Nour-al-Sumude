"""Admin dashboard for الطالب الصامد."""
from __future__ import annotations

import html
from typing import Any

import streamlit as st

from student_cloud_sync import (
    create_managed_spreadsheet,
    delete_message,
    last_created_url,
    last_sheets_error,
    last_upsert_name,
    list_messages,
    list_students,
    sheets_configured,
    spreadsheet_key,
    update_message_status,
)

ADMIN_UI = "samed-admin-ui-v7"


def _admin_password() -> str:
    try:
        return str(st.secrets.get("admin", {}).get("password") or "").strip()
    except Exception:
        return ""


def _css() -> None:
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;800&display=swap');
html, body, [data-testid="stAppViewContainer"], .stApp {{
  font-family: Cairo, 'Noto Sans Arabic', Tahoma, sans-serif !important;
  direction: rtl; text-align: right;
}}
.stApp {{ background: #f3f6f5; }}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {{ display: none !important; }}
.block-container {{ max-width: 1180px !important; padding-top: 1.1rem !important; }}
.{ADMIN_UI} .hero {{
  background: linear-gradient(135deg, #173f44 0%, #245e65 58%, #2f7a72 100%);
  color: #fff; border-radius: 22px; padding: 22px 24px 18px;
  box-shadow: 0 16px 36px rgba(23,63,68,.22); margin-bottom: 16px;
}}
.{ADMIN_UI} .hero b {{ color: #f5c65a; }}
.{ADMIN_UI} .kicker {{ color: #f5c65a; font-size: 13px; letter-spacing: .4px; }}
.{ADMIN_UI} .kpi-grid {{ display:grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap:12px; margin: 14px 0 8px; }}
.{ADMIN_UI} .kpi {{
  background:#fff; border:1px solid #d7e4e1; border-radius:16px; padding:14px 16px;
  box-shadow: 0 8px 18px rgba(23,63,68,.06);
}}
.{ADMIN_UI} .kpi span {{ display:block; color:#5d7370; font-size:13px; }}
.{ADMIN_UI} .kpi strong {{ display:block; color:#173f44; font-size:28px; margin-top:4px; }}
.{ADMIN_UI} .nav-wrap {{ display:flex; gap:12px; margin: 8px 0 16px; }}
.{ADMIN_UI} .nav-card {{
  flex:1; background:#fff; border:1px solid #d7e4e1; border-radius:18px; padding:16px 12px;
  text-align:center; box-shadow: 0 8px 18px rgba(23,63,68,.05);
}}
.{ADMIN_UI} .nav-card .ico {{ font-size:28px; display:block; margin-bottom:6px; }}
.{ADMIN_UI} .nav-card .lbl {{ color:#173f44; font-weight:800; }}
.{ADMIN_UI} .admin-table {{ width:100%; border-collapse:separate; border-spacing:0; background:#fff; border-radius:18px; overflow:hidden; }}
.{ADMIN_UI} .admin-table th {{
  background:#173f44; color:#f5c65a; padding:12px 10px; font-size:13px; text-align:right;
}}
.{ADMIN_UI} .admin-table td {{
  padding:12px 10px; border-bottom:1px solid #e6eeec; color:#173f44; vertical-align:middle;
}}
.{ADMIN_UI} .bar {{ height:8px; background:#e7efed; border-radius:99px; overflow:hidden; min-width:90px; }}
.{ADMIN_UI} .bar i {{ display:block; height:100%; background:linear-gradient(90deg,#245e65,#f5c65a); }}
.{ADMIN_UI} .chip {{
  display:inline-block; background:#eef6f3; color:#245e65; border-radius:999px;
  padding:2px 8px; margin:1px; font-size:12px; font-weight:700;
}}
.{ADMIN_UI} .msg {{
  background:#fff; border:1px solid #d7e4e1; border-radius:16px; padding:14px 16px; margin-bottom:10px;
}}
@media (max-width: 900px) {{
  .{ADMIN_UI} .kpi-grid {{ grid-template-columns: 1fr 1fr; }}
  .{ADMIN_UI} .nav-wrap {{ flex-direction: column; }}
}}
</style>
""",
        unsafe_allow_html=True,
    )


def _esc(value: Any) -> str:
    return html.escape(str(value or ""))


def _pct(raw: Any) -> int:
    try:
        n = float(str(raw).replace("%", "").strip() or 0)
    except Exception:
        n = 0
    return max(0, min(100, int(round(n))))


def _login() -> bool:
    if st.session_state.get("admin_ok"):
        return True
    expected = _admin_password()
    st.markdown(
        f'<div class="{ADMIN_UI}"><div class="hero"><div class="kicker">لوحة الإدارة</div>'
        "<h2>دخول المشرف</h2><p>أدخل كلمة مرور الأدمن لعرض إحصائيات الطلبة والرسائل.</p></div></div>",
        unsafe_allow_html=True,
    )
    if not expected:
        st.warning("أضف كلمة مرور الأدمن في Streamlit Cloud عبر Settings → Secrets ثم أعد تشغيل التطبيق.")
        return False
    with st.form("admin_login_v7"):
        password = st.text_input("كلمة المرور", type="password")
        ok = st.form_submit_button("دخول", use_container_width=True)
    if ok and password == expected:
        st.session_state["admin_ok"] = True
        st.rerun()
    if ok:
        st.error("كلمة المرور غير صحيحة.")
    return False


def _sheets_help() -> None:
    err = last_sheets_error()
    if not sheets_configured():
        st.warning("لم يُضبط Google Sheets بعد. أضف [gsheets] و [gcp_service_account] في Secrets.")
    elif err:
        st.error(err)
        st.caption("بعد مشاركة الجدول كمحرر، اضغط إنشاء جدول جديد إن بقي غير ظاهر.")
        share = st.text_input("إيميل للمشاركة بعد الإنشاء", value="techn47@gmail.com", key="admin_share_email")
        if st.button("إنشاء جدول جديد وربطه", key="admin_create_sheet"):
            try:
                created = create_managed_spreadsheet(share)
                st.success("تم إنشاء الجدول. انسخ المعرف إلى Secrets ثم أعد التشغيل.")
                st.code(created.get("id") or "")
                st.write(created.get("url") or last_created_url())
            except Exception:
                st.error(last_sheets_error() or "تعذر إنشاء الجدول. فعّل Google Drive API.")
    last = last_upsert_name()
    if last:
        st.caption("آخر طالب وصل إلى الجدول: " + last)


def _kpis(students: list[dict[str, Any]], new_msgs: int) -> str:
    grades = {str(s.get("grade") or "").strip() for s in students if str(s.get("grade") or "").strip()}
    avg = 0
    if students:
        avg = round(sum(_pct(s.get("progress")) for s in students) / len(students))
    return (
        f'<div class="kpi-grid">'
        f'<div class="kpi"><span>الطلبة المسجلون</span><strong>{len(students)}</strong></div>'
        f'<div class="kpi"><span>الصفوف النشطة</span><strong>{len(grades)}</strong></div>'
        f'<div class="kpi"><span>متوسط التقدم</span><strong>{avg}%</strong></div>'
        f'<div class="kpi"><span>رسائل جديدة</span><strong>{new_msgs}</strong></div>'
        f'</div>'
    )


def _students_table(students: list[dict[str, Any]]) -> str:
    if not students:
        return '<p style="color:#5d7370">لا يوجد طلبة في الجدول بعد. سجّل طالبًا جديدًا بعد رفع هذا التحديث.</p>'
    rows = []
    for s in students:
        pct = _pct(s.get("progress"))
        badges = "".join(f'<span class="chip">{_esc(b)}</span>' for b in str(s.get("badges") or "").replace("|", ",").split(",") if b.strip()) or "—"
        rows.append(
            "<tr>"
            f'<td><b>{_esc(s.get("name"))}</b><br><small>{_esc(s.get("id"))}</small></td>'
            f'<td>{_esc(s.get("grade"))}</td>'
            f'<td>{_esc(s.get("subjects"))}</td>'
            f'<td><div class="bar"><i style="width:{pct}%"></i></div> {pct}%</td>'
            f'<td>{_esc(s.get("xp"))}</td>'
            f'<td>{badges}</td>'
            f'<td>{_esc(s.get("last_seen"))}</td>'
            "</tr>"
        )
    return (
        '<table class="admin-table"><thead><tr>'
        "<th>الطالب</th><th>الصف</th><th>المواد</th><th>التقدم</th><th>XP</th><th>الأوسمة</th><th>آخر نشاط</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def _messages_page(status: str) -> None:
    title = "رسائل التواصل" if status == "new" else "الرسائل المعالجة"
    st.markdown(
        f'<div class="{ADMIN_UI}"><div class="hero"><div class="kicker">لوحة الإدارة</div>'
        f"<h2>{title}</h2></div></div>",
        unsafe_allow_html=True,
    )
    if st.button("رجوع إلى الرئيسية", key=f"admin_back_{status}"):
        st.session_state["admin_view"] = "home"
        st.rerun()
    rows = list_messages(status)
    if not rows:
        st.info("لا توجد رسائل هنا حاليًا.")
        return
    for row in rows:
        mid = str(row.get("id") or "")
        st.markdown(
            f'<div class="{ADMIN_UI}"><div class="msg"><b>{_esc(row.get("name"))}</b> · {_esc(row.get("subject"))}'
            f'<br><small>{_esc(row.get("created_at"))} · {_esc(row.get("email"))}</small>'
            f'<p>{_esc(row.get("message"))}</p></div></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        if status == "new":
            if cols[0].button("تمت المعالجة", key=f"admin_done_{mid}"):
                update_message_status(mid, "processed")
                st.rerun()
        if cols[1].button("حذف", key=f"admin_del_{status}_{mid}"):
            delete_message(mid)
            st.rerun()


def render_admin_panel() -> None:
    _css()
    if not _login():
        return
    view = st.session_state.get("admin_view") or "home"
    if view == "messages":
        _messages_page("new")
        return
    if view == "processed":
        _messages_page("processed")
        return

    students = list_students() if sheets_configured() else []
    new_msgs = list_messages("new") if sheets_configured() else []
    st.markdown(
        f'<div class="{ADMIN_UI}">'
        '<div class="hero"><div class="kicker">لوحة الإدارة · الطالب الصامد</div>'
        "<h2>متابعة الطلبة والتقدم والأوسمة</h2>"
        f'<p>الجدول المرتبط: <b>{_esc(spreadsheet_key() or "غير مضبوط")}</b></p>'
        f"{_kpis(students, len(new_msgs))}</div>"
        '<div class="nav-wrap">'
        '<div class="nav-card"><span class="ico">✉️</span><span class="lbl">رسائل التواصل</span></div>'
        '<div class="nav-card"><span class="ico">✅</span><span class="lbl">الرسائل المعالجة</span></div>'
        "</div></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    if cols[0].button("فتح رسائل التواصل", key="admin_open_messages"):
        st.session_state["admin_view"] = "messages"
        st.rerun()
    if cols[1].button("فتح الرسائل المعالجة", key="admin_open_processed"):
        st.session_state["admin_view"] = "processed"
        st.rerun()
    _sheets_help()
    st.markdown(f'<div class="{ADMIN_UI}">{_students_table(students)}</div>', unsafe_allow_html=True)
