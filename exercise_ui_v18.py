"""واجهة احترافية موحّدة لصفحات التمارين — إصدار v18."""
from __future__ import annotations

import re

import streamlit as st

EXERCISE_UI_VERSION = "exercise-ui-v18-professional-header"

_EXERCISE_CSS = r"""
<style id="exercise-ui-v18">
:root{--ex-bg:#f7faf9;--ex-paper:#fff;--ex-ink:#173b3d;--ex-muted:#6c817d;--ex-line:#dbe6e3;--ex-deep:#173f44;--ex-teal:#286a6d;--ex-green:#57967b;--ex-gold:#f2c457;--ex-shadow:0 18px 48px rgba(23,63,68,.11);--ex-shadow-sm:0 8px 25px rgba(23,63,68,.07)}html{box-sizing:border-box}*,*:before,*:after{box-sizing:inherit}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--ex-bg)!important;color:var(--ex-ink)!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
section[data-testid="stMain"]{width:100%!important;max-width:100%!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{width:100%!important;max-width:1240px!important;margin:0 auto!important;padding:12px 16px 42px!important;direction:rtl!important}
[data-testid="stMarkdownContainer"],.stSelectbox,.stToggle,.stButton,.stCaptionContainer{font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}

/* رأس صفحة التمارين — بنية فعلية جديدة لا تعتمد على تنسيق الرأس القديم */
.exercise-head-v18{position:relative;isolation:isolate;overflow:hidden;display:grid;grid-template-columns:minmax(0,1fr) 245px;gap:22px;align-items:center;background:linear-gradient(125deg,#173f44 0%,#286a6d 58%,#57967b 118%);color:#fff;border-radius:26px;padding:25px 27px;box-shadow:0 20px 48px rgba(28,88,87,.19);margin:0 0 10px;min-height:0}
.exercise-head-v18:before{content:"";position:absolute;width:300px;height:300px;border:62px solid rgba(255,255,255,.045);border-radius:50%;left:-170px;bottom:-225px;z-index:-1}.exercise-head-v18:after{content:"";position:absolute;width:145px;height:145px;background:rgba(255,255,255,.045);border-radius:50%;left:170px;top:-105px;z-index:-1}
.exercise-head-brand{display:flex;align-items:center;gap:12px;margin-bottom:13px}.exercise-head-mark{width:48px;height:48px;flex:0 0 48px;border-radius:15px;display:grid;place-items:center;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.16);font-size:24px}.exercise-head-brand b{display:block;font-size:20px;line-height:1.3}.exercise-head-brand small{display:block;color:#d7e9e5;font-size:10px;margin-top:2px}.exercise-head-kicker{display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.09);border-radius:999px;padding:5px 10px;font-size:10px;font-weight:900}.exercise-head-v18 h1{font-size:clamp(25px,2.7vw,37px);line-height:1.45;letter-spacing:-.5px;margin:8px 0 5px;color:#fff}.exercise-head-v18 p{font-size:12px;line-height:1.9;color:#d8e9e6;margin:0;max-width:760px}.exercise-head-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:13px}.exercise-head-chips span{border:1px solid rgba(255,255,255,.13);background:rgba(255,255,255,.09);border-radius:999px;padding:5px 9px;font-size:9.5px;font-weight:800}.exercise-head-side{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:17px;backdrop-filter:blur(7px)}.exercise-head-side strong{display:block;font-size:14px}.exercise-head-side p{font-size:10px;line-height:1.75;margin:5px 0 11px}.exercise-open-badge{display:flex;align-items:center;gap:7px;background:#fff;color:#245e65;border-radius:11px;padding:9px 10px;font-size:10px;font-weight:900}.exercise-version{display:inline-flex;margin-top:9px;color:#d6e8e4;font-size:8.5px;direction:ltr;unicode-bidi:isolate}
.st-key-exercise_header_actions{margin:0 0 12px!important;background:#fff!important;border:1px solid var(--ex-line)!important;border-radius:15px!important;padding:8px 10px!important;box-shadow:0 5px 17px rgba(23,63,68,.045)!important}.st-key-exercise_header_actions [data-testid="stHorizontalBlock"]{align-items:center!important}.exercise-breadcrumb{display:flex;align-items:center;gap:7px;color:#617873;font-size:11px;font-weight:850;min-height:42px}.exercise-breadcrumb b{color:#245e65}.st-key-exercise_header_actions .stButton>button{min-height:42px!important;border-radius:11px!important;background:#f8fbfa!important;color:#245e65!important;border:1px solid #d7e4e1!important;font-weight:900!important}.st-key-exercise_header_actions .stButton>button:hover{background:#eaf6f2!important;border-color:#a9cec4!important}.tip-box-v18{display:flex;align-items:flex-start;gap:9px;background:#fff9e8;border:1px solid #eddba8;border-right:5px solid var(--ex-gold);color:#72591d;border-radius:14px;padding:11px 14px;margin:0 0 14px;font-size:12px;line-height:1.85;box-shadow:none}

/* ملف الطالب يندمج في أعلى الصفحة دون زر عائم مزعج */
.st-key-avatar_row{height:0!important;min-height:0!important;margin:0!important;overflow:visible!important;position:relative!important;z-index:40!important}.st-key-avatar_row>[data-testid="stHorizontalBlock"]{height:0!important;min-height:0!important;margin:0!important}.st-key-profile_pop{position:absolute!important;left:18px!important;top:18px!important;width:auto!important;z-index:45!important}.st-key-profile_pop div[data-testid="stPopover"]>button{width:43px!important;min-width:43px!important;height:43px!important;min-height:43px!important;border-radius:13px!important;background:#fff!important;color:#245e65!important;border:1px solid #d7e4e1!important;box-shadow:0 7px 20px rgba(23,63,68,.08)!important;font-size:15px!important;padding:0!important}

/* شريط اختيار التمرين */
.st-key-exercise_nav{background:transparent!important;margin:2px 0 8px!important}.st-key-exercise_nav .stButton>button{background:#fff!important;color:var(--ex-ink)!important;border:1px solid var(--ex-line)!important;box-shadow:0 4px 14px rgba(23,63,68,.035)!important}.st-key-exercise_controls{background:#fff!important;border:1px solid var(--ex-line)!important;border-radius:18px!important;padding:14px 16px 9px!important;margin:0 0 15px!important;box-shadow:var(--ex-shadow-sm)!important}.st-key-exercise_controls [data-testid="stHorizontalBlock"]{align-items:end!important;gap:14px!important}.st-key-exercise_controls label{font-size:12px!important;font-weight:900!important;color:var(--ex-ink)!important}.st-key-exercise_controls [data-baseweb="select"]>div{min-height:48px!important;background:#f9fbfb!important;border-color:#cadbd7!important;border-radius:13px!important}.st-key-exercise_controls [data-testid="stToggle"] label{min-height:48px!important;background:#f3f8f6!important;border:1px solid #d6e5e1!important;border-radius:13px!important;padding:9px 12px!important}

/* بطاقة السؤال مبنية بعناصر Streamlit منفصلة؛ لا يوجد HTML متداخل يمكن أن يظهر كنص */
div[data-testid="stHorizontalBlock"]:has([class*="st-key-question_card_"]){align-items:stretch!important;gap:12px!important}div[data-testid="stHorizontalBlock"]:has([class*="st-key-question_card_"])>div[data-testid="stColumn"]:first-child{flex:1 1 auto!important;width:auto!important;min-width:0!important}div[data-testid="stHorizontalBlock"]:has([class*="st-key-question_card_"])>div[data-testid="stColumn"]:last-child{flex:0 0 175px!important;width:175px!important;min-width:175px!important;align-self:flex-start!important}
[class*="st-key-question_card_"] div[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border:1px solid var(--ex-line)!important;border-right:6px solid #286a6d!important;border-radius:21px!important;padding:5px!important;box-shadow:var(--ex-shadow-sm)!important;overflow:hidden!important}[class*="st-key-question_card_"] [data-testid="stVerticalBlock"]{gap:.45rem!important}.exercise-question-chip{display:inline-flex;width:max-content;border-radius:999px;padding:5px 10px;background:#dcf7ea;color:#196344;font-size:10px;font-weight:900}.exercise-question-chip.proof{background:#f1eafd;color:#64469a}.exercise-question-title{font-size:clamp(23px,2.3vw,31px);line-height:1.65;letter-spacing:-.35px;color:#173b3d;margin:2px 0 0}.exercise-question-text{font-size:17px;line-height:2.05;color:#314f50;margin:0;unicode-bidi:plaintext}.exercise-question-meta{display:flex;align-items:center;gap:7px;color:#71847f;font-size:11px;font-weight:800}.stProgress>div>div>div>div{background:linear-gradient(90deg,#286a6d,#57967b)!important}.fig-box{border-radius:16px!important;overflow:hidden!important;border:1px solid var(--ex-line)!important}
div[data-testid="stHorizontalBlock"]:has([class*="st-key-question_card_"])>div[data-testid="stColumn"]:last-child .stButton>button{background:#fff!important;border:1px solid var(--ex-line)!important;color:#48605d!important;min-height:44px!important;font-size:11px!important}
hr{border:0!important;border-top:1px solid #e3eae8!important;margin:20px 0!important}#phys-steps-anchor{font-size:22px!important;line-height:1.6!important;margin:3px 0!important;color:#173b3d!important}.stCaptionContainer{color:#71847f!important;font-size:12px!important}

/* بطاقات خطوات الحل */
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:18px!important;border-color:var(--ex-line)!important;background:#fff!important;box-shadow:0 6px 18px rgba(23,63,68,.045)!important;overflow:hidden!important}[class*="stepstate_active"] div[data-testid="stVerticalBlockBorderWrapper"]{border-color:#91bdb4!important;box-shadow:0 10px 28px rgba(40,106,109,.12)!important}.step-badge{border-radius:999px!important;padding:5px 9px!important;font-size:10px!important}.law-guide-box,.explain-box,.hint-box,.note-box,.result-box,.micro-box{border-radius:14px!important}.law-guide-box{background:#f0f8f5!important;border-color:#cde4dd!important;color:#285f57!important}.explain-box{font-size:14px!important;line-height:1.9!important}.formula-text,.eq-box,.result-eq,.law-eq,.eq-inline{direction:ltr!important;unicode-bidi:isolate!important;text-align:center!important}.law-note,.result-note{direction:rtl!important;unicode-bidi:isolate!important}.stTextInput input,.stNumberInput input{font-size:16px!important;min-height:45px!important;border-radius:12px!important}.stButton>button,.stFormSubmitButton>button{border-radius:12px!important;min-height:43px!important;font-weight:900!important}
#phys-dock .phys-pane{border:1px solid var(--ex-line)!important;border-radius:18px!important;box-shadow:0 18px 45px rgba(23,63,68,.16)!important;background:#fff!important}#phys-dock .phys-ic{background:#fff!important;border-color:#cadbd7!important;color:var(--ex-teal)!important;box-shadow:0 7px 20px rgba(23,63,68,.08)!important}#phys-dock .phys-ic.on{background:var(--ex-teal)!important;color:#fff!important;border-color:var(--ex-teal)!important}#phys-dock .phys-ic-lbl{background:#173f44!important;color:#fff!important;border-radius:9px!important}

/* Footer تعليمي واضح */
.st-key-exercise_platform_footer{margin-top:32px!important;background:linear-gradient(135deg,#173f44,#245e65 58%,#4b887c 125%)!important;border-radius:22px!important;padding:22px 24px 17px!important;color:#fff!important;box-shadow:0 17px 40px rgba(23,63,68,.14)!important}.st-key-exercise_platform_footer [data-testid="stMarkdownContainer"]{color:#fff!important}.exercise-footer-copy{display:flex;align-items:center;gap:11px}.exercise-footer-mark{width:43px;height:43px;border-radius:13px;display:grid;place-items:center;background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.14);font-size:21px}.exercise-footer-copy b{display:block;font-size:16px}.exercise-footer-copy small{display:block;color:#d4e7e3;font-size:10px;margin-top:2px}.exercise-footer-note{margin:11px 0 0;color:#d6e8e4;font-size:10.5px;line-height:1.8}.exercise-footer-email{direction:ltr;unicode-bidi:isolate;color:#f7d779;font-weight:900}.st-key-exercise_platform_footer .stButton>button{background:rgba(255,255,255,.10)!important;color:#fff!important;border:1px solid rgba(255,255,255,.17)!important}.st-key-exercise_platform_footer .stButton>button:hover{background:rgba(255,255,255,.17)!important;border-color:rgba(255,255,255,.3)!important}

@media(max-width:780px){section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{padding:8px 9px 30px!important}.exercise-head-v18{grid-template-columns:1fr;padding:16px 14px;border-radius:21px;gap:9px}.exercise-head-brand{margin-bottom:8px}.exercise-head-v18 h1{font-size:25px;margin:5px 0 3px}.exercise-head-v18 p{font-size:10.5px;line-height:1.7}.exercise-head-chips{margin-top:8px}.exercise-head-chips span:nth-child(n+3){display:none}.exercise-head-side{padding:10px;display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center}.exercise-head-side p,.exercise-version{display:none}.exercise-open-badge{padding:8px;font-size:9px}.exercise-head-brand b{font-size:18px}.st-key-exercise_header_actions [data-testid="stHorizontalBlock"],.st-key-exercise_controls [data-testid="stHorizontalBlock"]{display:block!important}.st-key-exercise_header_actions [data-testid="stColumn"],.st-key-exercise_controls [data-testid="stColumn"]{width:100%!important;margin-bottom:7px!important}.exercise-breadcrumb{justify-content:center}.st-key-profile_pop{left:11px!important;top:11px!important}div[data-testid="stHorizontalBlock"]:has([class*="st-key-question_card_"]){display:flex!important;flex-direction:column!important}div[data-testid="stHorizontalBlock"]:has([class*="st-key-question_card_"])>div[data-testid="stColumn"]:last-child{width:100%!important;min-width:0!important;flex:1 1 auto!important}.exercise-question-title{font-size:23px}.exercise-question-text{font-size:16px;line-height:2}.st-key-exercise_platform_footer{padding:19px 15px!important;border-radius:19px!important}.st-key-exercise_platform_footer [data-testid="stHorizontalBlock"]{display:grid!important;grid-template-columns:1fr!important}.st-key-exercise_platform_footer [data-testid="stColumn"]{width:100%!important}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;animation:none!important;transition:none!important}}
</style>
"""


