"""Secure online contact page for the Student Samed platform."""
from __future__ import annotations

import html
import os
import re
import smtplib
import ssl
import time
from email.message import EmailMessage
from email.utils import formataddr
from urllib.parse import quote

import streamlit as st

CONTACT_PAGE_VERSION = "contact-v20"
_ALLOWED_RETURN_PAGES = {
    "app.py",
    "pages/physics_textbook_exercises.py",
    "pages/chemistry_textbook_exercises.py",
    "pages/chemistry_unit_1.py",
    "pages/physics_foundation.py",
    "pages/physics_unit_review.py",
    "pages/chemistry_foundation.py",
    "pages/chemistry_unit_review.py",
}

_CONTACT_CSS = r"""
<style id="contact-page-v19">
:root{--c-bg:#f6f8f7;--c-paper:#fff;--c-ink:#173b3d;--c-muted:#6b7f7b;--c-line:#dfe7e5;--c-deep:#173f44}
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}
.stApp,[data-testid="stAppViewContainer"]{background:var(--c-bg)!important;color:var(--c-ink)!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{width:100%!important;max-width:980px!important;margin:0 auto!important;padding:12px 14px 28px!important}
.contact-nav{display:flex;align-items:center;justify-content:space-between;gap:10px;background:#fff;border:1px solid var(--c-line);border-radius:14px;padding:8px 12px;margin-bottom:12px}
.contact-brand{display:flex;align-items:center;gap:8px}.contact-mark{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:linear-gradient(145deg,#173f44,#347d78);font-size:18px}
.contact-brand b{display:block;font-size:15px}.contact-brand small{display:block;color:var(--c-muted);font-size:11px}
.contact-hero{background:linear-gradient(125deg,#173f44,#286a6d 70%);color:#fff;border-radius:18px;padding:16px 18px 14px;margin-bottom:12px}
.contact-kicker{display:inline-flex;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.1);border-radius:999px;padding:3px 9px;font-size:11px;font-weight:800}
.contact-hero h1{font-size:24px;line-height:1.35;margin:8px 0 4px}
.contact-hero>div>p{color:#dcebe8;font-size:13px;line-height:1.7;margin:0 0 12px;max-width:52ch}
.contact-facts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.contact-fact{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:8px 6px}
.contact-fact>span{width:28px;height:28px;border-radius:9px;background:rgba(255,255,255,.16);display:grid;place-items:center;font-size:14px}
.contact-fact b{display:block;font-size:12px;line-height:1.4;font-weight:800}
.contact-fact small{display:block;color:#d7e8e4;font-size:10px;line-height:1.4;margin:0}
.contact-card,.contact-side{background:#fff;border:1px solid var(--c-line);border-radius:16px}
.contact-card-head{padding:12px 16px 8px;border-bottom:1px solid #edf1f0}
.contact-card-head h2{font-size:18px;margin:0}.contact-card-head p{font-size:12px;color:var(--c-muted);margin:4px 0 0;line-height:1.6}
.contact-side{padding:14px 16px}.contact-side h3{font-size:15px;margin:0 0 6px}.contact-side p{font-size:12px;line-height:1.7;color:var(--c-muted);margin:0 0 10px}
.contact-note,.contact-privacy{display:flex;gap:8px;align-items:flex-start;border-radius:10px;padding:8px 10px;font-size:12px;line-height:1.6;margin-top:8px}
.contact-note{background:#fff8e8;border:1px solid #eedcae;color:#735b20}
.contact-privacy{background:#eef8f4;border:1px solid #d0e8df;color:#3c685e}
.c-label{display:block!important;visibility:visible!important;font-weight:800!important;font-size:13px!important;color:#173b3d!important;margin:0 0 6px!important;line-height:1.4!important}
.st-key-contact_form_shell{background:#fff!important;border:1px solid var(--c-line)!important;border-top:0!important;border-radius:0 0 16px 16px!important;padding:12px 16px 14px!important;margin-top:-10px!important}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p,.stTextInput label,.stTextArea label{display:flex!important;visibility:visible!important;height:auto!important;overflow:visible!important;color:#173b3d!important;font-weight:800!important;font-size:13px!important;margin-bottom:4px!important}
[data-testid="InputInstructions"]{display:none!important}
.stTextInput input,.stTextArea textarea{border:1px solid #cbdad7!important;background:#fff!important;border-radius:10px!important;font-size:14px!important}
.stTextInput input{min-height:44px!important}.stTextArea textarea{min-height:120px!important}
.stFormSubmitButton>button{background:#173f44!important;color:#fff!important;border:0!important;border-radius:12px!important;min-height:44px!important;font-weight:800!important}
.stButton>button{background:#fff!important;color:#173b3d!important;border:1px solid var(--c-line)!important;border-radius:12px!important;min-height:40px!important;font-weight:800!important}
.contact-bottom{margin-top:12px;background:#173f44;color:#fff;border-radius:14px;padding:12px 16px;display:flex;justify-content:space-between;gap:10px;align-items:center;font-size:12px}
@media(max-width:800px){.contact-facts{grid-template-columns:1fr 1fr 1fr}.contact-hero{padding:14px}.contact-hero h1{font-size:22px}.contact-bottom{display:grid;text-align:center}}
</style>
"""
def _cfg_value(config: dict, name: str, env_name: str, default: object = "") -> object:
    value = config.get(name, os.getenv(env_name, default))
    return value if value is not None else default


