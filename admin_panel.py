"""صفحة أدمن محمية — تُفتح عبر ?admin=1 ولا تظهر للطلبة."""
from __future__ import annotations

import hmac
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from student_cloud_sync import is_configured, list_contact_messages, list_students

_ADMIN_CSS = """
<style id="samed-admin-gate">
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f7f8f6!important;color:#173b3d!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{max-width:1280px!important;padding:18px 16px 28px!important}
.admin-box{background:#fff;border:1px solid #dce6e3;border-radius:18px;padding:22px;max-width:460px;margin:12vh auto 0;box-shadow:0 10px 28px rgba(23,63,68,.08)}
.admin-box h1{font-size:26px;margin:0 0 6px}
.admin-box p{color:#6f827e;font-size:14px;line-height:1.8;margin:0 0 16px}
.pending-box{background:#fff;border:1px solid #dce6e3;border-radius:16px;padding:16px;margin:0 0 16px}
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


def _render_pending_teachers() -> None:
    try:
        from accounts import approve_teacher, list_pending_teachers, reject_teacher
    except Exception:
        return
    try:
        pending = list_pending_teachers()
    except Exception as exc:
        st.error("تعذر قراءة طلبات الأساتذة.")
        st.caption(str(exc)[:240])
        return
    st.markdown('<div class="pending-box">', unsafe_allow_html=True)
    st.subheader("طلبات تسجيل الأساتذة")
    if not pending:
        st.caption("لا توجد طلبات بانتظار الموافقة.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    for row in pending:
        cols = st.columns([3, 2, 1, 1])
        with cols[0]:
            st.markdown(f"**{row.get('name') or 'أستاذ'}**")
        with cols[1]:
            st.caption(row.get("email") or "")
        with cols[2]:
            if st.button("موافقة", key=f"ok-{row['id']}", type="primary"):
                approve_teacher(row["id"])
                st.rerun()
        with cols[3]:
            if st.button("رفض", key=f"no-{row['id']}"):
                reject_teacher(row["id"])
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)



def _render_contact_messages() -> None:
    st.markdown('<div class="pending-box">', unsafe_allow_html=True)
    st.subheader("رسائل التواصل")
    if not is_configured():
        st.caption("اربط Google Sheets لتظهر رسائل صفحة التواصل هنا.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    try:
        messages = list_contact_messages()
    except Exception as exc:
        st.error("تعذر قراءة رسائل التواصل.")
        st.caption(str(exc)[:240])
        st.markdown("</div>", unsafe_allow_html=True)
        return
    if not messages:
        st.caption("لا توجد رسائل بعد.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    for row in messages[:40]:
        name = row.get("name") or "بدون اسم"
        subject = row.get("subject") or "بدون موضوع"
        created = str(row.get("created_at") or "")[:19].replace("T", " ")
        with st.expander(f"{name} · {subject} · {created}"):
            st.write(f"البريد: {row.get('email') or '—'}")
            st.write(f"المؤسسة: {row.get('institution') or '—'}")
            st.write(row.get("message") or "")
    st.markdown("</div>", unsafe_allow_html=True)

def render_admin_panel() -> None:
    st.markdown(_ADMIN_CSS, unsafe_allow_html=True)
    expected = _admin_password()
    if not expected:
        st.markdown('<div class="admin-box"><h1>لوحة الإدارة</h1><p>أضف كلمة مرور الأدمن في Streamlit Cloud عبر Settings → Secrets ثم أعد تشغيل التطبيق.</p></div>', unsafe_allow_html=True)
        st.code('[admin]\npassword = "كلمة-مرور-خاصة-بك"', language="toml")
        st.stop()

    if not st.session_state.get("samed_admin_ok"):
        st.markdown('<div class="admin-box"><h1>دخول الأدمن</h1><p>هذه الصفحة للمشرف فقط. الطلبة لا يرونها في القائمة.</p></div>', unsafe_allow_html=True)
        entered = st.text_input("كلمة مرور الأدمن", type="password", key="samed_admin_password")
        if st.button("دخول", type="primary"):
            if _passwords_match(entered.strip(), expected):
                st.session_state["samed_admin_ok"] = True
                st.rerun()
            st.error("كلمة المرور غير صحيحة.")
        st.stop()

    _render_pending_teachers()
    _render_contact_messages()

    live = False
    students: list[dict] | None = None
    if is_configured():
        try:
            students = list_students()
            live = True
        except Exception as exc:
            st.error("تعذر قراءة جدول Google Sheets. تحقق من مشاركة الجدول مع إيميل حساب الخدمة.")
            st.caption(str(exc)[:240])
            students = []
            live = True
    else:
        st.warning("لم يُضبط Google Sheets بعد، لذلك تُعرض بيانات تجريبية. راجع ملف ADMIN_SYNC_AR.txt.")

    html_path = Path(__file__).with_name("admin_dashboard.html")
    html = html_path.read_text(encoding="utf-8")
    if live:
        payload = json.dumps(students or [], ensure_ascii=False)
        html = html.replace(
            "/*__STUDENTS_INJECT__*/",
            f"window.SAMED_LIVE=true;window.SAMED_ROLE='admin';window.SAMED_STUDENTS={payload};",
        )
    else:
        html = html.replace("/*__STUDENTS_INJECT__*/", "window.SAMED_ROLE='admin';")
    components.html(html, height=900, scrolling=True)