def _safe_key(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value)


def apply_exercise_ui_v18() -> None:
    st.markdown(_EXERCISE_CSS, unsafe_allow_html=True)


def render_exercise_header_v18(*, subject: str, track: str, unit_title: str, current_page: str, tip: str, subject_icon: str) -> None:
    """يعرض رأسًا مضغوطًا واحترافيًا مع تنقل حقيقي."""
    apply_exercise_ui_v18()  # يُعاد هنا كي يتغلب على أي CSS قديم يسبق الرأس.
    st.markdown(
        '<section class="exercise-head-v18">'
        '<div class="exercise-head-main">'
        '<div class="exercise-head-brand"><span class="exercise-head-mark">🛡️</span>'
        '<span><b>الطالب الصامد</b><small>منصة تعلم العلوم أونلاين وأوفلاين</small></span></div>'
        f'<span class="exercise-head-kicker">{subject_icon} {subject} · الصف الثاني عشر · {track}</span>'
        f'<h1>{unit_title}</h1>'
        '<p>افهم نص المسألة، ثم أكمل العلاقات والتعويضات بنفسك. لا نكشف النتيجة قبل أن تشارك في خطوات الحل.</p>'
        '<div class="exercise-head-chips"><span>خطوات كاملة</span><span>حفظ تلقائي</span><span>رموز ومعادلات واضحة</span><span>يعمل دون اتصال بعد التحميل</span></div>'
        '</div><aside class="exercise-head-side"><strong>ابدأ من التمرين الذي يناسبك</strong>'
        '<p>اختر أي سؤال مباشرة. ترتيب التمارين مقترح للتنظيم وليس شرطًا للدخول.</p>'
        '<div class="exercise-open-badge">✓ جميع التمارين متاحة</div><span class="exercise-version">UI v18</span></aside>'
        '</section>',
        unsafe_allow_html=True,
    )
    with st.container(key="exercise_header_actions"):
        copy_col, dashboard_col, contact_col = st.columns([3.2, 1, 1])
        with copy_col:
            st.markdown(f'<div class="exercise-breadcrumb"><span>الرئيسية</span><span>←</span><span>{subject}</span><span>←</span><b>{track}</b></div>', unsafe_allow_html=True)
        with dashboard_col:
            if st.button("لوحة الطالب", key=f"exercise_head_dashboard_{_safe_key(current_page)}", use_container_width=True):
                st.session_state["samed_view"] = "dashboard"
                st.switch_page("app.py")
        with contact_col:
            if st.button("✉️ تواصل معنا", key=f"exercise_head_contact_{_safe_key(current_page)}", use_container_width=True):
                st.session_state["_contact_return_page"] = current_page
                st.session_state["_contact_return_view"] = st.session_state.get("samed_view", "dashboard")
                st.switch_page("pages/contact.py")
    st.markdown(f'<div class="tip-box-v18"><span>💡</span><span>{tip}</span></div>', unsafe_allow_html=True)