def _smtp_config() -> dict[str, object] | None:
    try:
        config = dict(st.secrets.get("contact_email", {}))
    except Exception:
        config = {}
    username = str(_cfg_value(config, "username", "CONTACT_SMTP_USERNAME", "")).strip()
    password = str(_cfg_value(config, "app_password", "CONTACT_SMTP_APP_PASSWORD", "")).replace(" ", "").strip()
    if not username or not password:
        return None
    try:
        port = int(_cfg_value(config, "smtp_port", "CONTACT_SMTP_PORT", 465))
    except (TypeError, ValueError):
        port = 465
    return {
        "host": str(_cfg_value(config, "smtp_host", "CONTACT_SMTP_HOST", "smtp.gmail.com")).strip(),
        "port": port,
        "username": username,
        "password": password,
        "sender": str(_cfg_value(config, "sender_email", "CONTACT_SENDER_EMAIL", username)).strip() or username,
    }


def _valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", value.strip()))


def _clean_header(value: str, limit: int) -> str:
    return " ".join(value.replace("\r", " ").replace("\n", " ").split())[:limit]


def _send_message(*, name: str, email: str, institution: str, subject: str, message: str) -> None:
    from student_cloud_sync import save_contact_message
    if not save_contact_message(name=name, email=email, institution=institution, subject=subject, message=message):
        raise RuntimeError("CONTACT_INBOX_NOT_CONFIGURED")


def _return_to_platform() -> None:
    target = str(st.session_state.get("_contact_return_page", "app.py"))
    if target not in _ALLOWED_RETURN_PAGES:
        target = "app.py"
    if target == "app.py":
        view = str(st.session_state.get("_contact_return_view", "home"))
        st.session_state["samed_view"] = view if view in {"home", "dashboard", "app"} else "home"
    st.switch_page(target)


