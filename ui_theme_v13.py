"""Shared final visual system for Streamlit pages — UI v13."""
from __future__ import annotations

import streamlit as st

UI_THEME_VERSION = "final-ui-v13-figma-rtl"

_UI_CSS = r"""
<style id="final-ui-v13">
:root{--ui-bg:#f8fafc;--ui-paper:#fff;--ui-ink:#173b3d;--ui-muted:#71847f;--ui-line:#dfe7e5;--ui-deep:#1d5156;--ui-teal:#347d78;--ui-green:#57967b;--ui-gold:#f5c65a;--ui-blue:#236b78;--ui-shadow:0 16px 42px rgba(23,63,68,.09);--ui-shadow-sm:0 7px 22px rgba(23,63,68,.06)}
html,body,.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f8fafc!important;color:var(--ui-ink)!important}
[data-testid="stHeader"],footer{display:none!important}.block-container{max-width:1220px!important;padding-top:16px!important;padding-bottom:55px!important}
[data-testid="stMarkdownContainer"]{color:var(--ui-ink)}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button,[data-testid="stLinkButton"] a{border-radius:12px!important;min-height:43px!important;font-weight:900!important;border:1px solid #cfded9!important;box-shadow:none!important;transition:.18s!important}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:var(--ui-deep)!important;color:#fff!important;border-color:var(--ui-deep)!important}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-1px)!important;border-color:#8bb6ac!important;box-shadow:0 8px 20px rgba(23,63,68,.08)!important}
div[data-testid="stPopover"]>button{border-radius:12px!important;background:#fff!important;color:var(--ui-ink)!important;border:1px solid var(--ui-line)!important;font-weight:900!important;min-height:43px!important}
[data-testid="stExpander"]{background:#fff!important;border:1px solid var(--ui-line)!important;border-radius:17px!important;box-shadow:0 6px 20px rgba(23,63,68,.045)!important;overflow:hidden!important;margin-bottom:8px!important}
[data-testid="stExpander"] summary{padding:7px 6px!important;font-size:15px!important;font-weight:900!important;color:var(--ui-ink)!important}
[data-testid="stExpander"] details[open]{border-color:#bfd4ce!important}
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div{border-radius:12px!important;border-color:#cbdad7!important;background:#fff!important}
.stTextInput input:focus,.stNumberInput input:focus{border-color:var(--ui-teal)!important;box-shadow:0 0 0 4px rgba(52,125,120,.11)!important}

/* shared learning-page surfaces */
.rv-hero{background:linear-gradient(125deg,#245e65 0%,#3e8179 58%,#6a9679 115%)!important;border-radius:28px!important;box-shadow:0 20px 46px rgba(28,88,87,.18)!important}
.rv-ring:after{background:#37736f!important}.rv-route-item,.rv-route>div{border-radius:15px!important;border-color:var(--ui-line)!important}.rv-route-item.active,.rv-route .active{background:#eef8f4!important;border-color:#9fc5bb!important;color:#1d5c58!important}.rv-route-item.active b,.rv-route .active b{background:var(--ui-teal)!important}
.rv-card,.rv-lesson-head,.rv-viz,.rv-visual{border-color:var(--ui-line)!important;border-radius:20px!important;box-shadow:var(--ui-shadow-sm)!important}.rv-card,.rv-lesson-head{background:#fff!important}.rv-lesson-head{border-right:5px solid var(--ui-teal)!important}
.rv-story{border-radius:17px!important}.rv-formula{background:linear-gradient(135deg,#1d5156,#286a6d)!important;border-radius:19px!important;box-shadow:0 12px 28px rgba(29,81,86,.13)!important}.rv-equation{border-radius:13px!important}.rv-map-node,.rv-map button{border-radius:14px!important;border-color:var(--ui-line)!important}.rv-map-node.current,.rv-map button.current{border-color:var(--ui-teal)!important;box-shadow:0 0 0 3px rgba(52,125,120,.10)!important}
.rv-action{background:var(--ui-deep)!important;border-radius:12px!important}.rv-inline-input{border-bottom-color:var(--ui-teal)!important}.rv-simple-sentence{background:#eef8f4!important;border-color:#b9dacf!important;color:#244e4b!important}.rv-vector-note{border-color:var(--ui-teal)!important;color:#1d5156!important}

/* exercise pages */
.main-header{background:linear-gradient(125deg,#245e65,#3e8179 62%,#6a9679)!important;border-radius:24px!important;box-shadow:var(--ui-shadow)!important;padding:22px!important}.q-card,.sidebar-card,.profile-card,.step-card,.law-guide-box,.explain-box,.hint-box,.note-box{border-radius:16px!important}.q-card,.sidebar-card,.profile-card{background:#fff!important;border:1px solid var(--ui-line)!important;box-shadow:var(--ui-shadow-sm)!important}.q-card{border-right:5px solid var(--ui-teal)!important}.step-card-active{border-top-color:var(--ui-teal)!important;box-shadow:0 9px 26px rgba(52,125,120,.12)!important}.step-card-active .step-badge{background:var(--ui-teal)!important}.points-chip{background:#e8f6f1!important;color:#2b705d!important}.xp-bar-fill,.qprogress-fill{background:linear-gradient(90deg,var(--ui-teal),var(--ui-green))!important}

@media(max-width:780px){.block-container{padding:9px 10px 42px!important}.rv-hero{border-radius:22px!important}.main-header{border-radius:18px!important;padding:18px!important}[data-testid="stExpander"] summary{font-size:14px!important}}
</style>
"""


def apply_ui_theme(kind: str = "content") -> None:
    """Inject the final RTL visual system after page-specific CSS."""
    st.markdown(_UI_CSS, unsafe_allow_html=True)
    st.markdown(f"<style>body::after{{content:'{kind}';display:none}}</style>", unsafe_allow_html=True)
