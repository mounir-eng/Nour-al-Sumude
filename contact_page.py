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

CONTACT_RECIPIENT = "techn47@gmail.com"
CONTACT_PAGE_VERSION = "contact-v17-smtp"
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
<style id="contact-page-v17">
:root{--c-bg:#f8fafc;--c-paper:#fff;--c-ink:#173b3d;--c-muted:#71847f;--c-line:#dfe7e5;--c-deep:#173f44;--c-teal:#286a6d;--c-green:#57967b;--c-gold:#f5c65a;--c-shadow:0 18px 48px rgba(23,63,68,.10);--c-shadow-sm:0 8px 24px rgba(23,63,68,.065)}
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}.stApp,[data-testid="stAppViewContainer"]{background:var(--c-bg)!important;color:var(--c-ink)!important}[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{width:100%!important;max-width:1120px!important;margin:0 auto!important;padding:14px 15px 42px!important}
.contact-nav{display:flex;align-items:center;justify-content:space-between;gap:14px;background:#fff;border:1px solid var(--c-line);border-radius:17px;padding:10px 13px;margin-bottom:13px;box-shadow:0 5px 18px rgba(23,63,68,.04)}.contact-brand{display:flex;align-items:center;gap:10px}.contact-mark{width:42px;height:42px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(145deg,var(--c-deep),#347d78);font-size:20px}.contact-brand b{display:block;font-size:16px}.contact-brand small{display:block;color:var(--c-muted);font-size:10px;margin-top:1px}
.contact-hero{position:relative;isolation:isolate;overflow:hidden;display:grid;grid-template-columns:1.15fr .85fr;gap:28px;align-items:center;background:linear-gradient(125deg,#173f44,#286a6d 58%,#57967b 118%);color:#fff;border-radius:27px;padding:29px 31px;margin-bottom:17px;box-shadow:0 20px 46px rgba(28,88,87,.18)}.contact-hero:after{content:"";position:absolute;width:300px;height:300px;border:65px solid rgba(255,255,255,.045);border-radius:50%;left:-170px;bottom:-225px;z-index:-1}.contact-kicker{display:inline-flex;border:1px solid rgba(255,255,255,.17);background:rgba(255,255,255,.10);border-radius:999px;padding:5px 10px;font-size:10px;font-weight:900}.contact-hero h1{font-size:35px;line-height:1.45;margin:10px 0 6px}.contact-hero p{color:#dcebe8;font-size:13px;line-height:1.95;margin:0;max-width:610px}.contact-facts{display:grid;gap:8px}.contact-fact{display:flex;align-items:center;gap:9px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.13);border-radius:13px;padding:10px}.contact-fact>span{width:34px;height:34px;border-radius:10px;background:rgba(255,255,255,.11);display:grid;place-items:center}.contact-fact b{display:block;font-size:11px}.contact-fact small{display:block;color:#d7e8e4;font-size:9px;margin-top:1px}
.contact-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(260px,.7fr);gap:15px;align-items:start}.contact-card,.contact-side{background:#fff;border:1px solid var(--c-line);border-radius:21px;box-shadow:var(--c-shadow-sm)}.contact-card-head{padding:20px 22px 12px;border-bottom:1px solid #edf1f0}.contact-card-head h2{font-size:22px;margin:0}.contact-card-head p{font-size:11px;color:var(--c-muted);line-height:1.8;margin:4px 0 0}.contact-side{padding:21px}.contact-side h3{font-size:16px;margin:0 0 10px}.contact-side p{font-size:11px;line-height:1.9;color:var(--c-muted);margin:0 0 12px}.contact-mail{direction:ltr;unicode-bidi:isolate;display:block;background:#eef8f4;border:1px solid #d0e8df;color:#235f55;border-radius:12px;padding:10px;text-align:center;font-weight:900;font-size:12px}.contact-note{display:flex;gap:8px;align-items:flex-start;background:#fff8e8;border:1px solid #eedcae;border-radius:13px;padding:11px 12px;color:#735b20;font-size:10px;line-height:1.8;margin-top:12px}.contact-privacy{display:flex;gap:8px;align-items:flex-start;background:#eef8f4;border:1px solid #d0e8df;border-radius:13px;padding:11px 12px;color:#3c685e;font-size:10px;line-height:1.8;margin-top:9px}
.st-key-contact_form_shell{background:#fff!important;border:1px solid var(--c-line)!important;border-top:0!important;border-radius:0 0 21px 21px!important;padding:18px 21px 20px!important;box-shadow:var(--c-shadow-sm)!important;margin-top:-17px!important}.stTextInput label,.stTextArea label{font-weight:900!important;font-size:12px!important;color:var(--c-ink)!important}.stTextInput input,.stTextArea textarea{border:1px solid #cbdad7!important;background:#fbfdfc!important;border-radius:12px!important;font-size:14px!important}.stTextInput input{min-height:46px!important}.stTextArea textarea{min-height:165px!important;line-height:1.8!important}.stTextInput input:focus,.stTextArea textarea:focus{border-color:#347d78!important;box-shadow:0 0 0 4px rgba(52,125,120,.11)!important}.stFormSubmitButton>button,.stButton>button,.stLinkButton a{border-radius:12px!important;min-height:44px!important;font-weight:900!important}.stFormSubmitButton>button{background:var(--c-deep)!important;color:#fff!important;border:1px solid var(--c-deep)!important}.stButton>button{background:#fff!important;color:var(--c-ink)!important;border:1px solid var(--c-line)!important}.stAlert{border-radius:14px!important}
.contact-bottom{margin-top:18px;background:linear-gradient(135deg,#173f44,#245e65);color:#fff;border-radius:19px;padding:16px 19px;display:flex;justify-content:space-between;gap:15px;align-items:center}.contact-bottom b{font-size:13px}.contact-bottom span{font-size:10px;color:#d3e5e2}
@media(max-width:800px){section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{padding:8px 9px 30px!important}.contact-hero{grid-template-columns:1fr;padding:23px 18px;border-radius:22px}.contact-hero h1{font-size:29px}.contact-grid{grid-template-columns:1fr}.st-key-contact_form_shell{padding:16px 14px!important}.contact-card-head{padding:18px 16px 11px}.contact-bottom{display:grid;text-align:center}.contact-brand small{display:none}}
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
    config = _smtp_config()
    if config is None:
        raise RuntimeError("CONTACT_EMAIL_NOT_CONFIGURED")
    safe_subject = _clean_header(subject, 150)
    sent_at = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    plain = (
        "رسالة جديدة من منصة الطالب الصامد\n"
        "================================\n\n"
        f"الاسم: {name}\n"
        f"البريد الإلكتروني: {email}\n"
        f"المؤسسة: {institution}\n"
        f"الموضوع: {safe_subject}\n"
        f"وقت الإرسال: {sent_at}\n\n"
        "نص الرسالة:\n"
        f"{message}\n"
    )
    rich = f"""
    <div dir="rtl" style="font-family:Arial,Tahoma,sans-serif;line-height:1.8;color:#173b3d">
      <h2 style="color:#245e65">رسالة جديدة من منصة الطالب الصامد</h2>
      <table style="border-collapse:collapse;width:100%;max-width:700px">
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>الاسم</b></td><td style="padding:7px;border:1px solid #dfe7e5">{html.escape(name)}</td></tr>
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>البريد الإلكتروني</b></td><td dir="ltr" style="padding:7px;border:1px solid #dfe7e5;text-align:left">{html.escape(email)}</td></tr>
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>المؤسسة</b></td><td style="padding:7px;border:1px solid #dfe7e5">{html.escape(institution)}</td></tr>
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>الموضوع</b></td><td style="padding:7px;border:1px solid #dfe7e5">{html.escape(safe_subject)}</td></tr>
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>وقت الإرسال</b></td><td dir="ltr" style="padding:7px;border:1px solid #dfe7e5;text-align:left">{sent_at}</td></tr>
      </table>
      <h3>نص الرسالة</h3><div style="white-space:pre-wrap;background:#f8fafc;border:1px solid #dfe7e5;border-radius:12px;padding:14px">{html.escape(message)}</div>
    </div>
    """
    mail = EmailMessage()
    mail["Subject"] = f"[الطالب الصامد] {safe_subject}"
    mail["From"] = formataddr(("منصة الطالب الصامد", str(config["sender"])))
    mail["To"] = CONTACT_RECIPIENT
    mail["Reply-To"] = _clean_header(email, 254)
    mail.set_content(plain)
    mail.add_alternative(rich, subtype="html")
    context = ssl.create_default_context()
    if int(config["port"]) == 465:
        with smtplib.SMTP_SSL(str(config["host"]), int(config["port"]), timeout=20, context=context) as smtp:
            smtp.login(str(config["username"]), str(config["password"]))
            smtp.send_message(mail)
    else:
        with smtplib.SMTP(str(config["host"]), int(config["port"]), timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(str(config["username"]), str(config["password"]))
            smtp.send_message(mail)


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
    nav_copy, nav_button = st.columns([4, 1])
    with nav_copy:
        st.markdown(
            '<div class="contact-nav"><div class="contact-brand"><span class="contact-mark">🛡️</span>'
            '<span><b>الطالب الصامد</b><small>صفحة التواصل والدعم</small></span></div>'
            '<span style="font-size:10px;color:#71847f">رسالتك تصل إلى فريق المنصة</span></div>',
            unsafe_allow_html=True,
        )
    with nav_button:
        if st.button("← الرجوع", key="contact_back_top", use_container_width=True):
            _return_to_platform()

    st.markdown(
        '<section class="contact-hero"><div><span class="contact-kicker">✉️ تواصل معنا</span>'
        '<h1>يسعدنا أن نسمع منك</h1><p>أرسل اقتراحًا، بلّغ عن مشكلة، أو اطلب تعاونًا تعليميًا. '
        'سنستقبل الرسالة مباشرة عبر البريد الإلكتروني للمنصة.</p></div>'
        '<div class="contact-facts"><div class="contact-fact"><span>📬</span><div><b>إرسال مباشر وآمن</b><small>لا نعرض بريدك للعموم</small></div></div>'
        '<div class="contact-fact"><span>🌐</span><div><b>يتطلب اتصالًا بالإنترنت</b><small>أما الدروس المحمّلة فتبقى أوفلاين</small></div></div>'
        '<div class="contact-fact"><span>↩️</span><div><b>الرد على بريدك</b><small>تأكد من كتابة البريد بشكل صحيح</small></div></div></div></section>',
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
                    name = st.text_input("الاسم الكامل *", value=default_name, max_chars=120, placeholder="اكتب اسمك الكامل")
                with c2:
                    email = st.text_input("البريد الإلكتروني *", max_chars=254, placeholder="name@example.com")
                c3, c4 = st.columns(2)
                with c3:
                    institution = st.text_input("المؤسسة *", max_chars=180, placeholder="المدرسة، الجامعة أو المؤسسة")
                with c4:
                    subject = st.text_input("الموضوع *", max_chars=150, placeholder="موضوع الرسالة باختصار")
                message = st.text_area("نص الرسالة *", max_chars=4000, placeholder="اكتب تفاصيل رسالتك بوضوح...", height=190)
                submitted = st.form_submit_button("إرسال الرسالة إلى المنصة ←", type="primary", use_container_width=True)

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
                        if str(exc) == "CONTACT_EMAIL_NOT_CONFIGURED":
                            st.error("الإرسال المباشر غير مهيأ بعد. يجب على مدير المنصة إضافة إعدادات البريد الآمنة في Streamlit Cloud.")
                        else:
                            st.error("تعذر إرسال الرسالة الآن. حاول مرة أخرى لاحقًا.")
                        mailto = (
                            f"mailto:{CONTACT_RECIPIENT}?subject={quote('[الطالب الصامد] ' + subject)}"
                            f"&body={quote('الاسم: ' + name + chr(10) + 'البريد: ' + email + chr(10) + 'المؤسسة: ' + institution + chr(10) + chr(10) + message)}"
                        )
                        st.link_button("فتح تطبيق البريد كخيار بديل", mailto, use_container_width=True)
                    except (smtplib.SMTPException, OSError, TimeoutError):
                        st.error("تعذر الاتصال بخدمة البريد الآن. تحقق من الإنترنت ثم حاول مجددًا.")
                    else:
                        st.session_state["_contact_last_sent"] = time.time()
                        st.success("تم إرسال رسالتك بنجاح إلى techn47@gmail.com. شكرًا لتواصلك معنا.")

    with right:
        st.markdown(
            '<aside class="contact-side"><h3>معلومات التواصل</h3><p>تُرسل الرسائل إلى البريد الرسمي التالي، ويمكن لفريق المنصة الرد مباشرة على البريد الذي تكتبه في النموذج.</p>'
            '<span class="contact-mail">techn47@gmail.com</span>'
            '<div class="contact-note"><span>⏱️</span><span>قد يتأخر الرد بحسب توفر الاتصال وظروف العمل، لكن رسالتك ستصل فور نجاح الإرسال.</span></div>'
            '<div class="contact-privacy"><span>🔒</span><span>لا تكتب كلمة المرور أو أي بيانات حساسة داخل الرسالة.</span></div></aside>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="contact-bottom"><b>© الطالب الصامد · منصة تعليمية لخدمة طلبة غزة</b>'
        '<span>تشغيل أونلاين وأوفلاين على سطح المكتب واللوحات والهاتف</span></div>',
        unsafe_allow_html=True,
    )