def render_contact_page() -> None:
    st.markdown(_CONTACT_CSS, unsafe_allow_html=True)
    nav_copy, nav_home, nav_out = st.columns([3.2, 1, 1])
    with nav_copy:
        st.markdown(
            '<div class="contact-nav"><div class="contact-brand"><span class="contact-mark">🛡️</span>'
            '<span><b>الطالب الصامد</b><small>صفحة التواصل · v20</small></span></div></div>',
            unsafe_allow_html=True,
        )
    with nav_home:
        if st.button("الرئيسية", key="contact_home_top", use_container_width=True):
            st.session_state["samed_view"] = "home"
            st.switch_page("app.py")
    with nav_out:
        if st.button("تسجيل الخروج", key="contact_logout_top", use_container_width=True):
            for key in ("student_profile", "teacher_profile", "samed_role", "student_name"):
                st.session_state[key] = None
            st.session_state["samed_teacher_learn"] = False
            st.session_state["samed_view"] = "home"
            st.switch_page("app.py")

    st.markdown(
        '<section class="contact-hero"><div><span class="contact-kicker">✉️ تواصل معنا</span>'
        '<h1>يسعدنا أن نسمع منك</h1><p>أرسل اقتراحًا أو استفسارًا أو طلب تعاون، وسنعود إليك في أقرب فرصة.</p>'
        '<div class="contact-facts"><div class="contact-fact"><span>✍️</span><b>اكتب بياناتك بوضوح</b><small>لنتمكن من الرد عليك</small></div>'
        '<div class="contact-fact"><span>🌐</span><b>يلزم اتصال بالإنترنت</b><small>لإرسال الرسالة فقط</small></div>'
        '<div class="contact-fact"><span>🔒</span><b>خصوصيتك مهمة</b><small>لا تكتب كلمة المرور هنا</small></div></div></div></section>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.55, .72], gap="medium")
    with left:
        st.markdown(
            '<section class="contact-card"><div class="contact-card-head"><h2>اكتب رسالتك</h2>'
            '<p>جميع الحقول مطلوبة. لن تُرسل الرسالة قبل التحقق من البيانات.</p></div></section>',
            unsafe_allow_html=True,
        )
        with st.container(key="contact_form_shell"):
            default_name = str((st.session_state.get("student_profile") or {}).get("name", ""))
            with st.form("contact_form_v17", clear_on_submit=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<span class="c-label">الاسم الكامل *</span>', unsafe_allow_html=True)
                    name = st.text_input("الاسم الكامل *", value=default_name, placeholder="اكتب اسمك الكامل", label_visibility="collapsed")
                with c2:
                    st.markdown('<span class="c-label">البريد الإلكتروني *</span>', unsafe_allow_html=True)
                    email = st.text_input("البريد الإلكتروني *", placeholder="name@example.com", label_visibility="collapsed")
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown('<span class="c-label">المؤسسة *</span>', unsafe_allow_html=True)
                    institution = st.text_input("المؤسسة *", placeholder="المدرسة، الجامعة أو المؤسسة", label_visibility="collapsed")
                with c4:
                    st.markdown('<span class="c-label">الموضوع *</span>', unsafe_allow_html=True)
                    subject = st.text_input("الموضوع *", placeholder="موضوع الرسالة باختصار", label_visibility="collapsed")
                st.markdown('<span class="c-label">نص الرسالة *</span>', unsafe_allow_html=True)
                message = st.text_area("نص الرسالة *", placeholder="اكتب تفاصيل رسالتك بوضوح...", height=130, label_visibility="collapsed")
                submitted = st.form_submit_button("إرسال الرسالة", type="primary", use_container_width=True)

            if submitted:
                name = name.strip()
                email = email.strip()
                institution = institution.strip()
                subject = subject.strip()
                message = message.strip()
                error = ""
                if len(name) < 2:
                    error = "يرجى كتابة اسم صحيح من حرفين على الأقل."
                elif not _valid_email(email):
                    error = "يرجى كتابة بريد إلكتروني صحيح."
                elif len(institution) < 2:
                    error = "يرجى كتابة اسم المؤسسة."
                elif len(subject) < 3:
                    error = "يرجى كتابة موضوع واضح للرسالة."
                elif len(message) < 10:
                    error = "يرجى كتابة رسالة أوضح من 10 أحرف على الأقل."
                last_sent = float(st.session_state.get("_contact_last_sent", 0) or 0)
                if not error and time.time() - last_sent < 45:
                    error = "تم إرسال رسالة مؤخرًا. انتظر قليلًا قبل إرسال رسالة أخرى."
                if error:
                    st.warning(error)
                else:
                    try:
                        _send_message(name=name, email=email, institution=institution, subject=subject, message=message)
                    except RuntimeError as exc:
                        st.error("تعذر إرسال الرسالة الآن. حاول مرة أخرى لاحقًا.")
                    except Exception:
                        st.error("تعذر إرسال الرسالة الآن. تحقق من الاتصال ثم حاول مجددًا.")
                    else:
                        st.session_state["_contact_last_sent"] = time.time()
                        st.success("تم الإرسال بنجاح سيتم التواصل معكم نشكركم على تواصلكم.")

    with right:
        st.markdown(
            '<aside class="contact-side"><h3>نصائح سريعة</h3><p>اكتب اسمك وبريدك وموضوعًا واضحًا حتى نتمكن من مساعدتك بسرعة.</p>'
            '<div class="contact-note"><span>⏱️</span><span>قد يتأخر الرد قليلًا بحسب ضغط العمل. سنعود إليك عبر البريد الذي كتبته.</span></div>'
            '<div class="contact-privacy"><span>🔒</span><span>لا تكتب كلمة المرور أو أي بيانات حساسة داخل الرسالة.</span></div></aside>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="contact-bottom"><b>© الطالب الصامد · منصة تعليمية لخدمة طلبة غزة</b>'
        '<span>تشغيل أونلاين وأوفلاين على سطح المكتب واللوحات والهاتف</span></div>',
        unsafe_allow_html=True,
    )