def render_question_card_v18(*, key: str, title: str, statement_html: str, figure_markup: str, progress_pct: int, step_number: int, total_steps: int, elapsed_label: str, kind: str = "interactive") -> None:
    """يبني بطاقة السؤال دون HTML متداخل لمنع ظهور الوسوم كنص."""
    is_proof = kind == "proof"
    chip = "📜 مسألة إثبات نظري" if is_proof else "🧮 تمرين رقمي تفاعلي"
    chip_class = "exercise-question-chip proof" if is_proof else "exercise-question-chip"
    with st.container(key=f"question_card_{_safe_key(key)}", border=True):
        st.markdown(f'<span class="{chip_class}">{chip}</span>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="exercise-question-title">{title}</h2>', unsafe_allow_html=True)
        st.markdown(f'<div class="exercise-question-text">{statement_html}</div>', unsafe_allow_html=True)
        if figure_markup:
            st.markdown(figure_markup, unsafe_allow_html=True)
        st.progress(max(0, min(100, int(progress_pct))) / 100.0)
        st.markdown(f'<div class="exercise-question-meta"><span>الخطوة {step_number} من {total_steps}</span><span>·</span><span>⏱️ الوقت: {elapsed_label}</span></div>', unsafe_allow_html=True)


def render_exercise_footer_v18(current_page: str = "app.py") -> None:
    with st.container(key="exercise_platform_footer"):
        copy_col, dashboard_col, contact_col = st.columns([3.2, 1, 1])
        with copy_col:
            st.markdown(
                '<div class="exercise-footer-copy"><span class="exercise-footer-mark">🛡️</span>'
                '<span><b>الطالب الصامد</b><small>تعليم واضح يعمل أونلاين وأوفلاين</small></span></div>'
                '<p class="exercise-footer-note">جميع أجزاء المسار متاحة للاختيار مباشرة. للدعم والملاحظات: '
                '<span class="exercise-footer-email">techn47@gmail.com</span></p>',
                unsafe_allow_html=True,
            )
        with dashboard_col:
            if st.button("لوحة الطالب", key=f"exercise_footer_dashboard_{_safe_key(current_page)}", use_container_width=True):
                st.session_state["samed_view"] = "dashboard"
                st.switch_page("app.py")
        with contact_col:
            if st.button("✉️ تواصل معنا", key=f"exercise_footer_contact_{_safe_key(current_page)}", use_container_width=True):
                st.session_state["_contact_return_page"] = current_page
                st.session_state["_contact_return_view"] = st.session_state.get("samed_view", "dashboard")
                st.switch_page("pages/contact.py")
