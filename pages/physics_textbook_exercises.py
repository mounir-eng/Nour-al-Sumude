import streamlit as st
import streamlit.components.v1 as components
from ui_theme_v13 import apply_ui_theme
from exercise_ui_v18 import (apply_exercise_ui_v18, render_exercise_header_v18, render_question_card_v18, render_exercise_footer_v18)
import random
import time
from datetime import datetime

# ==========================================================
# 0. هوية المنصة  —  غيّر هذه السطور وحدها لتغيير الاسم في كل المنصة
# ==========================================================
APP_NAME     = "الطالب الصامد"
APP_ICON     = "🛡️"
APP_TAGLINE  = "لا تتوقّف عند أول خطأ"
APP_SUBTITLE = "الدعم التعليمي في الفيزياء والكيمياء · الصفوف 6 — 12"
APP_UNIT     = "الفيزياء · الصف الثاني عشر · حلول تمارين الكتاب — الزخم الخطي والدفع"
PHYSICS_TEXTBOOK_PAGE_VERSION = "physics-book-momentum-v1"

# ==========================================================
# 1. إعدادات الصفحة
# ==========================================================
st.set_page_config(
    page_title=APP_NAME + " — الفيزياء والكيمياء",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# طبقة v18 تُحمّل مبكرًا كي لا تبقى الصفحة على التصميم القديم.
apply_exercise_ui_v18()

# ==========================================================
# 2. التنسيق (CSS)
# ==========================================================
st.markdown("""
<style>

    html, body, [class*="css"], div, span, label, button {
        font-family: 'Cairo', 'Noto Sans Arabic', 'Segoe UI', Tahoma, sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #f8fafc; }

    .main-header {
        background: linear-gradient(135deg, #0f172a, #2563eb);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    .tip-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-weight: 600;
        text-align: center;
    }
    .q-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-right: 6px solid #2563eb;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .q-card-proof { border-right-color: #9333ea; }
    .law-guide-box {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 1.05rem;
        color: #166534;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .explain-box {
        background-color: #eff6ff;
        border: 1px dashed #93c5fd;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 0.98rem;
        color: #1e40af;
        margin-bottom: 15px;
    }
    .hint-box {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        padding: 12px 15px;
        border-radius: 8px;
        font-size: 1rem;
        color: #991b1b;
        margin: 10px 0;
    }
    .note-box {
        background-color: #f5f3ff;
        border: 1px solid #ddd6fe;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #5b21b6;
        margin-top: 10px;
    }
    .points-chip {
        display: inline-block;
        background: #dbeafe;
        color: #1e3a8a;
        padding: 3px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .type-chip-interactive {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 2px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.78rem;
    }
    .type-chip-proof {
        display: inline-block;
        background: #f3e8ff;
        color: #6b21a8;
        padding: 2px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.78rem;
    }
    .badge-chip {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.82rem;
        margin: 3px;
        border: 1px solid #fde68a;
    }
    .sidebar-card {
        background: white;
        border-radius: 10px;
        padding: 14px;
        border: 1px solid #e2e8f0;
        margin-bottom: 14px;
    }
    .xp-bar-bg {
        background: #e2e8f0;
        border-radius: 999px;
        height: 12px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
    }
    .xp-bar-fill {
        background: linear-gradient(90deg,#2563eb,#7c3aed);
        height: 100%;
        border-radius: 999px;
    }
    .qprogress-bg {
        background: #e2e8f0;
        border-radius: 999px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin: 8px 0 16px 0;
    }
    .qprogress-fill {
        background: linear-gradient(90deg,#16a34a,#22c55e);
        height: 100%;
        border-radius: 999px;
    }
    .cert-box {
        background: linear-gradient(135deg,#fef9c3,#fde68a);
        border: 2px dashed #ca8a04;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 15px;
    }

    /* --- بطاقة الملف الشخصي المنبثقة (Popover) --- */
    div[data-testid="stPopover"] button {
        border-radius: 999px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg,#2563eb,#7c3aed) !important;
        color: white !important;
        border: none !important;
        padding: 8px 18px !important;
    }

    /* --- ورقة القوانين في الشريط الجانبي --- */
    .formula-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 10px;
        margin-bottom: 8px;
    }
    .formula-row .f-name {
        font-weight: 800;
        color: #0f172a;
        font-size: 0.92rem;
    }
    .formula-row .f-eq {
        direction: ltr;
        font-weight: 700;
        color: #1d4ed8;
        font-size: 0.95rem;
        background: #eff6ff;
        padding: 2px 8px;
        border-radius: 6px;
        white-space: nowrap;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    .formula-text {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1e3a8a;
        text-align: center;
        direction: ltr !important;
        white-space: nowrap;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1;
    }

    /* --- إصلاح خانات إدخال الأرقام: العرض، المحاذاة، حذف أزرار +/- --- */
    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    div[data-testid="stNumberInputContainer"] {
        height: 42px !important;
        box-sizing: border-box !important;
    }
    .stNumberInput input {
        text-align: center !important;
        direction: ltr !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        padding: 0 4px !important;
        box-sizing: border-box !important;
        height: 40px !important;
        line-height: 40px !important;
    }

    /* صفوف المعادلة التفاعلية: عرض بحجم المحتوى + محاذاة تامة + إخفاء التسمية المخفية */
    .st-key-formula_blanks_row [data-testid="stElementContainer"],
    .st-key-formula_res_row [data-testid="stElementContainer"],
    .st-key-formula_root_row [data-testid="stElementContainer"] {
        margin: 0 !important;
    }
    .st-key-formula_blanks_row [data-testid="stWidgetLabel"],
    .st-key-formula_res_row [data-testid="stWidgetLabel"],
    .st-key-formula_root_row [data-testid="stWidgetLabel"] {
        display: none !important;
    }
    .st-key-formula_blanks_row div[data-testid="stColumn"],
    .st-key-formula_res_row div[data-testid="stColumn"],
    .st-key-formula_root_row div[data-testid="stColumn"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0 3px !important;
    }
    .st-key-formula_blanks_row div[data-testid="stColumn"]:has(div[data-testid="stNumberInputContainer"]),
    .st-key-formula_res_row div[data-testid="stColumn"]:has(div[data-testid="stNumberInputContainer"]),
    .st-key-formula_root_row div[data-testid="stColumn"]:has(div[data-testid="stNumberInputContainer"]) {
        width: 108px !important;
    }
    .st-key-formula_blanks_row div[data-testid="stHorizontalBlock"],
    .st-key-formula_res_row div[data-testid="stHorizontalBlock"],
    .st-key-formula_root_row div[data-testid="stHorizontalBlock"] {
        direction: ltr !important;
        gap: 0.3rem !important;
        flex-wrap: wrap !important;
        row-gap: 10px !important;
    }

    /* ==================== صف إدخال خطوات الإثبات (رمزي/عددي) ==================== */
    .st-key-formula_proof_row [data-testid="stElementContainer"] { margin: 0 !important; }
    .st-key-formula_proof_row [data-testid="stWidgetLabel"] { display: none !important; }
    .st-key-formula_proof_row div[data-testid="stColumn"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0 4px !important;
    }
    .st-key-formula_proof_row div[data-testid="stColumn"]:has(div[data-testid="stTextInput"]) {
        width: 150px !important;
    }
    .st-key-formula_proof_row div[data-testid="stHorizontalBlock"] {
        direction: ltr !important;
        gap: 0.3rem !important;
        flex-wrap: wrap !important;
        row-gap: 10px !important;
    }
    .stTextInput input {
        text-align: center !important;
        direction: ltr !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        color: #1d4ed8 !important;
        border: 2px solid #93c5fd !important;
        border-radius: 8px !important;
        padding: 6px 8px !important;
        height: 40px !important;
        box-sizing: border-box !important;
    }

    /* ==================== بطاقات الخطوات الأفقية (RTL) ==================== */
    .step-card {
        border-radius: 12px;
        padding: 16px 14px;
        margin-bottom: 15px;
        min-height: 120px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .step-card .formula-text { font-size: 1.05rem; height: 34px; white-space: normal; }
    .step-card .law-guide-box { font-size: 0.88rem; padding: 8px 10px; margin-bottom: 10px; }
    .step-card .hint-box { font-size: 0.88rem; padding: 10px 12px; }
    .step-card .points-chip { font-size: 0.78rem; padding: 2px 10px; }
    .step-card h4 { font-size: 1rem; margin-bottom: 8px; }

    .step-card-completed {
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        border-top: 5px solid #16a34a;
    }
    .step-card-completed .step-badge {
        display: inline-block; background: #16a34a; color: white;
        font-size: 0.75rem; font-weight: 800; padding: 3px 10px;
        border-radius: 999px; margin-bottom: 8px;
    }
    .step-card-active {
        background-color: #ffffff;
        border: 1px solid #bfdbfe;
        border-top: 5px solid #2563eb;
        box-shadow: 0 4px 14px rgba(37,99,235,0.12);
    }
    .step-card-active .step-badge {
        display: inline-block; background: #2563eb; color: white;
        font-size: 0.75rem; font-weight: 800; padding: 3px 10px;
        border-radius: 999px; margin-bottom: 8px;
    }
    .step-card-locked {
        background-color: #f1f5f9;
        border: 1px dashed #cbd5e1;
        color: #94a3b8;
        border-top: 5px solid #cbd5e1;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .step-card-locked .lock-icon { font-size: 2rem; margin-bottom: 6px; opacity: 0.6; }

    /* ==================== شبكة الأوسمة في الشريط الجانبي ==================== */
    .badges-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: 8px;
    }
    .badge-tile {
        background: #fef3c7;
        border: 1px solid #fde68a;
        border-radius: 10px;
        padding: 10px 4px;
        text-align: center;
        font-size: 0.68rem;
        font-weight: 700;
        color: #92400e;
        line-height: 1.3;
    }
    .badge-tile .b-icon { font-size: 1.3rem; display: block; margin-bottom: 3px; }
    .badge-empty {
        text-align: center;
        color: #94a3b8;
        font-size: 0.82rem;
        padding: 10px 0;
    }
    .profile-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 14px;
        text-align: center;
    }
    .profile-avatar {
        width: 56px; height: 56px; border-radius: 50%;
        background: linear-gradient(135deg,#2563eb,#7c3aed);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem; color: white; margin: 0 auto 8px auto;
    }
    .level-badge-pill {
        display: inline-block;
        font-weight: 800;
        font-size: 0.85rem;
        padding: 3px 14px;
        border-radius: 999px;
        margin-top: 4px;
    }
    .proof-line {
        background: #faf5ff;
        border-right: 4px solid #9333ea;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
        direction: ltr;
        text-align: left;
        font-weight: 700;
        color: #581c87;
        font-size: 1.05rem;
    }

    /* ============ معادلات LaTeX في مسائل الإثبات: من اليسار إلى اليمين ============ */
    [data-testid="stLatex"],
    .stLatex,
    .katex,
    .katex-display,
    .katex-html {
        direction: ltr !important;
        unicode-bidi: isolate !important;
        text-align: center !important;
    }
    .katex-display {
        margin: 10px 0 !important;
        overflow-x: auto;
        overflow-y: hidden;
    }
    .katex { font-size: 1.45rem !important; }
    /* الرقم السفلي في أسفل يمين الرمز (m₁ ، p₂) */
    .katex .msupsub { text-align: left !important; }

    /* نصوص مختلطة (عربي + معادلات): كل مقطع باتجاهه الطبيعي */
    .law-guide-box, .explain-box, .hint-box, .proof-line,
    .q-card p, .q-card small, .q-card h2 {
        unicode-bidi: plaintext;
    }

    /* وضوح الرموز السفلية: الرقم أسفل يمين الحرف */
    .q-card sub, .law-guide-box sub, .explain-box sub, .hint-box sub,
    .proof-line sub, h4 sub, [data-testid="stAlert"] sub {
        font-size: 0.72em;
        font-weight: 800;
        line-height: 0;
        vertical-align: baseline;
        position: relative;
        bottom: -0.28em;
        padding-inline-start: 0.02em;
    }

    /* ============ عرض المعادلات بدون LaTeX: HTML من اليسار إلى اليمين ============ */
    .eq-box {
        direction: ltr;
        unicode-bidi: isolate;
        text-align: center;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 8px;
        margin: 6px 0 12px 0;
        overflow-x: auto;
        overflow-y: hidden;
    }
    .eq {
        display: inline-block;
        direction: ltr;
        unicode-bidi: isolate;
        white-space: nowrap;
        vertical-align: middle;
        font-family: "Cambria Math", "Times New Roman", Georgia, serif;
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.3;
    }
    .eq sub {
        font-size: 0.60em;
        font-weight: 800;
        vertical-align: baseline;
        position: relative;
        bottom: -0.32em;
        margin-left: 0.02em;
    }
    .eq sup {
        font-size: 0.60em;
        font-weight: 800;
        vertical-align: baseline;
        position: relative;
        top: -0.62em;
        margin-left: 0.02em;
    }
    .eq-fr {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        vertical-align: middle;
        margin: 0 5px;
        font-size: 0.90em;
    }
    .eq-num {
        display: block;
        padding: 0 7px 3px 7px;
        border-bottom: 2.5px solid #0f172a;
        white-space: nowrap;
    }
    .eq-den {
        display: block;
        padding: 3px 7px 0 7px;
        white-space: nowrap;
    }
    .eq-op { padding: 0 3px; color: #334155; }
    .eq-eq { padding: 0 9px; color: #2563eb; font-weight: 900; }
    .eq-txt {
        font-family: "Segoe UI", Tahoma, sans-serif;
        font-size: 0.72em;
        font-weight: 700;
        color: #475569;
    }
    .eq-rt { border-top: 2.5px solid #0f172a; padding: 0 3px; }
    .eq-unk {
        color: #b91c1c;
        background: #fee2e2;
        border: 1.5px dashed #f87171;
        border-radius: 6px;
        padding: 0 7px;
        font-weight: 900;
    }

    /* ============ صندوق القانون: العنوان في سطر والعلاقة في سطر واحد ============ */
    .derive-box {
      background: #eef4ff;
      border: 1px solid #c7d7fb;
      border-right: 5px solid #3b82f6;
      border-radius: 10px;
      padding: 9px 11px;
      margin: 4px 0 10px 0;
      direction: rtl;
    }
    .derive-title {
      font-weight: 800;
      color: #1e3a8a;
      font-size: 0.9rem;
      margin-bottom: 6px;
    }
    .derive-line {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      margin: 3px 0;
      padding-bottom: 4px;
      border-bottom: 1px dashed #dbe6fb;
    }
    .derive-line:last-child { border-bottom: none; padding-bottom: 0; }
    .derive-say {
      color: #1f2937;
      font-size: 0.85rem;
      font-weight: 600;
      line-height: 1.7;
    }
    .derive-num {
      display: inline-block;
      min-width: 19px;
      height: 19px;
      line-height: 19px;
      text-align: center;
      border-radius: 50%;
      background: #3b82f6;
      color: #ffffff;
      font-size: 0.7rem;
      font-weight: 800;
      margin-left: 6px;
    }
    .derive-eq { direction: ltr; unicode-bidi: isolate; }
    .derive-eq .eq { font-size: 1.06rem; }
    .derive-final {
      background: #fff7ed;
      border: 1px solid #fdba74;
      border-radius: 8px;
      padding: 5px 7px;
      margin-top: 5px;
    }
    .derive-final .derive-num { background: #f59e0b; }
    /* --- سلسلة الاستنتاج التفاعلية: نفس سلوك الصندوق الأصفر بألوان زرقاء --- */
    .derive-box .micro-box { background: transparent; border: none; padding: 0; margin: 0; }
    .derive-box .micro-line {
      display: block;
      margin: 5px 0 7px 0;
      padding-bottom: 6px;
      border-bottom: 1px dashed #dbe6fb;
    }
    .derive-box .micro-line:last-child { border-bottom: none; padding-bottom: 0; }
    .derive-box .micro-say { color: #1e3a8a; font-size: 0.85rem; font-weight: 700; }
    .derive-box .micro-num { background: #3b82f6; }
    .derive-box .micro-eq { border: 1px solid #c7d7fb; background: #ffffff; }
    .derive-box .derive-ref .micro-eq {
      background: #f8fafc;
      border-style: dashed;
      border-color: #94a3b8;
    }
    .derive-box .derive-ref .micro-num { background: #64748b; }
    .derive-box .derive-final {
      background: #fff7ed;
      border: 1px solid #fdba74;
      border-radius: 8px;
      padding: 6px 8px;
      margin-top: 7px;
    }
    .derive-box .derive-final .micro-num { background: #f59e0b; }
    .derive-box .derive-final .micro-say { color: #92400e; }
    .derive-box .derive-final .micro-eq { border-color: #fdba74; }
    .derive-tip {
      margin-top: 7px;
      font-size: 0.76rem;
      font-weight: 600;
      color: #475569;
    }
    .fig-box { margin: 10px 0 2px; text-align: center; }
    .fig-box img { width: 420px; max-width: 100%; height: auto; background: #fff;
        border: 1px solid #e2e8f0; border-radius: 10px; padding: 6px; }
    .fig-cap { font-size: 0.78rem; color: #64748b; margin-top: 2px; }
    .law-line { margin: 3px 0; }
    .law-label {
        display: block;
        direction: rtl;
        text-align: right;
        font-weight: 700;
        color: #166534;
    }
    .law-note {
        display: block;
        direction: rtl;
        text-align: right;
        font-weight: 600;
        color: #166534;
    }
    .law-eq {
        display: block;
        direction: ltr;
        unicode-bidi: isolate;
        text-align: left;
        white-space: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        font-family: "Cambria Math", "Times New Roman", Georgia, serif;
        font-size: 1.05rem;
        font-weight: 800;
        color: #14532d;
        background: #ffffff;
        border: 1px solid #bbf7d0;
        border-radius: 6px;
        padding: 4px 9px;
        margin: 3px 0 5px 0;
    }

    /* ============ خانة إدخال الطالب داخل المعادلة مكان علامة الاستفهام ============ */
    .eq-slot {
        display: inline-block;
        vertical-align: middle;
        line-height: 1;
    }
    .eq-slot .eq-unk { cursor: pointer; }
    input.phys-slot-input {
        width: 78px;
        height: 34px;
        box-sizing: border-box;
        text-align: center;
        direction: ltr;
        font-family: "Cambria Math", "Times New Roman", Georgia, serif;
        font-size: 1.05rem;
        font-weight: 900;
        color: #b91c1c;
        background: #fff5f5;
        border: 2px dashed #f87171;
        border-radius: 8px;
        padding: 0 5px;
        margin: 0 3px;
        outline: none;
        vertical-align: middle;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
        transition: background 0.15s, border-color 0.15s;
    }
    input.phys-slot-input::placeholder {
        color: #ef4444;
        opacity: 0.95;
        font-weight: 900;
    }
    input.phys-slot-input:hover { background: #fee2e2; }
    input.phys-slot-input:focus {
        border: 2px solid #2563eb;
        background: #eff6ff;
        color: #1e3a8a;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.16);
    }
    .eq-hint {
        direction: rtl;
        text-align: center;
        font-size: 0.8rem;
        font-weight: 700;
        color: #475569;
        margin: 4px 0 2px 0;
    }

    /* ============ توحيد شكل المعادلات في كل الصناديق (نفس أسلوب معادلة الإدخال) ============ */
    .law-eq .eq, .result-eq .eq, .micro-eq .eq { font-size: 1.12rem; }
    .eq-inline .eq { font-size: 1.0rem; }
    .law-eq .eq-eq, .result-eq .eq-eq, .micro-eq .eq-eq { padding: 0 6px; }
    .law-eq, .result-eq, .micro-eq { line-height: 1.55; }
    .eq-inline {
        display: inline-block;
        direction: ltr;
        unicode-bidi: isolate;
        margin: 0 4px;
        vertical-align: middle;
    }
    .result-note {
        display: block;
        direction: rtl;
        text-align: right;
        font-weight: 700;
        color: #065f46;
    }

    /* ============ صندوق الخطوات المبسّطة ============ */
    .micro-box {
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 7px 10px;
        margin: 8px 0 4px 0;
        direction: rtl;
    }
    .micro-title {
        direction: rtl;
        text-align: right;
        font-weight: 800;
        font-size: 0.92rem;
        color: #92400e;
        margin-bottom: 3px;
    }
    .micro-line { display: block; margin: 6px 0 8px 0; }

    /* ===== صفوف الإدخال الحيّة بنفس شكل الصندوق الأصفر ===== */
    .st-key-formula_blanks_row,
    .st-key-formula_root_row,
    .st-key-formula_res_row {
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 8px 10px 10px 10px;
        margin: 8px 0 4px 0;
        direction: rtl;
    }
    .live-say {
        display: block;
        direction: rtl;
        text-align: right;
        font-size: 0.86rem;
        font-weight: 700;
        color: #78350f;
        margin-bottom: 7px;
    }
    .st-key-formula_blanks_row div[data-baseweb="input"],
    .st-key-formula_root_row div[data-baseweb="input"],
    .st-key-formula_res_row div[data-baseweb="input"] {
        border: 1px dashed #f59e0b !important;
        border-radius: 7px !important;
        background: #ffffff !important;
    }
    .st-key-formula_blanks_row input,
    .st-key-formula_root_row input,
    .st-key-formula_res_row input {
        text-align: center !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        font-family: "Cambria Math", "Times New Roman", Georgia, serif !important;
        font-size: 1rem !important;
    }
    .st-key-formula_res_row [data-testid="stElementContainer"] { margin: 0 !important; }
    .st-key-step_actions_row { margin-top: 12px; }
    .micro-num {
        display: inline-block;
        min-width: 19px;
        height: 19px;
        line-height: 19px;
        text-align: center;
        border-radius: 50%;
        background: #f59e0b;
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 900;
        margin-left: 5px;
    }
    .micro-say {
        display: block;
        direction: rtl;
        text-align: right;
        font-size: 0.86rem;
        font-weight: 700;
        color: #78350f;
    }
    .micro-eq {
        display: block;
        direction: ltr;
        unicode-bidi: isolate;
        text-align: left;
        white-space: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        font-family: "Cambria Math", "Times New Roman", Georgia, serif;
        font-size: 1.02rem;
        font-weight: 800;
        color: #0f172a;
        background: #ffffff;
        border: 1px solid #fde68a;
        border-radius: 6px;
        padding: 3px 9px;
        margin: 3px 0 0 0;
    }

    /* ============ إطار النتيجة: بنفس أسلوب صندوق القانون/المعطى ============ */
    .result-box {
        background-color: #ecfdf5;
        border: 1px solid #6ee7b7;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 10px 0 4px 0;
    }
    .result-label {
        display: block;
        direction: rtl;
        text-align: right;
        font-weight: 800;
        font-size: 0.95rem;
        color: #065f46;
    }
    .result-eq {
        display: block;
        direction: ltr;
        unicode-bidi: isolate;
        text-align: left;
        white-space: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        font-family: "Cambria Math", "Times New Roman", Georgia, serif;
        font-size: 1.08rem;
        font-weight: 800;
        color: #137333;
        background: #ffffff;
        border: 1px solid #86efac;
        border-radius: 6px;
        padding: 5px 9px;
        margin: 4px 0 3px 0;
    }

    /* ============ شريط الخطوات: 3 إطارات في الشاشة + سحب أفقي ============ */
    .phys-strip { scrollbar-width: thin; scrollbar-color: #2563eb #e2e8f0; }
    .phys-strip::-webkit-scrollbar { height: 14px; }
    .phys-strip::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 8px; }
    .phys-strip::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        border-radius: 8px;
        border: 3px solid #e2e8f0;
    }
    .phys-hint-drag {
        text-align: center;
        font-size: 0.82rem;
        font-weight: 700;
        color: #475569;
        background: #eff6ff;
        border: 1px dashed #93c5fd;
        border-radius: 8px;
        padding: 4px 10px;
        margin: 4px 0 8px 0;
    }

    /* تصغير طفيف لنص المعادلة داخل صفوف الإدخال حتى تبقى في سطر واحد */
    .st-key-formula_proof_row .formula-text,
    .st-key-formula_blanks_row .formula-text,
    .st-key-formula_res_row .formula-text,
    .st-key-formula_root_row .formula-text {
        font-size: 1.1rem;
        height: 40px;
    }

    /* ============ تثبيت بطاقة التمرين عند تجاوزها (Freeze مثل Excel) ============ */
    /* نسخة مُجمّدة تطابق مكان البطاقة، ولا تظهر إلا بعد تجاوزها أثناء النزول */
    #phys-frozen-card {
        position: fixed;
        display: none;
        z-index: 1000;
        direction: rtl;
        text-align: right;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        box-shadow: 0 12px 34px rgba(15, 23, 42, 0.20);
        overflow: hidden;
    }
    #phys-frozen-card.phys-dock-side {
        flex-direction: column;
    }
    #phys-frozen-card .phys-panel-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        padding: 8px 12px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #ffffff;
        font-weight: 800;
        font-size: 0.92rem;
        flex: 0 0 auto;
    }
    #phys-frozen-card .phys-panel-close {
        background: rgba(255, 255, 255, 0.20);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        width: 26px;
        height: 26px;
        line-height: 1;
        font-size: 0.85rem;
        font-weight: 900;
        cursor: pointer;
        flex: 0 0 auto;
    }
    #phys-frozen-card .phys-panel-close:hover {
        background: rgba(255, 255, 255, 0.38);
    }
    #phys-frozen-card .phys-panel-body {
        flex: 1 1 auto;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 10px;
    }
    #phys-frozen-card.phys-dock-side .phys-panel-body {
        font-size: 0.94rem;
    }
    #phys-frozen-card.phys-dock-side .q-card {
        margin: 0 !important;
        border: none !important;
        box-shadow: none !important;
        max-height: none !important;
    }
    #phys-frozen-card.phys-dock-top {
        background: transparent;
        border: none;
        border-radius: 0;
        box-shadow: none;
    }
    #phys-frozen-card.phys-dock-top .phys-panel-bar {
        display: none;
    }
    #phys-frozen-card.phys-dock-top .phys-panel-body {
        padding: 0;
    }
    #phys-frozen-card.phys-dock-top .q-card {
        margin: 0 !important;
        max-height: 34vh;
        overflow-y: auto;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18) !important;
    }
    #phys-frozen-tab {
        position: fixed;
        display: none;
        z-index: 1000;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #ffffff;
        font-weight: 800;
        font-size: 0.82rem;
        padding: 12px 7px;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.20);
        -webkit-writing-mode: vertical-rl;
        writing-mode: vertical-rl;
        letter-spacing: 1px;
        user-select: none;
    }
    /* احتياطي: يعمل فقط إن لم يُشتغل السكربت في المتصفح */
    html:not(.phys-js) div[data-testid="stHorizontalBlock"]:has(.q-card) {
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
        background: #f8fafc !important;
    }

/* ===== حالات التعويض داخل الخطوات المبسّطة ===== */
.micro-eq.mi-ok { border-color: #34d399 !important; background: #f0fdf4 !important; }
.micro-eq.mi-bad { border-color: #ef4444 !important; background: #fef2f2 !important; animation: miShake .34s ease; }
.micro-eq.mi-shown { border-color: #f59e0b !important; background: #fffbeb !important; }
.eq-slot.eq-filled { border-style: solid !important; border-color: #34d399 !important; background: #ecfdf5 !important; }
.eq-slot.eq-filled .eq-unk { color: #047857 !important; }
.micro-tag { color: #047857; font-weight: 900; margin-right: 6px; font-size: 0.95rem; }
.micro-line.micro-final .eq-box { margin: 4px 0 2px 0; }
@keyframes miShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
    /* ===== أيقونة الطالب: كل المعلومات داخل نافذة منبثقة ===== */
    .st-key-profile_pop { display: flex; justify-content: center; margin: 2px 0 14px 0; }
    .st-key-profile_pop div[data-testid="stPopover"] button {
        width: 56px !important;
        height: 56px !important;
        min-height: 56px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        font-size: 1.45rem !important;
        font-weight: 900 !important;
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35) !important;
    }
    .st-key-profile_pop div[data-testid="stPopover"] button p {
        font-size: 1.45rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }
    /* ===== نص التمرين الدائم في أقصى اليمين ===== */
    .sb-stmt {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-right: 5px solid #7c3aed;
        border-radius: 12px;
        padding: 12px 14px;
        margin: 0 0 14px 0;
    }
    .sb-stmt .sb-chip {
        display: inline-block;
        background: #ede9fe;
        color: #6d28d9;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 3px 9px;
        border-radius: 999px;
        margin-bottom: 6px;
    }
    .sb-stmt h4 {
        margin: 2px 0 6px 0 !important;
        padding: 0 !important;
        font-size: 0.98rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
    }
    .sb-stmt p {
        font-size: 0.93rem !important;
        line-height: 1.85 !important;
        color: #1e293b !important;
        margin: 0 0 6px 0 !important;
    }
    .sb-stmt small { color: #64748b; font-size: 0.75rem; }
    .sb-title { font-weight: 900; color: #0f172a; font-size: 0.98rem; margin: 6px 0 8px 0; }

    /* ============ لوحة الأيقونتين الجانبية (القوانين / نص التمرين) ============ */
    #phys-src-stmt, #phys-src-laws { display: none !important; }
    .st-key-phys_src { display: none !important; }

    #phys-dock {
        position: fixed;
        z-index: 9998;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 10px;
        direction: ltr;
        pointer-events: none;
    }
    #phys-dock > * { pointer-events: auto; }

    .phys-rail { display: flex; flex-direction: column; align-items: center; gap: 14px; width: 96px; }
    .phys-ic-wrap { display: flex; flex-direction: column; align-items: center; gap: 5px; cursor: pointer; }
    .phys-ic-lbl {
        direction: rtl; font-size: 0.63rem; font-weight: 800; color: #334155;
        background: rgba(255,255,255,0.96); border: 1px solid #e2e8f0; border-radius: 9px;
        padding: 3px 6px; text-align: center; line-height: 1.35; max-width: 94px;
        box-shadow: 0 3px 9px rgba(15,23,42,0.10); transition: all 0.18s ease;
    }
    .phys-ic-wrap:hover .phys-ic-lbl { color: #0f172a; }
    .phys-ic-calc { background: linear-gradient(135deg, #059669, #34d399); }
    .phys-ic-wrap.on .lbl-calc { background: #ecfdf5; border-color: #6ee7b7; color: #065f46; }

    .phys-calc { direction: ltr; }
    .phys-calc-disp {
        background: #0f172a; color: #ffffff; border-radius: 12px;
        padding: 10px 12px; margin-bottom: 10px; text-align: right; min-height: 60px;
    }
    .phys-calc-expr { font-size: 0.82rem; color: #94a3b8; min-height: 17px; word-break: break-all; }
    .phys-calc-val { font-size: 1.5rem; font-weight: 900; word-break: break-all; }
    .phys-calc-pad { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7px; }
    .phys-calc-key {
        border: 1px solid #e2e8f0; background: #f8fafc; color: #0f172a;
        border-radius: 10px; padding: 11px 0; font-size: 1.05rem; font-weight: 800;
        cursor: pointer; transition: background 0.12s ease, transform 0.12s ease;
    }
    .phys-calc-key:hover { background: #e2e8f0; transform: translateY(-1px); }
    .phys-calc-key.k-fn { background: #fee2e2; border-color: #fecaca; color: #991b1b; }
    .phys-calc-key.k-eq {
        grid-column: span 3; border: none; color: #ffffff;
        background: linear-gradient(135deg, #2563eb, #60a5fa);
    }
    .phys-ic-wrap.on .lbl-laws { background: #fffbeb; border-color: #fcd34d; color: #92400e; }
    .phys-ic-wrap.on .lbl-stmt { background: #eff6ff; border-color: #93c5fd; color: #1e40af; }

    .phys-ic {
        width: 54px; height: 54px; min-height: 54px;
        border-radius: 50%; border: 3px solid #ffffff;
        cursor: pointer; padding: 0; margin: 0;
        font-size: 1.45rem; line-height: 1; color: #ffffff;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 7px 18px rgba(15, 23, 42, 0.30);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .phys-ic:hover { transform: scale(1.08); }
    .phys-ic-laws { background: linear-gradient(135deg, #f59e0b, #fcd34d); }
    .phys-ic-stmt { background: linear-gradient(135deg, #2563eb, #60a5fa); }
    .phys-ic.on {
        box-shadow: 0 0 0 4px rgba(15, 23, 42, 0.16), 0 9px 22px rgba(15, 23, 42, 0.34);
        transform: scale(1.06);
    }

    .phys-pane {
        display: none;
        direction: rtl; text-align: right;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        box-shadow: 0 18px 44px rgba(15, 23, 42, 0.22);
        padding: 14px 15px 16px 15px;
        overflow-y: auto; overflow-x: hidden;
        transform: translateY(0); opacity: 1;
        transition: transform 0.2s ease, opacity 0.2s ease;
    }
    .phys-pane.pane-out   { transform: translateY(34px); opacity: 0; }
    .phys-pane.pane-start { transform: translateY(-14px); opacity: 0; }

    .phys-pane-head {
        font-weight: 900; font-size: 1rem; color: #0f172a;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 9px; margin-bottom: 11px;
    }
    #phys-dock .sb-stmt {
        border: none; border-right: none; box-shadow: none;
        padding: 0; margin: 0; background: transparent;
    }
    #phys-dock .sb-stmt p { font-size: 1rem; line-height: 1.95; }
    #phys-dock .formula-row { margin: 0 0 10px 0; }
    #phys-dock .f-eq { font-size: 1.02rem; }

    /* إظهار المعادلات المنسّقة داخل صفوف التعويض */
    .formula-text .eq { font-size: inherit; line-height: 1; }
    .eq-par { color: #64748b; font-weight: 700; padding: 0 1px; }
    .eq-sl { color: #475569; padding: 0 3px; font-weight: 700; }
    .eq-rad { color: #0f172a; font-weight: 800; }
    .formula-text .eq sub, .formula-text .eq sup { line-height: 0; }

    
    /* ===== إلغاء المساحة الرمادية الجانبية: كل العرض لصفحة الموقع ===== */
    section[data-testid="stSidebar"] { display: none !important; }
    div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
    div[data-testid="collapsedControl"] { display: none !important; }
    button[data-testid="stSidebarCollapseButton"] { display: none !important; }
    section[data-testid="stMain"] { width: 100% !important; max-width: 100% !important; }
    .st-key-avatar_row { margin-bottom: -14px !important; }
    .st-key-avatar_row div[data-testid="stColumn"] { min-width: 0 !important; }

    
    /* ===== إخفاء شريط Streamlit الرمادي العلوي + عرض الموقع على كامل الشاشة ===== */
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    div[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
    section[data-testid="stMain"] .block-container,
    div[data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding-top: 0.6rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1.4rem !important;
        padding-right: 1.4rem !important;
    }

    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. بنك الأسئلة (تمارين تفاعلية + مسائل إثبات نظرية)
# ==========================================================
questions_db = [{'id': 'pb3',
  'title': 'تمرين الكتاب (3) · علّل',
  'type': 'proof',
  'focus': 'تفسير تطبيقات الدفع وحفظ الزخم',
  'text': 'علّل: 1) قد تنكسر البيضة على الإسمنت ولا تنكسر على الرمل من الارتفاع نفسه. 2) تكون مواسير بنادق '
          'الصيد طويلة. 3) سرعة ارتداد المدفع أقل كثيرًا من سرعة انطلاق القذيفة.',
  'conclusion': 'القاعدة المبسطة: زمن أطول ← قوة أقل، ودفع أكبر ← سرعة أكبر، وكتلة أكبر ← سرعة ارتداد أصغر.',
  'steps': [{'num': 1,
             'title': '1) البيضة: لماذا ينجيها الرمل؟',
             'law': 'F = ΔP ÷ Δt',
             'micro': [['السقوط من الارتفاع نفسه، إذن التغير في الزخم متساوٍ:', 'ΔP واحد في الحالتين'],
                       ['القوة = التغير في الزخم ÷ زمن التوقف:', 'F = ΔP ÷ Δt'],
                       ['الرمل يطيل زمن التوقف، فالقوة:', 'F = ?', 'تقل']],
             'type': 'symbol',
             'latex_preview': 'F = ΔP ÷ Δt',
             'prefix': 'الإجابة = ',
             'label': 'اكتب الإجابة في سطر واحد:',
             'suffix': '',
             'target': 'زمن التوقف أطول على الرمل فتقل القوة',
             'completed_display': 'ببساطة: التغير في الزخم واحد في الحالتين، والرمل يطيل زمن التوقف؛ ولأن '
                                  'القوة = ΔP ÷ Δt تكون القوة أصغر فلا تنكسر البيضة.',
             'hint': 'زمن أطول ← قوة أقل.'},
            {'num': 2,
             'title': '2) الماسورة الطويلة: لماذا تزيد السرعة؟',
             'law': 'I = F × Δt',
             'micro': [['الدفع = القوة × زمن تأثيرها:', 'I = F × Δt'],
                       ['الماسورة الطويلة تبقي القوة مؤثرة زمنًا أطول:', 'Δt يزداد'],
                       ['فيزداد الدفع، والدفع هو التغير في الزخم، إذن السرعة:', 'v = ?', 'تزداد']],
             'type': 'symbol',
             'latex_preview': 'I = F × Δt = ΔP',
             'prefix': 'الإجابة = ',
             'label': 'اكتب الإجابة في سطر واحد:',
             'suffix': '',
             'target': 'زمن تأثير أطول يعطي دفعًا أكبر فسرعة أكبر',
             'completed_display': 'ببساطة: طول الماسورة يزيد زمن دفع القوة للقذيفة، فيزداد الدفع ويزداد '
                                  'الزخم؛ فتخرج بسرعة أكبر.',
             'hint': 'زمن أطول ← دفع أكبر ← سرعة أكبر.'},
            {'num': 3,
             'title': '3) المدفع: لماذا سرعة ارتداده صغيرة؟',
             'law': 'زخم المدفع = زخم القذيفة (مقدارًا)',
             'micro': [['قبل الإطلاق النظام ساكن:', 'الزخم الكلي = 0'],
                       ['بعد الإطلاق يتساوى الزخمان في المقدار:', 'm_مدفع × v_مدفع = m_قذيفة × v_قذيفة'],
                       ['كتلة المدفع أكبر بكثير، فسرعته:', 'v_مدفع = ?', 'صغيرة']],
             'type': 'symbol',
             'latex_preview': 'm_g v_g = m_b v_b',
             'prefix': 'الإجابة = ',
             'label': 'اكتب الإجابة في سطر واحد:',
             'suffix': '',
             'target': 'كتلة المدفع أكبر فسرعة ارتداده أصغر',
             'completed_display': 'ببساطة: زخم المدفع يساوي زخم القذيفة في المقدار ويعاكسه في الاتجاه؛ ولأن '
                                  'كتلة المدفع أكبر بكثير تكون سرعة ارتداده أصغر بكثير.',
             'hint': 'الحاصل واحد: كتلة أكبر ← سرعة أصغر.'}]},
 {'id': 'pb4',
  'title': 'تمرين الكتاب (4) · الدفع والزمن',
  'type': 'interactive',
  'focus': 'I = FΔt',
  'text': 'أثرت قوة مقدارها 15 N في جسم مدة 7 s. احسب: أ) الدفع. ب) الزمن اللازم لقوة 1.5 N كي تعطي الدفع نفسه.',
  'conclusion': 'الدفع 105 N·s، والزمن المطلوب للقوة الثانية 70 s.',
  'steps': [{'num': 1,
             'title': 'حساب دفع القوة الأولى',
             'law': 'I = F Δt',
             'micro': [['اكتب القانون:', 'I = F Δt'], ['عوّض:', 'I = 15×7'], ['احسب:', 'I = 105 N·s']],
             'simple_explain': 'لا تنتقل إلى القوة الثانية قبل تثبيت قيمة الدفع الأول.',
             'prefix': 'I = (',
             'blanks': [{'label': 'F', 'target': 15.0, 'suffix': ') × ('},
                        {'label': 'dt', 'target': 7.0, 'suffix': ') N·s'}],
             'has_root': False,
             'result_target': 105.0,
             'result_tol': 0.01,
             'result_label': 'احسب الدفع I:',
             'hint': 'اضرب 15 في 7.'},
            {'num': 2,
             'title': 'عزل الزمن للقوة الثانية',
             'law': 'Δt = I/F',
             'micro': [['نفس الدفع:', 'I₂ = I₁ = 105'],
                       ['من I = FΔt:', 'Δt = I/F'],
                       ['بالتعويض:', 'Δt = 105/1.5 = 70 s']],
             'simple_explain': 'نستخدم الدفع المستنتج في الخطوة السابقة ثم نعزل الزمن.',
             'prefix': 'Δt = (',
             'blanks': [{'label': 'I', 'target': 105.0, 'suffix': ') / ('},
                        {'label': 'F', 'target': 1.5, 'suffix': ') s'}],
             'has_root': False,
             'result_target': 70.0,
             'result_tol': 0.01,
             'result_label': 'احسب الزمن Δt:',
             'hint': 'استخدم قيمة الدفع 105 ولا تعاود حسابها.'}]},
 {'id': 'pb5',
  'title': 'تمرين الكتاب (5) · كرة ساكنة',
  'type': 'interactive',
  'focus': 'التغير في الزخم ومتوسط القوة',
  'text': 'ضرب لاعب كرة ساكنة كتلتها 0.6 kg فانطلقت بسرعة 15 m/s. احسب التغير في زخمها ومتوسط القوة إذا دام التلامس '
          '0.06 s.',
  'conclusion': 'ΔP = 9 kg·m/s، ومتوسط القوة 150 N.',
  'steps': [{'num': 1,
             'title': 'التغير في زخم الكرة',
             'law': 'ΔP = m(v_f − v_i)',
             'micro': [['الكرة ساكنة:', 'v_i = 0'],
                       ['العلاقة:', 'ΔP = m(v_f−v_i)'],
                       ['التعويض:', 'ΔP = 0.6(15−0) = 9']],
             'simple_explain': '',
             'prefix': 'ΔP = (',
             'blanks': [{'label': 'm', 'target': 0.6, 'suffix': ') × (('},
                        {'label': 'vf', 'target': 15.0, 'suffix': ') − ('},
                        {'label': 'vi', 'target': 0.0, 'suffix': '))'}],
             'has_root': False,
             'result_target': 9.0,
             'result_tol': 0.01,
             'result_label': 'احسب ΔP (kg·m/s):',
             'hint': 'انتبه أن السرعة الابتدائية تساوي صفرًا.'},
            {'num': 2,
             'title': 'متوسط القوة',
             'law': 'F_avg = ΔP/Δt',
             'micro': [['استخدم النتيجة السابقة:', 'ΔP = 9'],
                       ['العلاقة:', 'F_avg = ΔP/Δt'],
                       ['التعويض:', 'F_avg = 9/0.06 = 150 N']],
             'simple_explain': '',
             'prefix': 'F_avg = (',
             'blanks': [{'label': 'dP', 'target': 9.0, 'suffix': ') / ('},
                        {'label': 'dt', 'target': 0.06, 'suffix': ') N'}],
             'has_root': False,
             'result_target': 150.0,
             'result_tol': 0.01,
             'result_label': 'احسب F_avg (N):',
             'hint': 'عوّض ΔP = 9 والزمن 0.06.'}]},
 {'id': 'pb6',
  'title': 'تمرين الكتاب (6) · متوسط القوة',
  'type': 'interactive',
  'focus': 'F_avg = ΔP/Δt',
  'text': 'أثرت قوة مدة 0.6 s على جسم فازداد زخمه بمقدار 12 kg·m/s. احسب متوسط القوة المؤثرة.',
  'conclusion': 'متوسط القوة 20 N.',
  'steps': [{'num': 1,
             'title': 'التعويض والحساب',
             'law': 'F_avg = ΔP/Δt',
             'micro': [['العلاقة:', 'F_avg = ΔP/Δt'], ['التعويض:', 'F_avg = 12/0.6'], ['الناتج:', 'F_avg = 20 N']],
             'simple_explain': '',
             'prefix': 'F_avg = (',
             'blanks': [{'label': 'dP', 'target': 12.0, 'suffix': ') / ('},
                        {'label': 'dt', 'target': 0.6, 'suffix': ') N'}],
             'has_root': False,
             'result_target': 20.0,
             'result_tol': 0.01,
             'result_label': 'احسب F_avg (N):',
             'hint': 'اقسم 12 على 0.6.'}]},
 {'id': 'pb7',
  'title': 'تمرين الكتاب (7) · حزام الأمان',
  'type': 'interactive',
  'focus': 'أثر زمن التوقف في القوة',
  'text': 'سائق كتلته 80 kg كان يتحرك بسرعة 25 m/s ثم توقف. أوقفه حزام الأمان خلال 0.5 s، بينما قد يحدث الاصطدام '
          'بالمقود خلال 0.001 s. احسب القوتين واستنتج دور الحزام.',
  'conclusion': 'قوة الحزام −4000 N، وقوة المقود −2×10⁶ N؛ إطالة زمن التوقف تقلل القوة.',
  'steps': [{'num': 1,
             'title': 'حساب التغير في الزخم',
             'law': 'ΔP = m(v_f − v_i)',
             'micro': [['بعد التوقف:', 'v_f = 0'],
                       ['العلاقة:', 'ΔP = m(v_f−v_i)'],
                       ['التعويض:', 'ΔP = 80(0−25) = −2000']],
             'simple_explain': '',
             'prefix': 'ΔP = (',
             'blanks': [{'label': 'm', 'target': 80.0, 'suffix': ') × (('},
                        {'label': 'vf', 'target': 0.0, 'suffix': ') − ('},
                        {'label': 'vi', 'target': 25.0, 'suffix': '))'}],
             'has_root': False,
             'result_target': -2000.0,
             'result_tol': 0.01,
             'result_label': 'احسب ΔP (kg·m/s):',
             'hint': 'الإشارة السالبة تعني أن التغير عكس اتجاه الحركة.'},
            {'num': 2,
             'title': 'قوة حزام الأمان',
             'law': 'F_belt = ΔP/Δt',
             'micro': [['استخدم:', 'ΔP = −2000'], ['الزمن:', 'Δt = 0.5 s'], ['التعويض:', 'F = −2000/0.5 = −4000 N']],
             'simple_explain': '',
             'prefix': 'F_belt = (',
             'blanks': [{'label': 'dP', 'target': -2000.0, 'suffix': ') / ('},
                        {'label': 'dt', 'target': 0.5, 'suffix': ') N'}],
             'has_root': False,
             'result_target': -4000.0,
             'result_tol': 0.01,
             'result_label': 'احسب F_belt (N):',
             'hint': 'استخدم التغير في الزخم من الخطوة السابقة.'},
            {'num': 3,
             'title': 'قوة المقود دون حزام',
             'law': 'F_wheel = ΔP/Δt',
             'micro': [['التغير في الزخم نفسه:', 'ΔP = −2000'],
                       ['الزمن قصير جدًا:', 'Δt = 0.001 s'],
                       ['التعويض:', 'F = −2000/0.001 = −2×10⁶ N']],
             'simple_explain': '',
             'prefix': 'F_wheel = (',
             'blanks': [{'label': 'dP', 'target': -2000.0, 'suffix': ') / ('},
                        {'label': 'dt', 'target': 0.001, 'suffix': ') N'}],
             'has_root': False,
             'result_target': -2000000.0,
             'result_tol': 0.01,
             'result_label': 'احسب F_wheel (N):',
             'hint': 'لا تغيّر ΔP؛ الذي تغيّر هو زمن التوقف.'},
            {'num': 4,
             'title': 'الاستنتاج',
             'law': 'F_avg = ΔP/Δt',
             'micro': [['التغير في الزخم نفسه تقريبًا:', 'ΔP = ثابت'],
                       ['عند زيادة Δt:', '|F_avg| = |ΔP|/Δt'],
                       ['إذن مقدار القوة:', '|F_avg| = ?', 'يقل']],
             'type': 'symbol',
             'latex_preview': 'F_avg = ΔP/Δt',
             'prefix': 'الإجابة = ',
             'label': 'اكتب الإجابة المختصرة:',
             'suffix': '',
             'target': 'إطالة زمن التوقف تقلل القوة',
             'completed_display': 'حزام الأمان يطيل زمن توقف السائق؛ لذلك يقل مقدار القوة المؤثرة فيه.',
             'hint': 'قارن 0.5 s مع 0.001 s.'}]},
 {'id': 'pb8',
  'title': 'تمرين الكتاب (8) · السيارة والمتسابق',
  'type': 'interactive',
  'focus': 'الزخم وتحويل الوحدات',
  'text': 'تسير سيارة كتلتها 600 kg بجانب متسابق بسرعة 9 km/h، وكتلة المتسابق 60 kg. احسب زخم كل منهما، وهل يمكن '
          'للمتسابق أن يملك زخم السيارة نفسه؟',
  'conclusion': 'P_car = 1500، P_runner = 150 kg·m/s، ويلزم المتسابق سرعة 25 m/s = 90 km/h وهي غير عملية.',
  'steps': [{'num': 1,
             'title': 'تحويل السرعة إلى m/s',
             'law': 'v = v_km/h / 3.6',
             'micro': [['عامل التحويل:', '1 m/s = 3.6 km/h'], ['إذن:', 'v = 9/3.6 = 2.5 m/s']],
             'simple_explain': '',
             'prefix': 'v = (',
             'blanks': [{'label': 'vkmh', 'target': 9.0, 'suffix': ') / ('},
                        {'label': 'factor', 'target': 3.6, 'suffix': ') m/s'}],
             'has_root': False,
             'result_target': 2.5,
             'result_tol': 0.01,
             'result_label': 'احسب v (m/s):',
             'hint': 'اقسم 9 على 3.6.'},
            {'num': 2,
             'title': 'زخم السيارة',
             'law': 'P_car = m_car v',
             'micro': [['استخدم السرعة المحولة:', 'v = 2.5'], ['التعويض:', 'P_car = 600×2.5 = 1500']],
             'simple_explain': '',
             'prefix': 'P_car = (',
             'blanks': [{'label': 'mcar', 'target': 600.0, 'suffix': ') × ('},
                        {'label': 'v', 'target': 2.5, 'suffix': ')'}],
             'has_root': False,
             'result_target': 1500.0,
             'result_tol': 0.01,
             'result_label': 'احسب P_car (kg·m/s):',
             'hint': 'استخدم 2.5 m/s لا 9 km/h.'},
            {'num': 3,
             'title': 'زخم المتسابق',
             'law': 'P_runner = m_runner v',
             'micro': [['السرعة نفسها:', 'v = 2.5'], ['التعويض:', 'P_runner = 60×2.5 = 150']],
             'simple_explain': '',
             'prefix': 'P_runner = (',
             'blanks': [{'label': 'mrunner', 'target': 60.0, 'suffix': ') × ('},
                        {'label': 'v', 'target': 2.5, 'suffix': ')'}],
             'has_root': False,
             'result_target': 150.0,
             'result_tol': 0.01,
             'result_label': 'احسب P_runner (kg·m/s):',
             'hint': 'كتلة المتسابق 60 kg.'},
            {'num': 4,
             'title': 'سرعة المتسابق ليمتلك زخم السيارة',
             'law': 'v = P_car/m_runner',
             'micro': [['الزخم المطلوب:', 'P = 1500'], ['العلاقة:', 'v = P/m'], ['التعويض:', 'v = 1500/60 = 25 m/s']],
             'simple_explain': '',
             'prefix': 'v = (',
             'blanks': [{'label': 'Pcar', 'target': 1500.0, 'suffix': ') / ('},
                        {'label': 'mrunner', 'target': 60.0, 'suffix': ') m/s'}],
             'has_root': False,
             'result_target': 25.0,
             'result_tol': 0.01,
             'result_label': 'احسب السرعة المطلوبة (m/s):',
             'hint': 'استخدم زخم السيارة 1500.'},
            {'num': 5,
             'title': 'تحويل السرعة المطلوبة إلى km/h',
             'law': 'v_km/h = 3.6v',
             'micro': [['التحويل:', 'v_km/h = 3.6v'],
                       ['التعويض:', '25×3.6 = 90 km/h'],
                       ['الاستنتاج:', 'هذه سرعة لا يستطيع شخص الركض بها عادةً.']],
             'simple_explain': '',
             'prefix': 'v_km/h = (',
             'blanks': [{'label': 'v', 'target': 25.0, 'suffix': ') × ('},
                        {'label': 'factor', 'target': 3.6, 'suffix': ')'}],
             'has_root': False,
             'result_target': 90.0,
             'result_tol': 0.01,
             'result_label': 'احسب السرعة (km/h):',
             'hint': 'اضرب 25 في 3.6.'}]},
 {'id': 'pb9',
  'title': 'تمرين الكتاب (9) · السيارة والجدار',
  'type': 'interactive',
  'focus': 'الزخم والطاقة الحركية',
  'figure': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5MDAiIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgOTAwIDMwMCI+CjxkZWZzPjxtYXJrZXIgaWQ9ImEiIG1hcmtlcldpZHRoPSIxMCIgbWFya2VySGVpZ2h0PSIxMCIgcmVmWD0iOCIgcmVmWT0iMyIgb3JpZW50PSJhdXRvIj48cGF0aCBkPSJNMCwwIEwwLDYgTDksMyB6IiBmaWxsPSIjMGY0YzgxIi8+PC9tYXJrZXI+PC9kZWZzPgo8cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjMwMCIgcng9IjI0IiBmaWxsPSIjZjdmYmZmIiBzdHJva2U9IiNiOGQ3ZWQiIHN0cm9rZS13aWR0aD0iNCIvPgo8ZyBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZpbGw9IiMxNjMyNGEiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjx0ZXh0IHg9IjIyNSIgeT0iNDgiIGZvbnQtc2l6ZT0iMjYiIGZvbnQtd2VpZ2h0PSI3MDAiPtio2LnYryDYp9mE2KfYsdiq2K/Yp9ivPC90ZXh0Pjx0ZXh0IHg9IjY3NSIgeT0iNDgiIGZvbnQtc2l6ZT0iMjYiIGZvbnQtd2VpZ2h0PSI3MDAiPtmC2KjZhCDYp9mE2KfYtdi32K/Yp9mFPC90ZXh0PjwvZz4KPGcgc3Ryb2tlPSIjMzc0MTUxIiBzdHJva2Utd2lkdGg9IjYiIGZpbGw9IiNkYmVhZmUiPjxwYXRoIGQ9Ik0xMTAgMTg1aDIyMGwtMTgtNjVoLTEyMGwtNDIgNjV6Ii8+PGNpcmNsZSBjeD0iMTY1IiBjeT0iMjA3IiByPSIyOSIgZmlsbD0iIzMzNDE1NSIvPjxjaXJjbGUgY3g9IjI4NSIgY3k9IjIwNyIgcj0iMjkiIGZpbGw9IiMzMzQxNTUiLz48cGF0aCBkPSJNNTcwIDE4NWgyMjBsLTE4LTY1aC0xMjBsLTQyIDY1eiIvPjxjaXJjbGUgY3g9IjYyNSIgY3k9IjIwNyIgcj0iMjkiIGZpbGw9IiMzMzQxNTUiLz48Y2lyY2xlIGN4PSI3NDUiIGN5PSIyMDciIHI9IjI5IiBmaWxsPSIjMzM0MTU1Ii8+PC9nPgo8cGF0aCBkPSJNMTI1IDg1aDIwNSIgc3Ryb2tlPSIjMGY0YzgxIiBzdHJva2Utd2lkdGg9IjgiIG1hcmtlci1lbmQ9InVybCgjYSkiLz48dGV4dCB4PSIyMjUiIHk9Ijc4IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMzAiIGZvbnQtd2VpZ2h0PSI3MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMwZjRjODEiPnZfZiA9ICsyLjYgbS9zPC90ZXh0Pgo8cGF0aCBkPSJNNzgwIDg1SDU3NSIgc3Ryb2tlPSIjMGY0YzgxIiBzdHJva2Utd2lkdGg9IjgiIG1hcmtlci1lbmQ9InVybCgjYSkiLz48dGV4dCB4PSI2NzUiIHk9Ijc4IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMzAiIGZvbnQtd2VpZ2h0PSI3MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMwZjRjODEiPnZfaSA9IOKIkjQuNSBtL3M8L3RleHQ+Cjwvc3ZnPg==',
  'figure_caption': 'اتجاه السرعة قبل اصطدام السيارة بالجدار وبعد ارتدادها.',
  'text': 'تقترب سيارة كتلتها 1600 kg من جدار بسرعة 4.5 m/s، ثم ترتد في الاتجاه المعاكس بسرعة 2.6 m/s. احسب التغير '
          'في زخم السيارة والطاقة الحركية المفقودة.',
  'conclusion': 'ΔP = 11360 kg·m/s باتجاه الارتداد، والطاقة المفقودة 10792 J.',
  'steps': [{'num': 1,
             'title': 'تثبيت الإشارات',
             'law': 'الموجب باتجاه الارتداد',
             'micro': [['الاتجاه الموجب:', 'اتجاه الارتداد'],
                       ['قبل الاصطدام:', 'v_i = ? m/s', '-4.5'],
                       ['بعد الارتداد:', 'v_f = ? m/s', '2.6']],
             'type': 'symbol',
             'latex_preview': 'الموجب باتجاه الارتداد',
             'prefix': 'الإجابة = ',
             'label': 'اكتب الإجابة المختصرة:',
             'suffix': '',
             'target': 'v_i = -4.5 و v_f = 2.6',
             'completed_display': 'نختار اتجاه الارتداد موجبًا: v_i = −4.5 m/s، v_f = +2.6 m/s.',
             'hint': 'السرعتان متعاكستان؛ لذلك يجب أن تختلف إشارتاهما.'},
            {'num': 2,
             'title': 'التغير في الزخم',
             'law': 'ΔP = m(v_f − v_i)',
             'micro': [['عوّض بالإشارات:', 'ΔP = 1600(2.6−(−4.5))'],
                       ['اجمع داخل القوس:', '2.6+4.5 = 7.1'],
                       ['الناتج:', 'ΔP = 1600×7.1 = 11360']],
             'simple_explain': '',
             'prefix': 'ΔP = (',
             'blanks': [{'label': 'm', 'target': 1600.0, 'suffix': ') × (('},
                        {'label': 'vf', 'target': 2.6, 'suffix': ') − ('},
                        {'label': 'vi', 'target': -4.5, 'suffix': '))'}],
             'has_root': False,
             'result_target': 11360.0,
             'result_tol': 0.01,
             'result_label': 'احسب ΔP (kg·m/s):',
             'hint': 'طرح السالب يتحول إلى جمع.'},
            {'num': 3,
             'title': 'الطاقة الحركية قبل الاصطدام',
             'law': 'K_i = ½mv_i²',
             'micro': [['الطاقة لا تعتمد على اتجاه السرعة:', 'K_i = ½m|v_i|²'],
                       ['التعويض:', 'K_i = 0.5×1600×4.5² = 16200 J']],
             'simple_explain': '',
             'prefix': 'K_i = 0.5 × (',
             'blanks': [{'label': 'm', 'target': 1600.0, 'suffix': ') × ('},
                        {'label': 'vi', 'target': 4.5, 'suffix': ')² J'}],
             'has_root': False,
             'result_target': 16200.0,
             'result_tol': 0.01,
             'result_label': 'احسب K_i (J):',
             'hint': 'استخدم مقدار السرعة 4.5.'},
            {'num': 4,
             'title': 'الطاقة الحركية بعد الارتداد',
             'law': 'K_f = ½mv_f²',
             'micro': [['العلاقة:', 'K_f = ½mv_f²'], ['التعويض:', 'K_f = 0.5×1600×2.6² = 5408 J']],
             'simple_explain': '',
             'prefix': 'K_f = 0.5 × (',
             'blanks': [{'label': 'm', 'target': 1600.0, 'suffix': ') × ('},
                        {'label': 'vf', 'target': 2.6, 'suffix': ')² J'}],
             'has_root': False,
             'result_target': 5408.0,
             'result_tol': 0.01,
             'result_label': 'احسب K_f (J):',
             'hint': 'استخدم سرعة الارتداد 2.6.'},
            {'num': 5,
             'title': 'الطاقة الحركية المفقودة',
             'law': 'K_lost = K_i − K_f',
             'micro': [['استخدم القيمتين السابقتين:', 'K_lost = 16200−5408'],
                       ['الناتج:', 'K_lost = 10792 J'],
                       ['مكافئًا:', 'ΔK = −10792 J']],
             'simple_explain': '',
             'prefix': 'K_lost = (',
             'blanks': [{'label': 'Ki', 'target': 16200.0, 'suffix': ') − ('},
                        {'label': 'Kf', 'target': 5408.0, 'suffix': ') J'}],
             'has_root': False,
             'result_target': 10792.0,
             'result_tol': 0.01,
             'result_label': 'احسب K_lost (J):',
             'hint': 'الطاقة المفقودة موجبة، بينما تغير الطاقة سالب.'}]},
 {'id': 'pb10',
  'title': 'تمرين الكتاب (10) · منحنى القوة–الزمن',
  'type': 'interactive',
  'focus': 'الدفع من المساحة تحت المنحنى',
  'figure': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5MDAiIGhlaWdodD0iNDQwIiB2aWV3Qm94PSIwIDAgOTAwIDQ0MCI+CjxkZWZzPjxtYXJrZXIgaWQ9ImFycm93IiBtYXJrZXJXaWR0aD0iMTAiIG1hcmtlckhlaWdodD0iMTAiIHJlZlg9IjgiIHJlZlk9IjMiIG9yaWVudD0iYXV0byI+PHBhdGggZD0iTTAsMCBMMCw2IEw5LDMgeiIgZmlsbD0iIzFlM2E1ZiIvPjwvbWFya2VyPjwvZGVmcz4KPHJlY3Qgd2lkdGg9IjkwMCIgaGVpZ2h0PSI0NDAiIHJ4PSIyNCIgZmlsbD0iI2ZiZmRmZiIgc3Ryb2tlPSIjYjhkN2VkIiBzdHJva2Utd2lkdGg9IjQiLz4KPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTEwLDQwKSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIj4KPGxpbmUgeDE9IjAiIHkxPSIxODAiIHgyPSI2OTAiIHkyPSIxODAiIHN0cm9rZT0iIzFlM2E1ZiIgc3Ryb2tlLXdpZHRoPSI1IiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93KSIvPjxsaW5lIHgxPSIwIiB5MT0iMzUwIiB4Mj0iMCIgeTI9IjEwIiBzdHJva2U9IiMxZTNhNWYiIHN0cm9rZS13aWR0aD0iNSIgbWFya2VyLWVuZD0idXJsKCNhcnJvdykiLz4KPGxpbmUgeDE9IjAiIHkxPSI2MCIgeDI9IjMwMCIgeTI9IjMwMCIgc3Ryb2tlPSIjMGY2ZWE5IiBzdHJva2Utd2lkdGg9IjgiLz48bGluZSB4MT0iMzAwIiB5MT0iMzAwIiB4Mj0iNjAwIiB5Mj0iMzAwIiBzdHJva2U9IiMwZjZlYTkiIHN0cm9rZS13aWR0aD0iOCIvPgo8bGluZSB4MT0iMzAwIiB5MT0iMTgwIiB4Mj0iMzAwIiB5Mj0iMzAwIiBzdHJva2U9IiM5NGEzYjgiIHN0cm9rZS1kYXNoYXJyYXk9IjEwIDEwIiBzdHJva2Utd2lkdGg9IjMiLz48bGluZSB4MT0iMCIgeTE9IjMwMCIgeDI9IjYwMCIgeTI9IjMwMCIgc3Ryb2tlPSIjOTRhM2I4IiBzdHJva2UtZGFzaGFycmF5PSIxMCAxMCIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxnIGZpbGw9IiMxZTI5M2IiIGZvbnQtc2l6ZT0iMjgiIGZvbnQtd2VpZ2h0PSI3MDAiPjx0ZXh0IHg9Ii00OCIgeT0iNzAiPjEwPC90ZXh0Pjx0ZXh0IHg9Ii02MiIgeT0iMzEwIj7iiJIxMDwvdGV4dD48dGV4dCB4PSIxNDUiIHk9IjIxNiI+MjwvdGV4dD48dGV4dCB4PSIyOTAiIHk9IjIxNiI+NDwvdGV4dD48dGV4dCB4PSI1OTAiIHk9IjIxNiI+NjwvdGV4dD48dGV4dCB4PSI2MjAiIHk9IjIyMCI+dCAocyk8L3RleHQ+PHRleHQgeD0iLTg1IiB5PSIzMCI+RiAoTik8L3RleHQ+PC9nPgo8L2c+PC9zdmc+',
  'figure_caption': 'القوة تهبط خطيًا من +10 N عند t=0 إلى −10 N عند t=4، ثم تثبت حتى t=6 s.',
  'text': 'جسم كتلته 2 kg يتحرك بسرعة 5 m/s على سطح أملس. أثرت فيه القوة الممثلة بيانيًا. احسب دفع القوة خلال 4 s و6 '
          's، وأكبر سرعة في اتجاه الحركة، وزمن التوقف، ومتوسط القوة حتى التوقف.',
  'conclusion': 'I₄ = 0، I₆ = −20 N·s، v_max = 10 m/s، زمن التوقف 5 s، ومتوسط القوة −2 N.',
  'steps': [{'num': 1,
             'title': 'الدفع الموجب حتى t = 2 s',
             'law': 'I₊ = area of triangle',
             'micro': [['المساحة مثلث:', 'I₊ = ½×base×height'], ['التعويض:', 'I₊ = ½×2×10 = 10 N·s']],
             'simple_explain': '',
             'prefix': 'I₊ = 0.5 × (',
             'blanks': [{'label': 'base', 'target': 2.0, 'suffix': ') × ('},
                        {'label': 'height', 'target': 10.0, 'suffix': ') N·s'}],
             'has_root': False,
             'result_target': 10.0,
             'result_tol': 0.01,
             'result_label': 'احسب I₊ (N·s):',
             'hint': 'احسب مساحة المثلث فوق محور الزمن.'},
            {'num': 2,
             'title': 'أكبر سرعة في اتجاه الحركة',
             'law': 'I = m(v_2 − v_i)',
             'micro': [['نهاية الدفع الموجب عند t=2:', 'I = 10'],
                       ['طبق:', '10 = 2(v_2−5)'],
                       ['اعزل السرعة:', 'v_2 = 5+10/2 = 10 m/s']],
             'simple_explain': '',
             'prefix': 'v_2 = ((',
             'blanks': [{'label': 'I', 'target': 10.0, 'suffix': ') / ('},
                        {'label': 'm', 'target': 2.0, 'suffix': ')) + ('},
                        {'label': 'vi', 'target': 5.0, 'suffix': ') m/s'}],
             'has_root': False,
             'result_target': 10.0,
             'result_tol': 0.01,
             'result_label': 'احسب v_max (m/s):',
             'hint': 'أكبر سرعة تكون عند نهاية الجزء الموجب.'},
            {'num': 3,
             'title': 'الدفع الكلي خلال 4 s',
             'law': 'I₄ = I₊ + I₋',
             'micro': [['المثلث الموجب:', 'I₊ = +10'],
                       ['المثلث السالب من 2 إلى4:', 'I₋ = −½×2×10 = −10'],
                       ['الجمع:', 'I₄ = 10−10 = 0']],
             'simple_explain': '',
             'prefix': 'I₄ = (',
             'blanks': [{'label': 'positive', 'target': 10.0, 'suffix': ') + ('},
                        {'label': 'negative', 'target': -10.0, 'suffix': ') N·s'}],
             'has_root': False,
             'result_target': 0.0,
             'result_tol': 0.01,
             'result_label': 'احسب I₄ (N·s):',
             'hint': 'المساحتان متساويتان ومتعاكستان.'},
            {'num': 4,
             'title': 'الدفع الكلي خلال 6 s',
             'law': 'I₆ = I₄ + rectangle 4→6',
             'micro': [['حتى t=4:', 'I₄ = 0'],
                       ['من 4 إلى6:', 'I = FΔt = −10×2 = −20'],
                       ['الجمع:', 'I₆ = 0−20 = −20 N·s']],
             'simple_explain': '',
             'prefix': 'I₆ = (',
             'blanks': [{'label': 'I4', 'target': 0.0, 'suffix': ') + ('},
                        {'label': 'rect', 'target': -20.0, 'suffix': ') N·s'}],
             'has_root': False,
             'result_target': -20.0,
             'result_tol': 0.01,
             'result_label': 'احسب I₆ (N·s):',
             'hint': 'بعد t=4 القوة ثابتة عند −10 N.'},
            {'num': 5,
             'title': 'زمن توقف الجسم',
             'law': 'I_stop = ΔP = m(0−v_i)',
             'micro': [['الزخم الابتدائي:', 'P_i = 2×5 = 10'],
                       ['للتوقف نحتاج دفعًا كليًا:', 'I_stop = −10'],
                       ['عند t=4 الدفع الكلي صفر:', 'I₄ = 0'],
                       ['بعد t=4، F = −10 N؛ نحتاج ثانية واحدة:', 'Δt = (−10)/(−10) = 1 s'],
                       ['إذن:', 't_stop = 4+1 = 5 s']],
             'simple_explain': '',
             'prefix': 't_stop = (',
             'blanks': [{'label': 't4', 'target': 4.0, 'suffix': ') + ('},
                        {'label': 'extra', 'target': 1.0, 'suffix': ') s'}],
             'has_root': False,
             'result_target': 5.0,
             'result_tol': 0.01,
             'result_label': 'احسب t_stop (s):',
             'hint': 'عند t=4 عاد الزخم إلى قيمته الابتدائية؛ ثم يحتاج ثانية إضافية عند −10 N.'},
            {'num': 6,
             'title': 'متوسط القوة حتى التوقف',
             'law': 'F_avg = I_stop/Δt',
             'micro': [['الدفع حتى التوقف:', 'I_stop = ΔP = 2(0−5) = −10'],
                       ['الزمن الكلي:', 'Δt = 5 s'],
                       ['التعويض:', 'F_avg = −10/5 = −2 N']],
             'simple_explain': '',
             'prefix': 'F_avg = (',
             'blanks': [{'label': 'Istop', 'target': -10.0, 'suffix': ') / ('},
                        {'label': 'tstop', 'target': 5.0, 'suffix': ') N'}],
             'has_root': False,
             'result_target': -2.0,
             'result_tol': 0.01,
             'result_label': 'احسب F_avg (N):',
             'hint': 'استخدم الدفع الكلي حتى السكون لا الدفع عند 6 s.'}]}]

# تمرين الكتاب (3) · علل — خطوات فقط دون خانة إجابة نهائية
for _q3 in questions_db:
    if _q3.get('id') == 'pb3':
        for _s3 in _q3.get('steps', []):
            _s3['micro_only'] = True

PB3_CHOICES = {
    "1": {
        "choices": [
            "زمن التوقف على الرمل أطول فيزداد دفع القوة، ولهذا تكون القوة المؤثرة على البيضة أصغر.",
            "التغير في الزخم واحد في الحالتين، والرمل يُطيل زمن التوقف؛ ولأن F = ΔP ÷ Δt تصغر القوة فلا تنكسر البيضة.",
            "الرمل يُقلل سرعة البيضة قبل وصولها فيصغر التغير في زخمها، ولهذا تصغر القوة."
        ],
        "answer_index": 1
    },
    "2": {
        "choices": [
            "طول الماسورة يُبقي القوة مؤثرة زمنًا أطول فيزداد الدفع I = F × Δt، والدفع هو التغير في الزخم فتخرج القذيفة بسرعة أكبر.",
            "طول الماسورة يزيد قوة الغازات المؤثرة على القذيفة فيزداد الدفع وتزداد السرعة.",
            "طول الماسورة يُقلل كتلة القذيفة الفعّالة، ولأن الزخم محفوظ تزداد سرعتها."
        ],
        "answer_index": 0
    },
    "3": {
        "choices": [
            "القوة المؤثرة على المدفع أصغر من القوة المؤثرة على القذيفة، ولهذا تكون سرعة ارتداده أصغر.",
            "كتلة المدفع الكبيرة تجعل زخمه أصغر من زخم القذيفة، فتكون سرعة ارتداده أصغر.",
            "الزخمان متساويان في المقدار ومتعاكسان في الاتجاه، وكتلة المدفع أكبر بكثير فتكون سرعة ارتداده أصغر بكثير."
        ],
        "answer_index": 2
    }
}
for _q3 in questions_db:
    if _q3.get('id') == 'pb3':
        for _s3 in _q3.get('steps', []):
            _c3 = PB3_CHOICES.get(str(_s3.get('num'))) or PB3_CHOICES.get(_s3.get('num'))
            if _c3:
                _s3['choices'] = list(_c3['choices'])
                _s3['answer_index'] = _c3['answer_index']

TOTAL_QUESTIONS = len(questions_db)

FORMULA_SHEET = [['الزخم الخطي', 'P = m v'],
 ['الدفع', 'I = F_avg Δt'],
 ['نظرية الدفع–الزخم', 'I = ΔP = m(v_f − v_i)'],
 ['متوسط القوة', 'F_avg = ΔP/Δt'],
 ['حفظ الزخم', 'ΣP_i = ΣP_f'],
 ['الطاقة الحركية', 'K = ½m v²'],
 ['الطاقة والزخم', 'K = P²/(2m)'],
 ['تحويل السرعة', 'v(m/s) = v(km/h)/3.6']]

STUDY_TIPS = [
    "🧠 نصيحة: اكتب دائماً وحدات القياس بجانب كل رقم لتتجنب الأخطاء.",
    "🧠 نصيحة: انتبه لإشارة السرعة عند تغيّر اتجاه الحركة (لأعلى/لأسفل).",
    "🧠 نصيحة: تحقق من القانون المناسب قبل التعويض المباشر بالأرقام.",
    "🧠 نصيحة: التمرين المتكرر يرسخ خطوات الحل في ذهنك بشكل أسرع.",
    "🧠 نصيحة: استخدم زر التلميح تدريجياً بدل النظر للحل مباشرة.",
]

SUCCESS_PHRASES = ["أحسنت! 👏🏼", "رائع جداً! 🌟", "ممتاز! 🔥", "عمل احترافي! 🚀", "بالضبط! 🎯"]

# ==========================================================
# 4. إدارة الحالة (Session State)
# ==========================================================
def init_state():
    defaults = {
        "physbook_student_name": "", "physbook_total_xp": 0, "physbook_streak": 0,
        "physbook_badges": set(), "physbook_completed_questions": set(),
        "physbook_no_hint_flag": {}, "physbook_attempts": {}, "physbook_hint_level": {},
        "physbook_start_time": {}, "physbook_time_spent": {},
        "physbook_daily_tip": random.choice(STUDY_TIPS),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
if st.session_state.get("student_profile") and not st.session_state.get("physbook_student_name"):
    st.session_state["physbook_student_name"] = st.session_state["student_profile"].get("name", "")

def award_badge(name):
    if name not in st.session_state["physbook_badges"]:
        st.session_state["physbook_badges"].add(name)
        if hasattr(st, "toast"):
            st.toast(f"🏅 وسام جديد: {name}", icon="🏅")

def normalize_symbol(symbol_str: str, case_sensitive: bool = False) -> str:
    """توحيد صيغة الإجابة الرمزية للمقارنة (حذف الفراغات/الشرطات السفلية/النجوم)."""
    if not symbol_str:
        return ""
    cleaned = symbol_str.replace(" ", "").replace("_", "").replace("*", "")
    return cleaned if case_sensitive else cleaned.lower()

_COMM_SUBS = (("×", "*"), ("·", "*"), ("∙", "*"), ("÷", "/"),
              ("−", "-"), ("–", "-"), ("—", "-"), (",", "."))

def _comm_term(term: str) -> str:
    factors = [f for f in term.split("*") if f]
    if len(factors) == 1 and not any(ch.isdigit() for ch in factors[0]):
        return "".join(sorted(factors[0]))
    return "*".join(sorted(factors))

def _comm_key(text, case_sensitive: bool = False) -> str:
    """مفتاح مقارنة يتجاهل ترتيب الرموز في الضرب والجمع وجهتي المساواة."""
    t = str(text or "")
    for a, b in _COMM_SUBS:
        t = t.replace(a, b)
    for ch in (" ", " ", "_", "{", "}", "(", ")"):
        t = t.replace(ch, "")
    if not case_sensitive:
        t = t.lower()
    if any("؀" <= c <= "ۿ" for c in t):
        return t
    sides = []
    for side in t.split("="):
        if len(side) > 14 or "/" in side or "-" in side:
            sides.append(side)
            continue
        terms = [_comm_term(x) for x in side.split("+") if x]
        sides.append("+".join(sorted(terms)))
    return "=".join(sorted(sides))

def symbol_answers_match(user_val, target, case_sensitive: bool = False) -> bool:
    """مقارنة مرنة: تقبل إعادة ترتيب الرموز (الضرب تبديلي)."""
    if normalize_symbol(user_val, case_sensitive) == normalize_symbol(target, case_sensitive):
        return True
    ku, kt = _comm_key(user_val, case_sensitive), _comm_key(target, case_sensitive)
    return bool(ku) and ku == kt

def eq_html(tex: str) -> str:
    """يحول معادلة LaTeX البسيطة إلى HTML عملي يُقرأ من اليسار إلى اليمين (بدون KaTeX)."""
    if not tex:
        return ""

    def grab(s, i):
        # i يشير إلى "{" ويعيد (المحتوى، الفهرس بعد "}")
        depth, start, j = 0, i + 1, i
        while j < len(s):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    return s[start:j], j + 1
            j += 1
        return s[start:], len(s)

    def conv(s):
        out, i, n = [], 0, len(s)
        while i < n:
            c = s[i]

            if s.startswith(r"\frac", i) or s.startswith(r"\dfrac", i):
                j = i + (6 if s.startswith(r"\dfrac", i) else 5)
                while j < n and s[j] == " ":
                    j += 1
                num, j = grab(s, j) if j < n and s[j] == "{" else ("", j)
                while j < n and s[j] == " ":
                    j += 1
                den, j = grab(s, j) if j < n and s[j] == "{" else ("", j)
                out.append(
                    '<span class="eq-fr"><span class="eq-num">' + conv(num)
                    + '</span><span class="eq-den">' + conv(den) + "</span></span>"
                )
                i = j
                continue

            if s.startswith(r"\mathbf", i) or s.startswith(r"\bm", i):
                j = i + (7 if s.startswith(r"\mathbf", i) else 3)
                body, j = grab(s, j) if j < n and s[j] == "{" else ("", j)
                if body.strip() == "?":
                    # مكان خانة إدخال الطالب داخل المعادلة نفسها
                    out.append('<span class="eq-slot"><b class="eq-unk">?</b></span>')
                else:
                    out.append('<b class="eq-unk">' + conv(body) + "</b>")
                i = j
                continue

            if s.startswith(r"\text", i) or s.startswith(r"\mathrm", i):
                j = i + (5 if s.startswith(r"\text", i) else 7)
                body, j = grab(s, j) if j < n and s[j] == "{" else ("", j)
                out.append('<span class="eq-txt">' + body.replace(" ", "&nbsp;") + "</span>")
                i = j
                continue

            if s.startswith(r"\sqrt", i):
                j = i + 5
                body, j = grab(s, j) if j < n and s[j] == "{" else ("", j)
                out.append('&radic;<span class="eq-rt">' + conv(body) + "</span>")
                i = j
                continue

            if s.startswith(r"\cdot", i):
                out.append('<span class="eq-op">&middot;</span>')
                i += 5
                continue
            if s.startswith(r"\times", i):
                out.append('<span class="eq-op">&times;</span>')
                i += 6
                continue
            if s.startswith(r"\left", i):
                i += 5
                continue
            if s.startswith(r"\right", i):
                i += 6
                continue
            if s.startswith(r"\,", i) or s.startswith(r"\;", i) or s.startswith("\\ ", i):
                out.append("&nbsp;")
                i += 2
                continue

            if c in "_^":
                tag = "sub" if c == "_" else "sup"
                j = i + 1
                if j < n and s[j] == "{":
                    body, j = grab(s, j)
                else:
                    body = s[j] if j < n else ""
                    j += 1
                out.append("<" + tag + ">" + conv(body) + "</" + tag + ">")
                i = j
                continue

            if c == "=":
                out.append('<span class="eq-eq">=</span>')
                i += 1
                continue
            if c == "+":
                out.append('<span class="eq-op">+</span>')
                i += 1
                continue
            if c == "-":
                out.append('<span class="eq-op">&minus;</span>')
                i += 1
                continue
            if c == "/":
                out.append('<span class="eq-op">/</span>')
                i += 1
                continue
            if c == "\\":
                i += 1
                continue

            out.append(c)
            i += 1
        return "".join(out)

    return '<span class="eq">' + conv(str(tex).strip()) + "</span>"


# ---- تحويل أي عبارة مكتوبة بشكل عادي إلى شكل latex جميل (كسور حقيقية ودلالات) ----
_SUPS = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
         "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁺": "+", "⁻": "-", "ⁿ": "n"}
_SUBSU = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5",
          "₆": "6", "₇": "7", "₈": "8", "₉": "9", "₊": "+", "₋": "-"}
_VULGAR = {"½": ("1", "2"), "⅓": ("1", "3"), "⅔": ("2", "3"), "¼": ("1", "4"), "¾": ("3", "4"),
           "⅕": ("1", "5"), "⅖": ("2", "5"), "⅗": ("3", "5"), "⅘": ("4", "5"),
           "⅙": ("1", "6"), "⅚": ("5", "6"), "⅛": ("1", "8"), "⅜": ("3", "8"),
           "⅝": ("5", "8"), "⅞": ("7", "8")}
# الوحدات تُحمى قبل التحويل حتى لا تصير Kg.m/s كسراً
_UNIT_TOKENS = ["Kg.m/s²", "kg.m/s²", "Kg.m/s", "kg.m/s", "Kg·m/s", "kg·m/s",
                "N.s", "N·s", "m/s²", "m/s^2", "m/s", "km/h", "J/kg"]
_REL_SEPS = ["=", "⇒", "⇔", "⇐", "≈", "≠", "≤", "≥", "→", "+", " - "]


def _grab_group(s, i):
    """يعيد (محتوى القوس المتوازن، الفهرس بعد إغلاقه) ابتداءً من i."""
    depth, j = 0, i
    while j < len(s):
        if s[j] in "([{":
            depth += 1
        elif s[j] in ")]}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def _split_top(s, seps):
    """يقسم النص عند الفواصل الموجودة خارج الأقواس فقط."""
    parts, cur, depth, i, n = [], "", 0, 0, len(s)
    while i < n:
        c = s[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth = max(0, depth - 1)
        elif depth == 0:
            hit = ""
            for sep in seps:
                if s.startswith(sep, i):
                    hit = sep
                    break
            if hit:
                parts.append((cur, hit))
                cur = ""
                i += len(hit)
                continue
        cur += c
        i += 1
    parts.append((cur, ""))
    return parts


def _is_single_frac(t: str) -> bool:
    if not t.startswith("\\frac{"):
        return False
    _num, j = _grab_group(t, 5)
    if j >= len(t) or t[j] != "{":
        return False
    _den, j2 = _grab_group(t, j)
    return j2 == len(t)


def _groups_pass(t: str) -> str:
    """يدخل داخل الأقواس لتحويل ما فيها من قسمة إلى كسور."""
    out, i, n = [], 0, len(t)
    while i < n:
        c = t[i]
        if c in "([":
            body, j = _grab_group(t, i)
            conv = _frac_pass(body)
            nxt = t[j] if j < n else ""
            if _is_single_frac(conv) and nxt not in "^_":
                out.append(conv)
            else:
                out.append(c + conv + (")" if c == "(" else "]"))
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _atom(p: str) -> str:
    p = p.strip()
    if not p:
        return p
    if p[0] in "([":
        body, j = _grab_group(p, 0)
        if j == len(p):
            return _frac_pass(body)
    return _groups_pass(p)


def _term_to_frac(t: str) -> str:
    raw = t.strip()
    if not raw:
        return ""
    parts = [p for (p, _s) in _split_top(raw, ["/"])]
    if len(parts) < 2:
        return _groups_pass(raw)
    cur = _atom(parts[0])
    for p in parts[1:]:
        cur = "\\frac{" + cur + "}{" + _atom(p) + "}"
    return cur


def _frac_pass(tex: str) -> str:
    out = []
    for chunk, sep in _split_top(tex, _REL_SEPS):
        out.append(_term_to_frac(chunk))
        if sep:
            out.append(" " + sep.strip() + " ")
    return "".join(out)


def plain_to_tex(expr) -> str:
    """يحول عبارة مثل \"K₁ = ( ⅔ p₂ )² / (2m₁)\" إلى LaTeX مكافئ."""
    s = str(expr).strip()
    if not s:
        return ""
    units = []
    for tok in _UNIT_TOKENS:
        while tok in s:
            s = s.replace(tok, "@U" + str(len(units)) + "@", 1)
            units.append(tok)
    s = s.replace("?", "@Q@")
    for ch, (a, b) in _VULGAR.items():
        s = s.replace(ch, "\\frac{" + a + "}{" + b + "}")
    s = s.replace("×", " \\times ").replace("·", " \\cdot ").replace("∙", " \\cdot ")
    s = s.replace("*", " \\cdot ").replace("÷", " / ")
    s = s.replace("−", "-").replace("–", "-")

    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c in _SUPS:
            buf, j = "", i
            while j < n and s[j] in _SUPS:
                buf += _SUPS[s[j]]
                j += 1
            out.append("^{" + buf + "}")
            i = j
            continue
        if c in _SUBSU:
            buf, j = "", i
            while j < n and s[j] in _SUBSU:
                buf += _SUBSU[s[j]]
                j += 1
            out.append("_{" + buf + "}")
            i = j
            continue
        if c in "_^" and i + 1 < n and s[i + 1] != "{":
            j, buf = i + 1, ""
            while j < n and s[j] not in " =+-/*()[]{}\u00b7\u00d7\u21d2\u060c,":
                buf += s[j]
                j += 1
            out.append(c + "{" + buf + "}")
            i = j
            continue
        if c == "√":
            j = i + 1
            while j < n and s[j] == " ":
                j += 1
            if j < n and s[j] in "([":
                body, j2 = _grab_group(s, j)
                out.append("\\sqrt{" + plain_to_tex(body) + "}")
                i = j2
                continue
            buf = ""
            while j < n and s[j] not in " =+-/\u00d7\u00b7\u21d2":
                buf += s[j]
                j += 1
            out.append("\\sqrt{" + plain_to_tex(buf) + "}")
            i = j
            continue
        out.append(c)
        i += 1

    tex = _frac_pass("".join(out))
    for idx, tok in enumerate(units):
        tex = tex.replace("@U" + str(idx) + "@", "\\text{" + tok + "}")
    tex = tex.replace("@Q@", "\\mathbf{?}")
    return tex


def plain_to_eq(expr) -> str:
    """يعرض أي عبارة عادية بشكل معادلة جميلة (نفس أسلوب معادلة الإدخال)."""
    return eq_html(plain_to_tex(expr))


def _is_ar(ch: str) -> bool:
    return ("\u0600" <= ch <= "\u06ff") or ("\u0750" <= ch <= "\u077f") or ("\ufb50" <= ch <= "\ufeff")


def _split_ar_math(raw: str):
    """يفصل النص المختلط إلى مقاطع عربية ومقاطع رياضية."""
    segs, buf, mode = [], "", None
    for ch in raw:
        if _is_ar(ch):
            kind = "ar"
        elif ch in " \t":
            kind = mode if mode else "math"
        else:
            kind = "math"
        if mode is None:
            mode, buf = kind, ch
        elif kind == mode:
            buf += ch
        else:
            segs.append((mode, buf))
            mode, buf = kind, ch
    if mode is not None:
        segs.append((mode, buf))

    merged = []
    for m, t in segs:
        if merged and m == "ar" and merged[-1][0] == "math" and merged[-1][1].rstrip().endswith(("_", "^", "{")):
            merged[-1] = ("math", merged[-1][1] + t)
        else:
            merged.append((m, t))
    return [(m, t) for m, t in merged if t.strip()]


def _is_expr(t: str) -> bool:
    core = t.strip()
    if len(core) < 3:
        return False
    if "=" not in core and "⇒" not in core:
        return False
    return any(ch.isalnum() for ch in core)


def mixed_math_html(text, eq_cls: str = "law-eq", note_cls: str = "law-note") -> str:
    """يعرض العبارات الرياضية بشكل latex ويترك النص العربي كما هو."""
    raw = str(text).strip()
    if not raw:
        return ""
    segs = _split_ar_math(raw)
    if not segs:
        return ""
    if not any(m == "ar" for m, _t in segs):
        return '<span class="' + eq_cls + '">' + plain_to_eq(raw) + "</span>"
    if not any(m == "math" and _is_expr(t) for m, t in segs):
        body = ""
        for m, t in segs:
            if m == "ar" or not any(ch.isalnum() for ch in t):
                body += t
            else:
                body += '<span class="eq-inline">' + plain_to_eq(t) + "</span>"
        return '<span class="' + note_cls + '">' + body + "</span>"
    out = ""
    for m, t in segs:
        if m == "ar":
            out += '<span class="' + note_cls + '">' + t.strip() + "</span>"
        elif _is_expr(t) or any(ch.isalnum() for ch in t):
            out += '<span class="' + eq_cls + '">' + plain_to_eq(t) + "</span>"
    return out


def result_eq_parts(label):
    """يستخرج رمز الناتج ووحدته من نص المطلوب: 'احسب ... v (m/s):' -> (v, m/s)"""
    txt = str(label or "").strip()
    while txt.endswith(":"):
        txt = txt[:-1].strip()
    unit = ""
    i = txt.rfind("(")
    j = txt.rfind(")")
    if i != -1 and j > i:
        unit = txt[i + 1:j].strip()
        txt = txt[:i].strip()
    tail = txt.split(" ")[-1] if txt else ""
    has_lat = any(("a" <= c <= "z") or ("A" <= c <= "Z") for c in tail)
    has_ar = any("\u0600" <= c <= "\u06ff" for c in tail)
    sym = tail if (tail and has_lat and not has_ar) else "الناتج"
    return sym, unit


DERIVE_STEPS = {
    # ---------------------------------------------------------------- q1
    ("q1", 1): [
        ("📘 معادلة مدروسة في منهاج الصف 11 — الحركة الرأسية (الصاديّة) حيث ‏a_y = - g ، المعادلة المستقلة عن الزمن:", "v²_yf = v²_yi - 2 · g · ( y_f - y_i )"),
        ("نطبّقها على حالة تمريننا: نأخذ مبدأ المحاور عند نقطة الرمي، فالموضع الابتدائي:", "y_i = ?", "0"),
        ("والموضع النهائي هو الارتفاع h المذكور في التمرين:", "y_f = ?", "h"),
        ("والسرعة الابتدائية على المحور الرأسي هي سرعة الرمي نفسها:", "v_yi = ?", "v₀|v0"),
        ("عوّض هذه القيم في المعادلة:", "v² = v₀² - 2 · g · ( ? - 0 )", "h"),
        ("بسّط ما بين القوسين — هذه هي العلاقة المستعملة في الحل:", "v² = v₀² - ?", "2gh"),
    ],
    ("q1", 2): [
        ("القانون المدروس — تعريف الزخم الخطي (العلاقة 1-1):", "p = m · v"),
        ("الزخم كمية متجهة اتجاهها اتجاه السرعة، ومقياسها جداء الكتلة في السرعة اللحظية:", "p = m · ?", "v"),
        ("السرعة v هي التي استنتجتها في الخطوة 1 — إذن العلاقة جاهزة للتطبيق:", "p = m · v"),
    ],
    # ---------------------------------------------------------------- q2
    ("q2", 1): [
        ("القانون المدروس — الطاقة الحركية:", "K = ½ · m · v²"),
        ("اضرب البسط والمقام في الكتلة m لإظهار الزخم داخل العبارة:", "K = ( m² · v² ) / ( 2 · ? )", "m"),
        ("وبما أن p = m · v فإن m² · v² = p²، فتصبح الطاقة بدلالة الزخم:", "K = p² / ( 2 · ? )", "m"),
        ("طبّق هذه الصيغة على الجسم الأول:", "K₁ = p₁² / ( 2 · ? )", "m₁"),
        ("المعطى في نص التمرين: زخم الجسم الأول يساوي ثلثي زخم الثاني:", "p₁ = ? · p₂", "2/3|⅔"),
        ("عوّض بـ p₁ داخل عبارة K₁ — هذه هي العبارة المستعملة في هذه الخطوة:", "K₁ = ( ⅔ · p₂ )² / ( 2 · ? )", "m₁"),
    ],
    ("q2", 2): [
        ("نفس القانون المدروس مكتوباً بدلالة الزخم:", "K = p² / ( 2 · m )"),
        ("طبّقه على الجسم الثاني:", "K₂ = p₂² / ( 2 · ? )", "m₂"),
        ("المعطى: كتلة الجسم الثاني ضِعف كتلة الأول:", "m₂ = ? · m₁", "2"),
        ("عوّض بها داخل عبارة K₂ — هذه هي العبارة المستعملة:", "K₂ = p₂² / ( 2 · ? )", "2m₁"),
    ],
    ("q2", 3): [
        ("من الخطوة 1:", "K₁ = ( 4/9 ) · p₂² / ( 2 · m₁ )"),
        ("ومن الخطوة 2:", "K₂ = p₂² / ( 4 · m₁ )"),
        ("اقسم K₁ على K₂ (قسمة كسر على كسر = ضرب في المقلوب):", "K₁ / K₂ = ( 4/9 ) · ( 4 · m₁ ) / ( 2 · ? )", "m₁"),
        ("اختصر p₂² و m₁ لوجودهما في البسط والمقام:", "K₁ / K₂ = ( 4/9 ) · ?", "2"),
        ("أنجز العملية العددية — هذه هي النسبة المطلوبة:", "K₁ / K₂ = ?", "8/9"),
    ],
    ("q2", 4): [
        ("المعطى في نص التمرين — مجموع الطاقتين:", "K₁ + K₂ = 68"),
        ("من النسبة المستنتجة في الخطوة 3، اكتب K₁ بدلالة K₂:", "K₁ = ( 8/9 ) · ?", "K₂"),
        ("عوّض في معادلة المجموع:", "( 8/9 ) · K₂ + K₂ = ?", "68"),
        ("اجمع الحدّين المتشابهين:", "( ? ) · K₂ = 68", "17/9"),
        ("استخرج K₂ — هذه هي العلاقة المستعملة:", "K₂ = 68 · 9 / ?", "17"),
    ],
    # ---------------------------------------------------------------- q3
    ("q3", 1): [
        ("القانون المدروس — الطاقة الحركية بدلالة الزخم:", "K = p² / ( 2 · m )"),
        ("اضرب الطرفين في 2m لاستخراج مربع الزخم:", "p² = 2 · m · ?", "K"),
        ("طبّقها على الجسم الأول:", "p₁² = 2 · m₁ · ?", "K₁"),
        ("المعطى: كتلة الأول ضِعف كتلة الثاني:", "m₁ = ? · m₂", "2"),
        ("عوّض بالكتلة وبالمعطى K₁ = 2K₂ — هذه هي العبارة المستعملة:", "p₁² = 2 · ( 2m₂ ) · ?", "2K₂"),
    ],
    ("q3", 2): [
        ("طبّق نفس القانون على الجسم الثاني:", "p₂² = 2 · m₂ · K₂"),
        ("اقسم عبارة p₁² على عبارة p₂²:", "p₁² / p₂² = [ 2 · ( 2m₂ ) · ( 2K₂ ) ] / [ 2 · m₂ · ? ]", "K₂"),
        ("اختصر m₂ و K₂ ثم أنجز العملية:", "p₁² / p₂² = ?", "4"),
        ("خذ الجذر التربيعي للطرفين — هذه هي النسبة المستعملة:", "p₁ / p₂ = ?", "2"),
    ],
    ("q3", 3): [
        ("المعطى في نص التمرين — مجموع الزخمين:", "p₁ + p₂ = 90"),
        ("من النسبة المستنتجة في الخطوة 2:", "p₁ = 2 · ?", "p₂"),
        ("عوّض في معادلة المجموع:", "2 · p₂ + p₂ = ?", "90"),
        ("اجمع الحدّين المتشابهين:", "? · p₂ = 90", "3"),
        ("استخرج p₂ — هذه هي العلاقة المستعملة:", "p₂ = 90 / ?", "3"),
    ],
    ("q3", 4): [
        ("من النسبة المستنتجة في الخطوة 2:", "p₁ / p₂ = 2"),
        ("اضرب الطرفين في p₂ — هذه هي العلاقة المستعملة:", "p₁ = 2 · ?", "p₂"),
    ],
    # ---------------------------------------------------------------- q4
    ("q4", 1): [
        ("📘 معادلة مدروسة في منهاج الصف 11 — الحركة الرأسية (الصاديّة) حيث ‏a_y = - g ، المعادلة المستقلة عن الزمن:", "v²_yf = v²_yi - 2 · g · ( y_f - y_i )"),
        ("نطبّقها على حالة تمريننا: مبدأ المحاور عند نقطة الرمي، فالموضع الابتدائي:", "y_i = ?", "0"),
        ("والموضع النهائي هو ارتفاع السقف h:", "y_f = ?", "h"),
        ("والسرعة الابتدائية هي سرعة الرمي:", "v_yi = ?", "v₀|v0"),
        ("والسرعة النهائية هي سرعة الوصول إلى السقف:", "v_yf = ?", "v₁|v1"),
        ("عوّض هذه القيم في المعادلة:", "v₁² = v₀² - 2 · g · ( ? - 0 )", "h"),
        ("بسّط — هذه هي العلاقة المستعملة عند الوصول إلى السقف:", "v₁² = v₀² - ?", "2gh"),
    ],
    ("q4", 2): [
        ("القانون المدروس — نظرية الدفع والزخم:", "I = Δp = p₂ - p₁"),
        ("اكتب زخم الكرة قبل الارتطام بالسقف:", "p₁ = m · ?", "v₁"),
        ("واكتب زخمها بعد الارتداد:", "p₂ = m · ?", "v₂"),
        ("عوّض الزخمين في النظرية:", "I = m · v₂ - m · ?", "v₁"),
        ("أخرج الكتلة m عاملاً مشتركاً:", "I = m · ( ? )", "v₂-v₁"),
        ("المطلوب مقدار الدفع والسرعتان متعاكستان، لذلك نأخذ القيمة المطلقة — العلاقة المستعملة:", "I = | m · ( ? ) |", "v₂-v₁"),
    ],
    ("q4", 3): [
        ("القانون المدروس — دفع محصلة القوى (العلاقة 1-3):", "I = ΣF · Δt"),
        ("أثناء التلامس تؤثر على الكرة قوتان نحو الأسفل: قوة السقف F والوزن m·g. اكتب المحصلة:", "ΣF = F + ?", "mg"),
        ("عوّض المحصلة في القانون:", "I = ( F + m · g ) · ?", "Δt|dt|t"),
        ("اقسم الطرفين على زمن التلامس Δt:", "I / Δt = F + ?", "mg"),
        ("استخرج قوة السقف F — هذه هي العلاقة المستعملة:", "F = ( I / Δt ) - ?", "mg"),
    ],
    # ---------------------------------------------------------------- q5
    ("q5", 1): [
        ("القانون المدروس — نظرية الدفع والزخم (العلاقة 1-5):", "I = F · Δt = Δp"),
        ("القوة الوحيدة المؤثرة طوال زمن التحليق هي الوزن، والاتجاه نحو الأعلى موجب:", "F = - ?", "mg"),
        ("ينطلق الجسم بسرعة v₀ نحو الأعلى ويعود إلى نقطة الانطلاق بنفس السرعة نحو الأسفل:", "Δp = m · ( - v₀ ) - ?", "mv₀"),
        ("أنجز العملية في الطرف الأيمن:", "Δp = ?", "-2mv₀"),
        ("عوّض في النظرية، وزمن التأثير هو زمن التحليق t:", "- m · g · t = ?", "-2mv₀"),
        ("اختصر الكتلة m والإشارة السالبة من الطرفين:", "g · t = ?", "2v₀"),
        ("اقسم على g لاستخراج زمن التحليق — هذه هي العلاقة المستعملة:", "t = ?", "2v₀/g"),
    ],
    # ---------------------------------------------------------------- q6
    ("q6", 1): [
        ("القانون المدروس — تعريف الزخم الخطي (العلاقة 1-1):", "p = m · v"),
        ("طبّقه في اللحظة الابتدائية (بداية البيان):", "p₀ = m · ?", "v₀"),
        ("اقسم الطرفين على الكتلة m:", "p₀ / m = ?", "v₀"),
        ("إذن تُقرأ السرعة الابتدائية من البيان بقسمة الزخم الابتدائي على الكتلة:", "v₀ = ?", "p₀/m"),
    ],
    ("q6", 2): [
        ("القانون المدروس — نظرية الدفع والزخم (العلاقة 1-5):", "I = Δp = F · Δt"),
        ("تغيّر الزخم هو الفرق بين الزخم النهائي والزخم الابتدائي:", "Δp = p₂ - ?", "p₁"),
        ("إذن يُقرأ الدفع مباشرة من البيان كفرق بين قيمتي الزخم — العلاقة المستعملة:", "I = ?", "p₂-p₁"),
    ],
    ("q6", 3): [
        ("القانون المدروس — الدفع (العلاقة 1-2):", "I = F · Δt"),
        ("اقسم الطرفين على المدة الزمنية Δt:", "I / Δt = ?", "F"),
        ("إذن متوسط القوة — هذه هي العلاقة المستعملة:", "F = ?", "I/Δt|I/dt|I/t"),
    ],
    # ---------------------------------------------------------------- q7
    ("q7", 1): [
        ("القانون المدروس — تعريف الزخم الخطي:", "p = m · v"),
        ("زخم الجسم في اللحظة الابتدائية:", "p₁ = m · ?", "v₁"),
        ("وزخمه في اللحظة النهائية:", "p₂ = m · ?", "v₂"),
        ("ونظرية الدفع والزخم تعطي:", "I = Δp = p₂ - p₁"),
        ("عوّض بالزخمين:", "I = m · v₂ - m · ?", "v₁"),
        ("أخرج الكتلة عاملاً مشتركاً — هذه هي العلاقة المستعملة:", "I = m · ( ? )", "v₂-v₁"),
    ],
    ("q7", 2): [
        ("من الدرس: الدفع يساوي المساحة المحصورة تحت منحنى القوة – الزمن.", ""),
        ("الشكل البياني مثلث، ومساحته = ½ × القاعدة × الارتفاع؛ القاعدة هي المدة t والارتفاع هو القوة العظمى F:", "I = ½ · t · ?", "F"),
        ("اضرب الطرفين في 2:", "2 · I = t · ?", "F"),
        ("اقسم على المدة t — هذه هي العلاقة المستعملة:", "F = ?", "2I/t"),
    ],
    ("q7", 3): [
        ("القانون المدروس — الدفع بدلالة القوة المتوسطة:", "I = F · t"),
        ("اقسم الطرفين على المدة t لاستخراج متوسط القوة — العلاقة المستعملة:", "F = ?", "I/t"),
    ],
    # ---------------------------------------------------------------- q8
    ("q8", 1): [
        ("القانون المدروس — الطاقة الحركية:", "K = ½ · m · v²"),
        ("اضرب البسط والمقام في الكتلة m:", "K = ( m² · v² ) / ( 2 · ? )", "m"),
        ("وبما أن p = m · v فإن m² · v² = p²:", "K = p² / ( 2 · ? )", "m"),
        ("الجزءان لهما نفس مقدار الزخم p (انحفاظ الزخم)، والمعطى أن كتلة الأول ثلاثة أمثال الثاني:", "m₁ = ? · m₂", "3"),
        ("عوّض بكتلة الجسم الأول — هذه هي العبارة المستعملة:", "K₁ = p² / ( 2 · ? )", "3m₂"),
    ],
    ("q8", 2): [
        ("طبّق نفس القانون على الجزء الثاني:", "K₂ = p² / ( 2 · m₂ )"),
        ("اقسم K₂ على K₁ (ضرب في المقلوب) بعد اختصار p²:", "K₂ / K₁ = [ 2 · ( 3m₂ ) ] / ( 2 · ? )", "m₂"),
        ("اختصر العدد 2 والكتلة m₂ — هذه هي النسبة المطلوبة:", "K₂ / K₁ = ?", "3"),
    ],
    # ---------------------------------------------------------------- q9
    ("q9", 1): [
        ("القانون المدروس — انحفاظ الزخم الخطي (العلاقة 1-6):", "Σp = Σp'"),
        ("قبل الانفجار: جسم واحد كتلته m وسرعته v₀:", "Σp = m · ?", "v₀"),
        ("بعد الانفجار: جزء كتلته 0.25m بسرعة v₁ وجزء كتلته 0.75m بسرعة v₂:", "Σp' = 0.25 · m · v₁ + 0.75 · m · ?", "v₂"),
        ("طبّق مبدأ الانحفاظ (الزخم قبل = الزخم بعد):", "m · v₀ = 0.25 · m · v₁ + 0.75 · m · ?", "v₂"),
        ("اختصر الكتلة m من جميع الحدود:", "v₀ = 0.25 · v₁ + 0.75 · ?", "v₂"),
        ("انقل الحد 0.25 · v₁ إلى الطرف الآخر:", "0.75 · v₂ = v₀ - ?", "0.25v₁"),
        ("اقسم على 0.75 — هذه هي العلاقة المستعملة:", "v₂ = ?", "(v₀-0.25v₁)/0.75"),
    ],
    # ---------------------------------------------------------------- q10
    ("q10", 1): [
        ("📘 معادلة مدروسة في منهاج الصف 11 — الحركة الرأسية (الصاديّة)، المعادلة المستقلة عن الزمن، ونأخذ هنا المنحى الموجب نحو الأسفل فتصبح ‏a_y = + g:", "v²_yf = v²_yi + 2 · g · ( y_f - y_i )"),
        ("نطبّقها على حالة تمريننا: الرجل ينطلق من السكون، إذن السرعة الابتدائية:", "v_yi = ?", "0"),
        ("والإزاحة من نقطة القفز إلى سطح الماء هي الارتفاع h:", "y_f - y_i = ?", "h"),
        ("عوّض هذه القيم في المعادلة:", "v² = 0 + 2 · g · ?", "h"),
        ("رتّب — هذه هي العلاقة المستعملة في الحل:", "v² = ?", "2gh"),
    ],
    ("q10", 2): [
        ("القانون المدروس — دفع محصلة القوى (العلاقة 1-3):", "I = ΣF · Δt = Δp"),
        ("داخل الماء تؤثر قوة الماء F نحو الأعلى والوزن m·g نحو الأسفل، والاتجاه الموجب نحو الأعلى:", "ΣF = F - ?", "mg"),
        ("يتوقف الرجل داخل الماء، فتنعدم سرعته النهائية ويكون مقدار تغيّر زخمه:", "Δp = m · ?", "v"),
        ("عوّض في القانون:", "( F - m · g ) · Δt = m · ?", "v"),
        ("اقسم الطرفين على مدة التوقف Δt:", "F - m · g = ( m · v ) / ?", "Δt|dt|t"),
        ("استخرج قوة دفع الماء F — هذه هي العلاقة المستعملة:", "F = ( m · v / Δt ) + ?", "mg"),
    ],
    # ---------------------------------------------------------------- q11
    ("q11", 1): [
        ("القانون الأول المدروس — تعريف الزخم:", "p = m · v"),
        ("والقانون الثاني المدروس — الطاقة الحركية:", "K = ½ · m · v²"),
        ("اقسم الطاقة على الزخم:", "K / p = ( ½ · m · v² ) / ( m · ? )", "v"),
        ("اختصر الكتلة m وإحدى السرعتين:", "K / p = v / ?", "2"),
        ("اضرب في 2 لاستخراج السرعة — هذه هي العلاقة المستعملة:", "v = ?", "2K/p"),
    ],
    # ---------------------------------------------------------------- q12
    ("q12", 1): [
        ("القانون المدروس — انحفاظ الزخم الخطي (العلاقة 1-6):", "Σp = Σp'"),
        ("قبل التصادم الزلاجة ساكنة، فسرعتها:", "v₂ = ?", "0"),
        ("إذن الزخم الكلي قبل التصادم هو زخم المتزلج وحده:", "Σp = m₁ · ?", "v₁"),
        ("بعد التصادم يتحرك الجسمان معاً بسرعة مشتركة، فتُجمع الكتلتان:", "Σp' = ( m₁ + ? ) · v'", "m₂"),
        ("طبّق مبدأ الانحفاظ:", "m₁ · v₁ = ( m₁ + m₂ ) · ?", "v'"),
        ("اقسم على مجموع الكتلتين — هذه هي العلاقة المستعملة:", "v' = ?", "m₁v₁/(m₁+m₂)"),
    ],
    # ---------------------------------------------------------------- q13
    ("q13", 1): [
        ("القانون المدروس — نظرية الدفع والزخم:", "I = Δp = p₂ - p₁"),
        ("نعتبر اتجاه ذهاب الكرة نحو الحائط موجباً، فالزخم قبل الارتطام:", "p₁ = m · ?", "v"),
        ("ترتد الكرة بـ 75% من سرعتها في الاتجاه المعاكس، فالزخم بعد الارتطام:", "p₂ = - 0.75 · m · ?", "v"),
        ("عوّض الزخمين في النظرية:", "I = - 0.75 · m · v - ?", "mv"),
        ("اجمع الحدّين المتشابهين:", "I = ?", "-1.75mv"),
        ("المطلوب مقدار الدفع فنأخذ القيمة المطلقة — هذه هي العلاقة المستعملة:", "I = ?", "1.75mv"),
    ],
    ("q13", 2): [
        ("القانون المدروس — الدفع (العلاقة 1-2):", "I = F · Δt"),
        ("اقسم الطرفين على زمن التلامس Δt — هذه هي العلاقة المستعملة:", "F = ?", "I/Δt|I/dt|I/t"),
    ],
    # ---------------------------------------------------------------- q14
    ("q14", 1): [
        ("القانون المدروس — انحفاظ الزخم الخطي (العلاقة 1-6):", "Σp = Σp'"),
        ("الجسم ساكن قبل الانفجار، فزخمه الابتدائي:", "Σp = ?", "0"),
        ("وبعد الانفجار يبقى مجموع زخمي الجزأين مساوياً للزخم الابتدائي:", "p₁ + p₂ = ?", "0"),
        ("انقل الزخم الثاني إلى الطرف الآخر (الزخمان متعاكسان في الاتجاه):", "p₁ = - ?", "p₂"),
        ("بأخذ المقياس نجد أن للجزأين نفس مقدار الزخم — هذه هي العلاقة المستعملة:", "| p₁ | = | ? | = p", "p₂"),
    ],
    ("q14", 2): [
        ("القانون المدروس — الطاقة الحركية بدلالة الزخم:", "K = p² / ( 2 · m )"),
        ("طاقة الجزء الأول (مقدار زخمه p):", "K₁ = p² / ( 2 · ? )", "m₁"),
        ("وطاقة الجزء الثاني (نفس مقدار الزخم p):", "K₂ = p² / ( 2 · ? )", "m₂"),
        ("الطاقة الكلية المتحررة هي مجموع الطاقتين — هذه هي العلاقة المستعملة:", "K = p² / ( 2 · m₁ ) + p² / ( 2 · ? )", "m₂"),
    ],
    ("q14", 3): [
        ("انطلاقاً من عبارة الطاقة الكلية المستنتجة في الخطوة 2:", "K = p² / ( 2 · m₁ ) + p² / ( 2 · m₂ )"),
        ("وحّد المقامين في طرف واحد:", "K = p² · ( m₁ + m₂ ) / ( 2 · m₁ · ? )", "m₂"),
        ("استخرج p² من هذه العلاقة:", "p² = 2 · K · m₁ · m₂ / ( m₁ + ? )", "m₂"),
        ("عوّض p² داخل عبارة K₂ = p² / ( 2 · m₂ ) ثم اختصر m₂:", "K₂ = K · m₁ / ( m₁ + ? )", "m₂"),
        ("أعد ترتيب العبارة — هذه هي العلاقة المطلوب إثباتها:", "K₂ = [ m₁ / ( m₁ + ? ) ] · K", "m₂"),
    ],
    # ---------------------------------------------------------------- q15
    ("q15", 1): [
        ("القانون المدروس — انحفاظ الزخم الخطي (العلاقة 1-6):", "Σp = Σp'"),
        ("قبل الإطلاق يكون النظام (مدفع + قذيفة) ساكناً، فزخمه:", "Σp = ?", "0"),
        ("بعد الإطلاق: المدفع كتلته M وسرعة ارتداده V، والقذيفة كتلتها m وسرعتها v:", "M · V + m · ? = 0", "v"),
        ("الزخمان متعاكسان، وبأخذ المقياس نصل إلى العلاقة المستعملة:", "M · V = m · ?", "v"),
    ],
    ("q15", 2): [
        ("من الخطوة 1، مقدارا الزخمين متساويان:", "p = M · V = m · v"),
        ("والقانون المدروس للطاقة الحركية بدلالة الزخم:", "K = p² / ( 2 · m )"),
        ("طاقة المدفع بدلالة الزخم المشترك p:", "Kc = p² / ( 2 · ? )", "M"),
        ("وطاقة القذيفة بدلالة نفس الزخم:", "Kp = p² / ( 2 · ? )", "m"),
        ("اكتب النسبة بين الطاقتين — هذه هي العبارة المستعملة:", "Kc / Kp = ( p² / 2M ) / [ p² / ( 2 · ? ) ]", "m"),
    ],
    ("q15", 3): [
        ("انطلاقاً من النسبة المستنتجة في الخطوة 2:", "Kc / Kp = ( p² / 2M ) / ( p² / 2m )"),
        ("اقسم الكسرين (ضرب في المقلوب) واختصر p² والعدد 2:", "Kc / Kp = ( 2 · m ) / ( 2 · ? )", "M"),
        ("بسّط — هذه هي النسبة المطلوب إثباتها:", "Kc / Kp = ?", "m/M"),
    ],
}


FIGURES = {'pb9': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5MDAiIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgOTAwIDMwMCI+CjxkZWZzPjxtYXJrZXIgaWQ9ImEiIG1hcmtlcldpZHRoPSIxMCIgbWFya2VySGVpZ2h0PSIxMCIgcmVmWD0iOCIgcmVmWT0iMyIgb3JpZW50PSJhdXRvIj48cGF0aCBkPSJNMCwwIEwwLDYgTDksMyB6IiBmaWxsPSIjMGY0YzgxIi8+PC9tYXJrZXI+PC9kZWZzPgo8cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjMwMCIgcng9IjI0IiBmaWxsPSIjZjdmYmZmIiBzdHJva2U9IiNiOGQ3ZWQiIHN0cm9rZS13aWR0aD0iNCIvPgo8ZyBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZpbGw9IiMxNjMyNGEiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjx0ZXh0IHg9IjIyNSIgeT0iNDgiIGZvbnQtc2l6ZT0iMjYiIGZvbnQtd2VpZ2h0PSI3MDAiPtio2LnYryDYp9mE2KfYsdiq2K/Yp9ivPC90ZXh0Pjx0ZXh0IHg9IjY3NSIgeT0iNDgiIGZvbnQtc2l6ZT0iMjYiIGZvbnQtd2VpZ2h0PSI3MDAiPtmC2KjZhCDYp9mE2KfYtdi32K/Yp9mFPC90ZXh0PjwvZz4KPGcgc3Ryb2tlPSIjMzc0MTUxIiBzdHJva2Utd2lkdGg9IjYiIGZpbGw9IiNkYmVhZmUiPjxwYXRoIGQ9Ik0xMTAgMTg1aDIyMGwtMTgtNjVoLTEyMGwtNDIgNjV6Ii8+PGNpcmNsZSBjeD0iMTY1IiBjeT0iMjA3IiByPSIyOSIgZmlsbD0iIzMzNDE1NSIvPjxjaXJjbGUgY3g9IjI4NSIgY3k9IjIwNyIgcj0iMjkiIGZpbGw9IiMzMzQxNTUiLz48cGF0aCBkPSJNNTcwIDE4NWgyMjBsLTE4LTY1aC0xMjBsLTQyIDY1eiIvPjxjaXJjbGUgY3g9IjYyNSIgY3k9IjIwNyIgcj0iMjkiIGZpbGw9IiMzMzQxNTUiLz48Y2lyY2xlIGN4PSI3NDUiIGN5PSIyMDciIHI9IjI5IiBmaWxsPSIjMzM0MTU1Ii8+PC9nPgo8cGF0aCBkPSJNMTI1IDg1aDIwNSIgc3Ryb2tlPSIjMGY0YzgxIiBzdHJva2Utd2lkdGg9IjgiIG1hcmtlci1lbmQ9InVybCgjYSkiLz48dGV4dCB4PSIyMjUiIHk9Ijc4IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMzAiIGZvbnQtd2VpZ2h0PSI3MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMwZjRjODEiPnZfZiA9ICsyLjYgbS9zPC90ZXh0Pgo8cGF0aCBkPSJNNzgwIDg1SDU3NSIgc3Ryb2tlPSIjMGY0YzgxIiBzdHJva2Utd2lkdGg9IjgiIG1hcmtlci1lbmQ9InVybCgjYSkiLz48dGV4dCB4PSI2NzUiIHk9Ijc4IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMzAiIGZvbnQtd2VpZ2h0PSI3MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMwZjRjODEiPnZfaSA9IOKIkjQuNSBtL3M8L3RleHQ+Cjwvc3ZnPg==',
 'pb10': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5MDAiIGhlaWdodD0iNDQwIiB2aWV3Qm94PSIwIDAgOTAwIDQ0MCI+CjxkZWZzPjxtYXJrZXIgaWQ9ImFycm93IiBtYXJrZXJXaWR0aD0iMTAiIG1hcmtlckhlaWdodD0iMTAiIHJlZlg9IjgiIHJlZlk9IjMiIG9yaWVudD0iYXV0byI+PHBhdGggZD0iTTAsMCBMMCw2IEw5LDMgeiIgZmlsbD0iIzFlM2E1ZiIvPjwvbWFya2VyPjwvZGVmcz4KPHJlY3Qgd2lkdGg9IjkwMCIgaGVpZ2h0PSI0NDAiIHJ4PSIyNCIgZmlsbD0iI2ZiZmRmZiIgc3Ryb2tlPSIjYjhkN2VkIiBzdHJva2Utd2lkdGg9IjQiLz4KPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTEwLDQwKSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIj4KPGxpbmUgeDE9IjAiIHkxPSIxODAiIHgyPSI2OTAiIHkyPSIxODAiIHN0cm9rZT0iIzFlM2E1ZiIgc3Ryb2tlLXdpZHRoPSI1IiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93KSIvPjxsaW5lIHgxPSIwIiB5MT0iMzUwIiB4Mj0iMCIgeTI9IjEwIiBzdHJva2U9IiMxZTNhNWYiIHN0cm9rZS13aWR0aD0iNSIgbWFya2VyLWVuZD0idXJsKCNhcnJvdykiLz4KPGxpbmUgeDE9IjAiIHkxPSI2MCIgeDI9IjMwMCIgeTI9IjMwMCIgc3Ryb2tlPSIjMGY2ZWE5IiBzdHJva2Utd2lkdGg9IjgiLz48bGluZSB4MT0iMzAwIiB5MT0iMzAwIiB4Mj0iNjAwIiB5Mj0iMzAwIiBzdHJva2U9IiMwZjZlYTkiIHN0cm9rZS13aWR0aD0iOCIvPgo8bGluZSB4MT0iMzAwIiB5MT0iMTgwIiB4Mj0iMzAwIiB5Mj0iMzAwIiBzdHJva2U9IiM5NGEzYjgiIHN0cm9rZS1kYXNoYXJyYXk9IjEwIDEwIiBzdHJva2Utd2lkdGg9IjMiLz48bGluZSB4MT0iMCIgeTE9IjMwMCIgeDI9IjYwMCIgeTI9IjMwMCIgc3Ryb2tlPSIjOTRhM2I4IiBzdHJva2UtZGFzaGFycmF5PSIxMCAxMCIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxnIGZpbGw9IiMxZTI5M2IiIGZvbnQtc2l6ZT0iMjgiIGZvbnQtd2VpZ2h0PSI3MDAiPjx0ZXh0IHg9Ii00OCIgeT0iNzAiPjEwPC90ZXh0Pjx0ZXh0IHg9Ii02MiIgeT0iMzEwIj7iiJIxMDwvdGV4dD48dGV4dCB4PSIxNDUiIHk9IjIxNiI+MjwvdGV4dD48dGV4dCB4PSIyOTAiIHk9IjIxNiI+NDwvdGV4dD48dGV4dCB4PSI1OTAiIHk9IjIxNiI+NjwvdGV4dD48dGV4dCB4PSI2MjAiIHk9IjIyMCI+dCAocyk8L3RleHQ+PHRleHQgeD0iLTg1IiB5PSIzMCI+RiAoTik8L3RleHQ+PC9nPgo8L2c+PC9zdmc+'}

FIGURE_CAPTIONS = {'pb9': 'اتجاه السرعة قبل الاصطدام وبعد الارتداد', 'pb10': 'منحنى القوة–الزمن للسؤال العاشر'}


def figure_html(qid):
    """الرسم البياني المرافق لنص التمرين إن وجد"""
    src = FIGURES.get(qid)
    if not src:
        return ""
    cap = FIGURE_CAPTIONS.get(qid, "")
    return (
        '<div class="fig-box"><img src="' + src + '" alt="' + cap + '">'
        + ('<div class="fig-cap">' + cap + "</div>" if cap else "")
        + "</div>"
    )


def _pkh(t):
    """بصمة قصيرة ثابتة للإجابة تدخل في مفتاح الحفظ"""
    h = 0
    for ch in str(t):
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return format(h, "x")


DERIVE_TITLES = {
    ("q1", 1): "🧭 معادلة مدروسة في الصف 11 — طبّقها على حالة تمريننا",
    ("q4", 1): "🧭 معادلة مدروسة في الصف 11 — طبّقها على حالة تمريننا",
    ("q10", 1): "🧭 معادلة مدروسة في الصف 11 — طبّقها على حالة تمريننا",
}


def derive_html(qid, step):
    """سلسلة استنتاج تفاعلية: ينطلق الطالب من قانون الدرس ويكمل بنفسه كل سطر حتى العلاقة المستعملة."""
    items = DERIVE_STEPS.get((qid, step.get("num"))) or []
    if not items:
        return ""
    cs = "1" if step.get("case_sensitive") else "0"
    rows, last = [], len(items) - 1
    for i, it in enumerate(items):
        say = it[0] if len(it) > 0 else ""
        eq = it[1] if len(it) > 1 else ""
        ans = it[2] if len(it) > 2 else None
        cls = "micro-line derive-line"
        if ans is None:
            cls += " derive-ref"
        if i == last:
            cls += " derive-final"
        attrs = ' class="' + cls + '"'
        if ans is not None:
            attrs += ' data-pk="' + str(qid) + ':' + str(step.get('num')) + ':d:' + str(i + 1) + ':' + _pkh(ans) + '"'
            attrs += ' data-ans="' + str(ans).replace('"', "&quot;") + '" data-tries="0" data-cs="' + cs + '"'
        row = (
            "<div" + attrs
            + '><span class="micro-say derive-say"><span class="micro-num derive-num">'
            + str(i + 1) + "</span>" + say + "</span>"
        )
        if eq:
            row += '<span class="micro-eq derive-eq">' + plain_to_eq(eq) + "</span>"
        rows.append(row + "</div>")
    return (
        '<div class="derive-box">'
        + '<div class="derive-title">' + DERIVE_TITLES.get((qid, step.get("num")), "🧭 استنتج العلاقة بنفسك — من قانون الدرس إلى علاقة الحل") + '</div>'
        + '<div class="micro-box derive-steps" data-mk="d">' + "".join(rows) + "</div>"
        + '<div class="derive-tip">✍️ أكمل الفراغ في كل سطر ثم اضغط Enter — الأسطر الرمادية معادلات مدروسة سابقاً، وبعد 3 محاولات يظهر الجواب.</div>'
        + "</div>"
    )

def micro_html(step, final_mode="preview", field="micro", start=0, final_say=None, qid="", reveal=False):
    """صندوق الخطوات المبسّطة: يعوّض الطالب في كل خطوة حتى يصل للعبارة الكاملة"""
    micro = step.get(field) or []
    cs = "1" if step.get("case_sensitive") else "0"
    rows = []
    n = start
    for item in micro:
        say = item[0] if len(item) > 0 else ""
        eq = item[1] if len(item) > 1 else ""
        ans = item[2] if len(item) > 2 else None
        if ans is None and eq and "=" in str(eq) and "?" not in str(eq):
            _lhs, _rhs = str(eq).rsplit("=", 1)
            if _rhs.strip():
                eq, ans = _lhs + "= ?", _rhs.strip()
        if reveal and ans is not None:
            eq = str(eq).replace("?", str(ans).split("|")[0])
            ans = None
        n += 1
        attrs = ' class="micro-line"'
        if ans is not None:
            attrs += ' data-pk="' + str(qid) + ':' + str(step.get('num')) + ':' + str(field) + ':' + str(n) + ':' + _pkh(ans) + '"'
            attrs += ' data-ans="' + str(ans).replace('"', "&quot;") + '" data-tries="0" data-cs="' + cs + '"'
        eq_part = '<span class="micro-eq">' + plain_to_eq(eq) + "</span>" if eq else ""
        rows.append(
            "<div" + attrs + '><span class="micro-say"><span class="micro-num">'
            + str(n) + "</span>" + say + "</span>" + eq_part + "</div>"
        )
    if final_mode == "preview":
        n += 1
        _fsay = str(final_say).strip().rstrip(":").strip() if final_say else "أكمل هذه العبارة الأخيرة ثم اضغط زر «تحقق 🎯»"
        rows.append(
            '<div class="micro-line micro-final"><span class="micro-say"><span class="micro-num">'
            + str(n) + "</span>" + _fsay + "</span>"
            + '<div class="eq-box">' + eq_html(step.get("latex_preview", "") if reveal else _mask_ans(step.get("latex_preview", ""))) + "</div></div>"
        )
    return '<div class="micro-box" data-mk="' + str(field) + '">' + "".join(rows) + "</div>"


def law_no_given(law_text):
    """يحذف مقاطع «المعطى» من صندوق القانون لأن الخطوات المبسّطة تذكرها"""
    if not law_text:
        return ""
    keep = []
    for part in law_text.split("،"):
        part = part.strip()
        if not part:
            continue
        head = part.split(":", 1)[0].strip()
        if head.startswith("المعطى") or head.startswith("المعطيات"):
            continue
        keep.append(part)
    return "  ،  ".join(keep)


def eq_frag(txt):
    """يعرض شذرة معادلة (بادئة/لاحقة/جذر) بنفس طريقة عرض المعادلات،
    دون حذف أي قوس أو علامة قسمة لأن الطالب يكتب داخلها."""
    t = (txt or "").strip()
    if not t:
        return ""

    # رقم ملتصق برمز ينزل أسفل اليمين: v1 -> v₁
    subs_chars = "₀₁₂₃₄₅₆₇₈₉"
    buf = []
    for i, ch in enumerate(t):
        prev = t[i - 1] if i else ""
        nxt = t[i + 1] if i + 1 < len(t) else ""
        is_sym = ("a" <= prev <= "z") or ("A" <= prev <= "Z") or prev == "Δ"
        is_d = "0" <= ch <= "9"
        nxt_d = "0" <= nxt <= "9"
        if is_d and is_sym and not (nxt_d or nxt in ".,"):
            buf.append(subs_chars[int(ch)])
        else:
            buf.append(ch)
    t = "".join(buf)

    SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
           "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"}
    SUB = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
           "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9"}
    OPS = {"*": "&middot;", "·": "&middot;", "-": "&minus;", "−": "&minus;",
           "×": "&times;", "+": "+"}

    out = []
    for ch in t:
        if ch in SUP:
            out.append("<sup>" + SUP[ch] + "</sup>")
        elif ch in SUB:
            out.append("<sub>" + SUB[ch] + "</sub>")
        elif ch in OPS:
            out.append('<span class="eq-op">' + OPS[ch] + "</span>")
        elif ch == "=":
            out.append('<span class="eq-eq">=</span>')
        elif ch == "√":
            out.append('<span class="eq-rad">√</span>')
        elif ch in "()[]{}":
            out.append('<span class="eq-par">' + ch + "</span>")
        elif ch == "/":
            out.append('<span class="eq-sl">/</span>')
        elif ch == "&":
            out.append("&amp;")
        elif ch == "<":
            out.append("&lt;")
        elif ch == ">":
            out.append("&gt;")
        else:
            out.append(ch)
    return '<span class="eq">' + "".join(out) + "</span>"


def law_html(law_text: str) -> str:
    """عنوان القانون/المعطى في سطر، والعلاقة في سطر واحد كامل تحته."""
    if not law_text:
        return '<div class="law-guide-box">📘</div>'

    segments = [p.strip() for p in str(law_text).replace("،", "\n").split("\n") if p.strip()]
    lines, first = [], True
    for seg in segments:
        ico = "📘 " if first else ""
        if ":" in seg:
            label, _, rest = seg.partition(":")
            label, rest = label.strip(), rest.strip()
            block = '<div class="law-line">'
            block += '<span class="law-label">' + ico + label + ":</span>"
            if rest:
                block += mixed_math_html(rest)
            block += "</div>"
        else:
            block = '<div class="law-line">'
            if ico:
                block += '<span class="law-label">📘</span>'
            block += mixed_math_html(seg) + "</div>"
        lines.append(block)
        first = False

    return '<div class="law-guide-box">' + "".join(lines) + "</div>"


def result_html(result_text, label: str = "✅ النتيجة", pre_html: bool = False) -> str:
    """يعرض نتيجة الخطوة في إطار مستقل بنفس أسلوب صندوق القانون/المعطى."""
    if result_text is None:
        return ""
    raw = str(result_text).strip()
    if not raw:
        return ""

    # الفاصل المستعمل بين نتيجتين هو "  |  " فقط، حتى لا تتأثر رموز القيمة المطلقة مثل |p₁|
    parts = [p.strip() for p in raw.split("  |  ") if p.strip()]
    if pre_html:
        # المحتوى مبنيّ مسبقاً بـ eq_frag: يُعرض كما هو دون إعادة معالجة
        body = "".join('<span class="result-eq">' + p + "</span>" for p in parts)
    else:
        body = "".join(
            mixed_math_html(p, eq_cls="result-eq", note_cls="result-note") for p in parts
        )
    return (
        '<div class="result-box"><span class="result-label">'
        + label + ":</span>" + body + "</div>"
    )


SYMBOL_LIBRARY = [
    "Δ", "ΔP", "Δt", "θ", "π", "×", "÷", "√", "²",
    "³", "≈", "±", "→", "←", "°", "m/s", "m/s²", "kg",
    "N", "N·s", "kg·m/s", "J", "−", "⁄", "⬜", "⌫", "مسح",
]


def _mask_ans(txt):
    """يخفي طرف المعادلة الأيمن (الإجابة) حتى لا تُعرض قبل أن يكتبها الطالب."""
    t = str(txt or "")
    if not t or "?" in t or "=" not in t:
        return t
    head, _tail = t.rsplit("=", 1)
    if not _tail.strip():
        return t
    return head + "= ?"


def _hint_micro_lines(step, field="micro", keep_last_blank=True):
    """يشرح خطوات الحل ويكشف معادلاتها ما عدا الفراغ الأخير."""
    rows = step.get(field) or []
    out = []
    for i, item in enumerate(rows):
        say = item[0] if len(item) > 0 else ""
        eq = item[1] if len(item) > 1 else ""
        ans = item[2] if len(item) > 2 else None
        if ans is not None and "?" in str(eq):
            eq = str(eq).replace("?", str(ans).split("|")[0])
        if keep_last_blank and i == len(rows) - 1:
            eq = _mask_ans(eq)
        out.append("<li><b>" + str(i + 1) + ".</b> " + str(say) + ((" <code>" + str(eq) + "</code>") if eq else "") + "</li>")
    return "".join(out)


def rich_hint(step, level=1):
    """تلميح موسّع: شرح + جزء من الحل يتزايد مع المستوى."""
    parts = []
    if step.get("law"):
        parts.append("<div><b>القانون المستعمل:</b> " + str(step["law"]) + "</div>")
    if step.get("simple_explain"):
        parts.append("<div>💬 " + str(step["simple_explain"]) + "</div>")
    micro_html_lines = _hint_micro_lines(step, "micro", keep_last_blank=(level < 3))
    if micro_html_lines:
        parts.append("<div><b>خطوات الحل مفصّلة:</b><ol class=\"hint-steps\">" + micro_html_lines + "</ol></div>")
    if level >= 2:
        lines2 = _hint_micro_lines(step, "micro2", keep_last_blank=(level < 3))
        if lines2:
            parts.append("<div><b>تابع:</b><ol class=\"hint-steps\">" + lines2 + "</ol></div>")
        if step.get("blanks"):
            sub = str(step.get("prefix", ""))
            for b in step["blanks"]:
                sub += "(" + str(b["target"]) + ")" + str(b.get("suffix", ""))
            parts.append("<div><b>هكذا يكون التعويض:</b> <code>" + sub + "</code></div>")
            if step.get("has_root"):
                parts.append("<div><b>تحت الجذر:</b> <code>" + str(step.get("root_prefix", "")) + " " + str(step.get("root_target", "")) + " " + str(step.get("root_suffix", "")) + "</code></div>")
            parts.append("<div>احسب بالترتيب: ما داخل الأقواس أولاً، ثم الضرب والقسمة، واكتب الناتج في خانة "
                         + str(step.get("result_label", "النتيجة")).strip().rstrip(":") + ".</div>")
    if step.get("hint"):
        parts.append("<div><b>مفتاح الفكرة:</b> " + str(step["hint"]) + "</div>")
    if level < 3:
        parts.append("<div><small>اضغط 💡 مرة أخرى لشرح أوسع، أو اضغط «✅ الإجابة الصحيحة» لإدخالها تلقائياً في الفراغات.</small></div>")
    return "".join(parts)


def calc_points(attempts_count, hint_lvl):
    hint_deduction = {0: 0, 1: 1, 2: 3, 3: 5}.get(hint_lvl, 5)
    attempts_deduction = max(0, attempts_count - 1)
    return max(1, 10 - hint_deduction - attempts_deduction)

def get_level(xp):
    if xp < 20:
        return "🌱 مبتدئ", "#94a3b8", 20
    elif xp < 60:
        return "📘 متدرب", "#2563eb", 60
    elif xp < 120:
        return "🚀 متمكن", "#7c3aed", 120
    else:
        return "🏆 خبير الفيزياء", "#f59e0b", max(xp + 20, 150)

def fmt_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"

def reset_question(qid, qtype):
    st.session_state["physbook_completed_questions"].discard(qid)
    st.session_state["physbook_start_time"][qid] = time.time()
    st.session_state["physbook_time_spent"].pop(qid, None)
    st.session_state[f"step_prog_{qid}"] = 1
    st.session_state["physbook_no_hint_flag"][qid] = True
    keys_to_clear = [k for k in st.session_state["physbook_attempts"] if k.startswith(f"{qid}_")]
    for k in keys_to_clear:
        st.session_state["physbook_attempts"].pop(k, None)
        st.session_state["physbook_hint_level"].pop(k, None)

def reset_everything():
    keep_name = st.session_state.get("physbook_student_name", "")
    for key in list(st.session_state.keys()):
        if key.startswith("physbook_"):
            del st.session_state[key]
    init_state()
    st.session_state["physbook_student_name"] = keep_name

# ==========================================================
# 5. زر الملف الشخصي (نافذة منبثقة) في أعلى يمين الصفحة
# ==========================================================
with st.container(key="avatar_row"):
    _pc_avatar = st.columns([1, 11])[0]
with _pc_avatar:
    level_label, level_color, next_threshold = get_level(st.session_state["physbook_total_xp"])
    xp = st.session_state["physbook_total_xp"]
    progress_pct = min(100, int((xp / next_threshold) * 100)) if next_threshold else 100
    name_display = st.session_state["physbook_student_name"] or "طالب مجتهد"
    avatar_letter = name_display.strip()[0] if name_display.strip() else "🧑‍🎓"
    done_count = len(st.session_state["physbook_completed_questions"])
    overall_pct = int((done_count / TOTAL_QUESTIONS) * 100)

    # --- أيقونة الطالب: الملف والأوسمة داخل نافذة منبثقة ---
    with st.container(key="profile_pop"):
        _pop = (
            st.popover(avatar_letter, use_container_width=False)
            if hasattr(st, "popover")
            else st.expander("👤 " + name_display)
        )
        with _pop:
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-avatar">{avatar_letter}</div>
                <div style="font-weight:800; font-size:1.05rem; color:#0f172a;">{name_display}</div>
                <span class="level-badge-pill" style="background:{level_color}22; color:{level_color};">{level_label}</span>
                <div style="margin-top:10px; text-align:right;">
                    <small style="color:#64748b;">نقاط الخبرة</small>
                    <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{progress_pct}%;"></div></div>
                    <small style="color:#64748b;">{xp} XP</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.session_state["physbook_student_name"] = st.text_input(
                "✏️ اسم الطالب/ـة", value=st.session_state["physbook_student_name"],
                placeholder="اكتب اسمك هنا..."
            )

            st.markdown(f"""
            <div class="sidebar-card">
                <b>📊 التقدم العام</b>
                <div class="qprogress-bg"><div class="qprogress-fill" style="width:{overall_pct}%;"></div></div>
                <div style="display:flex; justify-content:space-between;">
                    <small style="color:#64748b;">التمارين المكتملة</small>
                    <b style="color:#16a34a;">{done_count} / {TOTAL_QUESTIONS}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="sidebar-card"><b>🏅 الأوسمة المكتسبة</b>', unsafe_allow_html=True)
            if st.session_state["physbook_badges"]:
                tiles = ""
                for b in sorted(st.session_state["physbook_badges"]):
                    parts = b.split(" ", 1)
                    icon = parts[0]
                    txt = parts[1] if len(parts) > 1 else ""
                    tiles += f'<div class="badge-tile"><span class="b-icon">{icon}</span>{txt}</div>'
                st.markdown(f'<div class="badges-grid">{tiles}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="badge-empty">لم تحصل على أوسمة بعد، ابدأ الحل! 💪</div></div>', unsafe_allow_html=True)

            if st.button("🔄 إعادة تعيين كل التقدم", use_container_width=True):
                reset_everything()
                st.rerun()


# ==========================================================
# 6. الرأس والنصيحة اليومية
# ==========================================================
render_exercise_header_v18(
    subject="الفيزياء", track="تمارين الكتاب", unit_title="حلول تمارين الكتاب · الزخم الخطي والدفع",
    current_page="pages/physics_textbook_exercises.py", tip=st.session_state["physbook_daily_tip"], subject_icon="⚛️",
)

# ==========================================================
# 6.5 الصفحة الرئيسية للمنصة + التوجيه بين الواجهة والتمارين
# ==========================================================
HOME_GRADES = [(6, "السادس"), (7, "السابع"), (8, "الثامن"), (9, "التاسع"),
               (10, "العاشر"), (11, "الحادي عشر"), (12, "الثاني عشر")]

HOME_SUBJECTS = {"phys": ("الفيزياء", "⚛️"), "chem": ("الكيمياء", "🧪")}

HOME_UNITS = {
    "phys": {
        6:  ["القياس والوحدات", "الحركة والسرعة", "القوى من حولنا",
              "الشغل والطاقة", "الضوء والرؤية", "الصوت"],
        7:  ["المادة وحالاتها", "الحرارة ودرجة الحرارة", "الآلات البسيطة",
              "الكهرباء الساكنة", "المغناطيسية"],
        8:  ["الحركة المنتظمة", "القوة والاحتكاك", "الضغط والكثافة",
              "الطاقة وتحولاتها", "الدارات الكهربائية"],
        9:  ["الحركة بتسارع ثابت", "قوانين نيوتن", "الشغل والقدرة",
              "الموجات", "التيار الكهربائي"],
        10: ["المتجهات", "الحركة في بعدين", "قوانين نيوتن وتطبيقاتها",
              "الشغل والطاقة والقدرة", "مقدمة في الزخم"],
        11: ["الحركة الرأسية والمقذوفات", "الحركة الدائرية", "الجاذبية الكونية",
              "الموائع", "الاهتزاز والموجات"],
        12: ["الزخم الخطي والدفع", "الكهرباء الساكنة", "التيار والدارات",
              "المجال المغناطيسي", "الحث الكهرومغناطيسي", "مقدمة الفيزياء الحديثة"],
    },
    "chem": {
        6:  ["المادة وخواصها", "المخاليط والمحاليل",
              "التغيرات الفيزيائية والكيميائية", "الماء ودورته"],
        7:  ["بناء الذرة", "العناصر والمركبات", "مقدمة الجدول الدوري",
              "الأحماض والقواعد حولنا"],
        8:  ["التركيب الذري والإلكترونات", "الروابط الكيميائية",
              "التفاعلات الكيميائية", "المحاليل والذائبية"],
        9:  ["المعادلات الكيميائية ووزنها", "الأحماض والقواعد والأملاح",
              "الأكسدة والاختزال", "مقدمة الكيمياء العضوية"],
        10: ["المول والحسابات الكيميائية", "الجدول الدوري والدورية",
              "أنواع الروابط", "الغازات وقوانينها"],
        11: ["الاتزان الكيميائي", "سرعة التفاعل",
              "الأحماض والقواعد وحساب pH", "الكهروكيمياء"],
        12: ["الكيمياء الحرارية", "الكيمياء العضوية", "البوليمرات", "التحليل الكيميائي"],
    },
}

# الوحدة المبنية فعليًا الآن: (المادة، الصف، رقم الوحدة)
HOME_LIVE = ("phys", 12, 0)

for _k, _v in (("physbook_samed_view", "home"), ("physbook_samed_grade", 12), ("physbook_samed_subject", None)):
    if _k not in st.session_state:
        st.session_state[_k] = _v

PHYSBOOK_STARTUP_VERSION = "physics-book-direct-v1"
if st.session_state.get("physbook_startup_version") != PHYSBOOK_STARTUP_VERSION:
    st.session_state["physbook_samed_view"] = "app"
    st.session_state["physbook_startup_version"] = PHYSBOOK_STARTUP_VERSION

st.markdown("""
<style>
  .home-hero{ background:linear-gradient(135deg,#ecfdf5 0%,#f0fdfa 60%,#ffffff 100%);
     border:1px solid #a7f3d0; border-radius:20px; padding:22px 24px; height:100%;
     border-right:5px solid #10b981; }
  .home-hero h2{ margin:0 0 10px; font-size:25px; font-weight:800; color:#064e3b; line-height:1.45; }
  .home-hero p{ margin:0; font-size:14.5px; color:#065f46; line-height:1.9; }
  .home-resume{ background:#ffffff; border:1px solid #e2e8f0; border-radius:20px;
     padding:18px 20px; box-shadow:0 6px 18px rgba(15,45,80,.07); }
  .home-resume h4{ margin:0 0 4px; font-size:13px; color:#64748b; font-weight:700; }
  .home-resume b{ display:block; font-size:18px; color:#0f172a; font-weight:800; }
  .home-resume small{ color:#64748b; font-size:12.5px; }
  .home-bar{ height:10px; border-radius:99px; background:#eef2f7; overflow:hidden;
     border:1px solid #e2e8f0; margin:10px 0 6px; }
  .home-bar i{ display:block; height:100%; border-radius:99px;
     background:linear-gradient(90deg,#10b981,#6ee7b7); }
  .home-h2{ margin:22px 0 6px; font-size:19px; font-weight:800; color:#0f172a; }
  .home-h2 span{ font-size:12.5px; font-weight:600; color:#94a3b8; }
  .home-stats{ display:flex; gap:10px; flex-wrap:wrap; margin-top:6px; }
  .home-stat{ flex:1; min-width:120px; background:#fff; border:1px solid #e2e8f0;
     border-radius:14px; padding:11px 14px; text-align:center; }
  .home-stat b{ display:block; font-size:21px; font-weight:800; color:#0f766e; }
  .home-stat small{ font-size:11.5px; color:#64748b; font-weight:700; }
  .home-card{ background:#fff; border:1px solid #e2e8f0; border-radius:18px;
     padding:16px 18px 12px; margin-bottom:6px; }
  .home-card .ic{ font-size:30px; }
  .home-card .nm{ font-size:20px; font-weight:800; color:#0f172a; }
  .home-card .mt{ font-size:12.5px; color:#64748b; font-weight:700; }
  .home-bd{ background:#fff; border:1px solid #e2e8f0; border-radius:15px;
     padding:13px 10px; text-align:center; height:100%; }
  .home-bd.got{ border-color:#fcd34d; background:linear-gradient(180deg,#fffbeb,#fff); }
  .home-bd .bi{ font-size:26px; display:block; filter:grayscale(1) opacity(.38); }
  .home-bd.got .bi{ filter:none; }
  .home-bd b{ display:block; font-size:13px; font-weight:800; color:#0f172a; margin-top:5px; }
  .home-bd small{ font-size:10.5px; color:#94a3b8; line-height:1.5; display:block; }
  .home-note{ margin-top:20px; background:#fffbeb; border:1px solid #fde68a;
     border-right:5px solid #f59e0b; border-radius:14px; padding:14px 18px;
     font-size:13.5px; color:#78350f; line-height:1.9; }
</style>
""", unsafe_allow_html=True)


if st.session_state["physbook_samed_view"] == "home":

    _xp   = int(st.session_state.get("physbook_total_xp", 0) or 0)
    _done = len(st.session_state.get("physbook_completed_questions", set()) or set())
    _bdg  = len(st.session_state.get("physbook_badges", set()) or set())
    _strk = int(st.session_state.get("physbook_streak", 0) or 0)
    _pct  = int(round(_done * 100.0 / TOTAL_QUESTIONS)) if TOTAL_QUESTIONS else 0

    _hc1, _hc2 = st.columns([1.35, 1])
    with _hc1:
        st.markdown(
            "<div class='home-hero'><h2>لا تتوقّف عند أول خطأ.</h2>"
            "<p>فيزياء وكيمياء من الصف السادس إلى الثاني عشر. كل تمرين يُحلّ معك خطوة بخطوة: "
            "تكتب أنت القيمة في الفراغ، وتستنتج القانون بنفسك، ولا تُعرض عليك الإجابة "
            "إلا بعد ثلاث محاولات.</p></div>",
            unsafe_allow_html=True)
    with _hc2:
        st.markdown(
            "<div class='home-resume'><h4>تابِع من حيث توقّفت</h4>"
            "<b>⚛️ الزخم الخطي والدفع</b>"
            "<small>الفيزياء · الصف الثاني عشر</small>"
            "<div class='home-bar'><i style='width:" + str(_pct) + "%'></i></div>"
            "<small>أنجزتَ " + str(_done) + " من " + str(TOTAL_QUESTIONS) +
            " تمرينًا (" + str(_pct) + "%)</small></div>",
            unsafe_allow_html=True)
        if st.button("▶️ ابدأ / تابِع الحل", key="samed_go",
                     use_container_width=True, type="primary"):
            st.session_state["physbook_samed_view"] = "app"
            st.rerun()

    st.markdown(
        "<div class='home-stats'>"
        "<div class='home-stat'><b>" + str(_xp) + "</b><small>نقطة</small></div>"
        "<div class='home-stat'><b>" + str(_done) + "</b><small>تمرين مُنجَز</small></div>"
        "<div class='home-stat'><b>" + str(_bdg) + "</b><small>وسام</small></div>"
        "<div class='home-stat'><b>" + str(_strk) + "</b><small>يوم متتالٍ</small></div>"
        "</div>", unsafe_allow_html=True)

    # ---------- اختيار الصف ----------
    st.markdown("<p class='home-h2'>اختر صفّك <span>— المحتوى يتغيّر تلقائيًا</span></p>",
                unsafe_allow_html=True)
    _gc = st.columns(7)
    for _i, (_gn, _gl) in enumerate(HOME_GRADES):
        with _gc[_i]:
            _on = (st.session_state["physbook_samed_grade"] == _gn)
            if st.button(str(_gn) + " · " + _gl, key="samed_g_" + str(_gn),
                         use_container_width=True,
                         type=("primary" if _on else "secondary")):
                st.session_state["physbook_samed_grade"] = _gn
                st.rerun()

    # ---------- المواد ----------
    _grade = st.session_state["physbook_samed_grade"]
    st.markdown("<p class='home-h2'>المواد <span>— اضغط المادة لعرض وحداتها</span></p>",
                unsafe_allow_html=True)
    _sc = st.columns(2)
    for _i, _sk2 in enumerate(["phys", "chem"]):
        _nm, _ic = HOME_SUBJECTS[_sk2]
        _units = HOME_UNITS[_sk2].get(_grade, [])
        _live_here = (HOME_LIVE[0] == _sk2 and HOME_LIVE[1] == _grade)
        _meta = (str(TOTAL_QUESTIONS) + " تمرينًا تفاعليًا جاهزًا") if _live_here else "قيد الإعداد"
        with _sc[_i]:
            st.markdown(
                "<div class='home-card'><span class='ic'>" + _ic + "</span> "
                "<span class='nm'>" + _nm + "</span><br>"
                "<span class='mt'>" + str(len(_units)) + " وحدات · " + _meta + "</span></div>",
                unsafe_allow_html=True)
            _open = (st.session_state["physbook_samed_subject"] == _sk2)
            if st.button(("▼ إخفاء الوحدات" if _open else "عرض الوحدات ←"),
                         key="samed_s_" + _sk2, use_container_width=True,
                         type=("primary" if _open else "secondary")):
                st.session_state["physbook_samed_subject"] = (None if _open else _sk2)
                st.rerun()

    # ---------- الوحدات ----------
    _subj = st.session_state["physbook_samed_subject"]
    if _subj:
        _nm, _ic = HOME_SUBJECTS[_subj]
        _lab = dict(HOME_GRADES)[_grade]
        _units = HOME_UNITS[_subj].get(_grade, [])
        st.markdown("<p class='home-h2'>" + _ic + " وحدات " + _nm +
                    " — الصف " + _lab + "</p>", unsafe_allow_html=True)
        for _i, _t in enumerate(_units):
            _is_live = (HOME_LIVE == (_subj, _grade, _i))
            if _is_live:
                if st.button("✅ " + str(_i + 1) + ". " + _t + "  —  متاح الآن ("
                             + str(TOTAL_QUESTIONS) + " تمرينًا)",
                             key="samed_u_" + _subj + "_" + str(_grade) + "_" + str(_i),
                             use_container_width=True, type="primary"):
                    st.session_state["physbook_samed_view"] = "app"
                    st.rerun()
            else:
                st.button("🔒 " + str(_i + 1) + ". " + _t + "  —  قريبًا",
                          key="samed_u_" + _subj + "_" + str(_grade) + "_" + str(_i),
                          use_container_width=True, disabled=True)

    # ---------- الأوسمة ----------
    st.markdown("<p class='home-h2'>أوسمتك <span>— تُكتسب بالمثابرة</span></p>",
                unsafe_allow_html=True)
    _badges = [
        ("🛡️", "الصامد",      "أنهيتَ تمرينًا كاملًا",     _done >= 1),
        ("⚡",   "البرق",       "جمعتَ 100 نقطة",           _xp >= 100),
        ("🧭",  "المُستنتِج", "أنهيتَ 3 تمارين",           _done >= 3),
        ("🔁",  "المُثابِر",   "5 أيام متتالية من الحل",   _strk >= 5),
    ]
    _bc = st.columns(4)
    for _i, (_bi, _bn, _bd, _got) in enumerate(_badges):
        with _bc[_i]:
            st.markdown(
                "<div class='home-bd" + (" got" if _got else "") + "'>"
                "<span class='bi'>" + _bi + "</span><b>" + _bn + "</b>"
                "<small>" + _bd + "</small></div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='home-note'>🕯️ <b>صُمّمت لظروفك.</b> المنصة تحفظ إجاباتك على جهازك، "
        "فإن انقطعت الكهرباء أو أغلقت الصفحة تعود حيث توقّفت. ولا تحتاج تسجيل دخول "
        "ولا أي بيانات شخصية.</div>", unsafe_allow_html=True)

    st.stop()

# ---------- وضع التمارين: شريط الرجوع إلى لوحة الطالب ----------
with st.container(key="exercise_nav"):
    _bk1, _bk2 = st.columns([1, 4])
    with _bk1:
        if st.button("← لوحة الطالب", key="physbook_samed_back", use_container_width=True):
            st.session_state["samed_view"] = "dashboard"
            st.switch_page("app.py")


# ==========================================================
# 7. اختيار التمرين + وضع الشرح المبسط
# ==========================================================
def display_title(item):
    icon = "🧮" if item["type"] == "interactive" else "📜"
    return f"{icon} {item['title']}"

with st.container(key="exercise_controls"):
    col_sel, col_toggle = st.columns([3, 1])
    with col_sel:
        _all_titles = [display_title(item) for item in questions_db]
        _goto = st.session_state.pop("physbook_goto_title", None)
        if _goto in _all_titles:
            st.session_state["physbook_qpick"] = _goto
        selected_title = st.selectbox(
            "📌 اختر التمرين المراد حله تفاعلياً:",
            _all_titles, key="physbook_qpick"
        )
    with col_toggle:
        explain_mode = st.toggle("🔍 شرح مبسط", value=False)

q = next(item for item in questions_db if display_title(item) == selected_title)
qid = q["id"]
qtype = q["type"]

if qid not in st.session_state["physbook_start_time"]:
    st.session_state["physbook_start_time"][qid] = time.time()
if qid not in st.session_state["physbook_no_hint_flag"]:
    st.session_state["physbook_no_hint_flag"][qid] = True

elapsed = st.session_state["physbook_time_spent"].get(qid)
if elapsed is None:
    elapsed = time.time() - st.session_state["physbook_start_time"][qid]

# --- مصدر مخفي تقرأ منه لوحة الأيقونتين (نص التمرين + القوانين) ---
_sb_total = len(q["steps"])
_sb_at = min(st.session_state.get(f"step_prog_{qid}", 1), _sb_total)
_sb_pct = int(((_sb_at - 1) / _sb_total) * 100)
_sb_chip = "📜 مسألة إثبات نظري" if qtype == "proof" else "🧮 تمرين رقمي تفاعلي"
_stmt_src = (
    f'<div class="sb-stmt"><span class="sb-chip">{_sb_chip}</span>'
    f'<h4>{q["title"]}</h4><p>{q["text"]}</p>{figure_html(qid)}'
    f'<div class="qprogress-bg"><div class="qprogress-fill" style="width:{_sb_pct}%;"></div></div>'
    f'<small>الخطوة {_sb_at} من {_sb_total}</small></div>'
)
_laws_src = "".join(
    f'<div class="formula-row"><span class="f-name">{_n}</span>'
    f'<span class="f-eq">{plain_to_eq(_f)}</span></div>'
    for _n, _f in FORMULA_SHEET
)
with st.container(key="phys_src"):
    st.markdown(
        f'<div id="phys-src-stmt">{_stmt_src}</div><div id="phys-src-laws">{_laws_src}</div>',
        unsafe_allow_html=True,
    )

# ==========================================================
# 8أ. مسار المسائل التفاعلية (تعويض وحل رقمي)
# ==========================================================
if qtype == "interactive":
    step_state_key = f"step_prog_{qid}"
    if step_state_key not in st.session_state:
        st.session_state[step_state_key] = 1
    current_step_user_at = st.session_state[step_state_key]

    q_progress_pct = int(((current_step_user_at - 1) / len(q["steps"])) * 100)

    top_l, top_r = st.columns([4, 1])
    with top_l:
        # سلسلة متصلة تمنع Markdown من تفسير HTML المتداخل كنص برمجي ظاهر.
        render_question_card_v18(
            key=f"{qid}_interactive", title=q["title"], statement_html=q["text"],
            figure_markup=figure_html(qid), progress_pct=q_progress_pct,
            step_number=min(current_step_user_at, len(q["steps"])), total_steps=len(q["steps"]),
            elapsed_label=fmt_time(elapsed), kind="interactive",
        )
    with top_r:
        st.write("")
        if st.button("🔁 إعادة حل هذا التمرين", key=f"reset_{qid}", use_container_width=True):
            reset_question(qid, "interactive")
            st.rerun()

    st.markdown("---")
    st.markdown('<h3 id="phys-steps-anchor">📝 مراحل التعويض والجذر التربيعي:</h3>', unsafe_allow_html=True)
    st.caption("الخطوات مرتبة من اليمين لليسار: مكتملة ✅ ← نشطة 🔵 ← مقفلة 🔒")

    step_cols = st.columns(len(q["steps"]))

    for idx, step in enumerate(q["steps"]):
        s_num = step["num"]
        step_key = f"{qid}_{s_num}"

        # 🟢 خطوة مكتملة
        if s_num < current_step_user_at:
            with step_cols[idx]:
                with st.container(key=f"card_{qid}_{s_num}_stepstate_completed", border=True):
                    completed_formula = eq_frag(step["prefix"])
                    for b in step["blanks"]:
                        completed_formula += f"<b>{b['target']}</b>" + eq_frag(b["suffix"])
                    root_str = f"  |  {eq_frag(step.get('root_prefix', ''))} <b>{step.get('root_target', '')}</b> {eq_frag(step.get('root_suffix', ''))}" if step.get("has_root") else ""
                    completed_line = f"{completed_formula} {root_str} = <b>{step['result_target']}</b>"
                    st.markdown(f"""
                    <span class="step-badge">✅ خطوة مكتملة</span>
                    <h4>{step["title"]}</h4>
                    {law_html(step["law"])}
                    {result_html(completed_line, pre_html=True)}
                    """, unsafe_allow_html=True)
            continue

        # ⚪ خطوة مغلقة
        if s_num > current_step_user_at:
            with step_cols[idx]:
                with st.container(key=f"card_{qid}_{s_num}_stepstate_locked", border=True):
                    st.markdown(f"""
                    <div class="lock-icon">🔒</div>
                    <h4>{step["title"]}</h4>
                    <small>أكمل الخطوة {s_num - 1} أولاً لفتح هذه الخطوة.</small>
                    """, unsafe_allow_html=True)
            continue

        # 🔵 الخطوة الحالية النشطة
        with step_cols[idx]:
          with st.container(key=f"card_{qid}_{s_num}_stepstate_active", border=True):
            st.markdown(f"""
            <span class="step-badge">✍️ الخطوة النشطة</span>
            <h4>{step["title"]}</h4>
            {law_html(law_no_given(step["law"]) if step.get("micro") else step["law"])}
            """, unsafe_allow_html=True)

            st.markdown(derive_html(qid, step), unsafe_allow_html=True)

            if explain_mode and step.get("simple_explain"):
                st.markdown(f'<div class="explain-box">💬 {step["simple_explain"]}</div>', unsafe_allow_html=True)

            attempts_so_far = st.session_state["physbook_attempts"].get(step_key, 0)
            hint_lvl_current = st.session_state["physbook_hint_level"].get(step_key, 0)
            potential_points = calc_points(attempts_so_far + 1, hint_lvl_current)
            _revealed = st.session_state.setdefault("physbook_revealed", {}).get(step_key, False)
            _mn = 0
            if step.get("micro"):
                st.markdown(micro_html(step, final_mode="none", qid=qid, reveal=_revealed), unsafe_allow_html=True)
                _mn = len(step["micro"])
            _steps_only = bool(step.get("micro"))
            user_blank_inputs = []
            user_root_val = None
            user_result = None
            if not _steps_only:
                with st.container(key="formula_blanks_row"):
                    st.markdown(
                        f'<div class="live-say"><span class="micro-num">{_mn + 1}</span>'
                        'عوّض المعطيات في العبارة العامة (من اليسار لليمين):</div>',
                        unsafe_allow_html=True,
                    )
                    cols = st.columns(1 + len(step["blanks"]) * 2)
                    cols[0].markdown(f"<div class='formula-text'>{eq_frag(step['prefix'])}</div>", unsafe_allow_html=True)
                    col_idx = 1
                    for bidx, b in enumerate(step["blanks"]):
                        with cols[col_idx]:
                            val = st.number_input(
                                label=b["label"], key=f"blank_{qid}_{s_num}_{bidx}",
                                value=(float(b["target"]) if _revealed else None), placeholder="..", label_visibility="collapsed"
                            )
                            user_blank_inputs.append(val)
                        col_idx += 1
                        with cols[col_idx]:
                            st.markdown(f"<div class='formula-text'>{eq_frag(b['suffix'])}</div>", unsafe_allow_html=True)
                        col_idx += 1

            _mn2 = 0
            if step.get("micro2"):
                st.markdown(
                    micro_html(step, final_mode="none", field="micro2", start=(_mn if _steps_only else _mn + 1), qid=qid, reveal=_revealed),
                    unsafe_allow_html=True,
                )
                _mn2 = len(step["micro2"])

            if step.get("has_root") and not _steps_only:
                with st.container(key="formula_root_row"):
                    st.markdown(
                        f'<div class="live-say"><span class="micro-num">{_mn + _mn2 + 2}</span>'
                        'عوّض القيمة تحت الجذر التربيعي:</div>',
                        unsafe_allow_html=True,
                    )
                    r_c1, r_c2, r_c3 = st.columns(3)
                    with r_c1:
                        st.markdown(f"<div class='formula-text'>{eq_frag(step['root_prefix'])}</div>", unsafe_allow_html=True)
                    with r_c2:
                        user_root_val = st.number_input(
                            label="root_val", key=f"root_{qid}_{s_num}",
                            value=(float(step["root_target"]) if _revealed else None), placeholder="..", label_visibility="collapsed"
                        )
                    with r_c3:
                        st.markdown(f"<div class='formula-text'>{eq_frag(step['root_suffix'])}</div>", unsafe_allow_html=True)

            if not _steps_only:
                _nres = _mn + _mn2 + 2 + (1 if step.get("has_root") else 0)
                _rlabel = step["result_label"]
                _rsym, _runit = result_eq_parts(_rlabel)
                _rsay = _rlabel.strip().rstrip(":").strip()
                with st.container(key="formula_res_row"):
                    st.markdown(
                        f'<div class="live-say"><span class="micro-num">{_nres}</span>{_rsay}</div>',
                        unsafe_allow_html=True,
                    )
                    rc1, rc2, rc3 = st.columns(3)
                    with rc1:
                        st.markdown(f"<div class='formula-text'>{eq_frag(_rsym + ' =')}</div>", unsafe_allow_html=True)
                    with rc2:
                        user_result = st.number_input(
                            _rlabel, key=f"res_{qid}_{s_num}",
                            value=(float(step["result_target"]) if _revealed else None), placeholder="..", label_visibility="collapsed"
                        )
                    with rc3:
                        st.markdown(f"<div class='formula-text'>{eq_frag(_runit)}</div>", unsafe_allow_html=True)

            else:
                st.markdown("<div class='note-box'>✅ أكمل فراغات الخطوات أعلاه بالترتيب، ثم اضغط «تحقق 🎯» للانتقال للخطوة التالية.</div>", unsafe_allow_html=True)

            with st.container(key="step_actions_row"):
                _bc1, _bc2, _bc3 = st.columns(3)
                with _bc1:
                    check_btn = st.button("تحقق 🎯", key=f"btn_{qid}_{s_num}", use_container_width=True)
                with _bc2:
                    hint_btn = st.button("💡 تلميح", key=f"hint_{qid}_{s_num}", use_container_width=True)
                with _bc3:
                    reveal_btn = st.button("✅ الإجابة الصحيحة", key=f"reveal_{qid}_{s_num}",
                                           use_container_width=True, disabled=_revealed)

            if reveal_btn:
                for _bi in range(len(step.get("blanks") or [])):
                    st.session_state.pop(f"blank_{qid}_{s_num}_{_bi}", None)
                st.session_state.pop(f"root_{qid}_{s_num}", None)
                st.session_state.pop(f"res_{qid}_{s_num}", None)
                st.session_state.setdefault("physbook_revealed", {})[step_key] = True
                st.session_state["physbook_hint_level"][step_key] = 3
                st.session_state["physbook_no_hint_flag"][qid] = False
                st.toast("تم إدخال الإجابة الصحيحة في الفراغات — اضغط «تحقق 🎯» للتقدم")
                st.rerun()

            st.markdown(f'<span class="points-chip">🎯 نقاط هذه المحاولة المتوقعة: {potential_points}</span>', unsafe_allow_html=True)

            if hint_btn:
                new_level = min(3, hint_lvl_current + 1)
                st.session_state["physbook_hint_level"][step_key] = new_level
                st.session_state["physbook_no_hint_flag"][qid] = False
                st.rerun()

            if hint_lvl_current >= 1:
                msg = rich_hint(step, hint_lvl_current)
                st.markdown(f'<div class="hint-box">💡 <b>شرح موجّه (مستوى {hint_lvl_current}):</b>{msg}</div>', unsafe_allow_html=True)
                if hint_lvl_current < 3:
                    st.caption("بحاجة لمساعدة أكبر؟ اضغط 💡 تلميح مرة أخرى.")

            if check_btn:
                st.session_state["physbook_attempts"][step_key] = st.session_state["physbook_attempts"].get(step_key, 0) + 1
                attempts_now = st.session_state["physbook_attempts"][step_key]

                if _steps_only:
                    pts = calc_points(attempts_now, hint_lvl_current)
                    st.session_state["physbook_total_xp"] += pts
                    st.success(f"{random.choice(SUCCESS_PHRASES)} أحسنت — اكتملت خطوات الحل! (+{pts} XP)")
                    st.session_state[step_state_key] = s_num + 1
                    st.rerun()

                blanks_correct = True
                for u_val, b_item in zip(user_blank_inputs, step["blanks"]):
                    if u_val is None or abs(u_val - b_item["target"]) > 0.01:
                        blanks_correct = False
                        break

                root_correct = True
                if step.get("has_root"):
                    if user_root_val is None or abs(user_root_val - step["root_target"]) > 0.1:
                        root_correct = False

                result_correct = False
                if user_result is not None:
                    if abs(user_result - step["result_target"]) <= step["result_tol"]:
                        result_correct = True
                    elif "alt_result_target" in step and abs(user_result - step["alt_result_target"]) <= step["result_tol"]:
                        result_correct = True

                if blanks_correct and root_correct and result_correct:
                    pts = calc_points(attempts_now, hint_lvl_current)
                    st.session_state["physbook_total_xp"] += pts
                    if attempts_now == 1 and hint_lvl_current == 0:
                        st.session_state["physbook_streak"] += 1
                    else:
                        st.session_state["physbook_streak"] = 0
                    if st.session_state["physbook_streak"] == 3:
                        award_badge("🔥 3 إجابات متتالية بلا أخطاء")
                    if st.session_state["physbook_streak"] == 5:
                        award_badge("⚡ 5 إجابات متتالية متقنة")
                    st.success(f"{random.choice(SUCCESS_PHRASES)} خطوة صحيحة بالكامل (+{pts} XP)")
                    st.session_state[step_state_key] = s_num + 1
                    st.rerun()
                elif not root_correct and blanks_correct:
                    st.warning("التعويض الأول صحيح، لكن قيمة الناتج تحت الجذر التربيعي غير صحيحة!")
                elif not blanks_correct:
                    st.warning("تأكد من كتابة أرقام المعطيات والإشارات بشكل صحيح داخل فراغات القانون!")
                else:
                    st.error("الناتج الحسابي النهائي غير دقيق! راجع العمليات الحسابية ❌")
                    if attempts_now >= 3:
                        st.info("جرّبت عدة مرات 💪 — استخدم زر 💡 تلميح فوق للمساعدة التدريجية.")

    if current_step_user_at > len(q["steps"]):
        if qid not in st.session_state["physbook_completed_questions"]:
            st.session_state["physbook_completed_questions"].add(qid)
            duration = time.time() - st.session_state["physbook_start_time"][qid]
            st.session_state["physbook_time_spent"][qid] = duration
            st.session_state["physbook_total_xp"] += 15
            if len(st.session_state["physbook_completed_questions"]) == 1:
                award_badge("🏅 أول تمرين مكتمل")
            if st.session_state["physbook_no_hint_flag"].get(qid, False):
                award_badge("⭐ إتقان بلا تلميحات")
            if len(st.session_state["physbook_completed_questions"]) == TOTAL_QUESTIONS:
                award_badge("🎓 إتقان كامل لجميع التمارين")
            st.balloons()
            _idx_now = next((_i for _i, _it in enumerate(questions_db) if _it["id"] == qid), None)
            if _idx_now is not None and _idx_now + 1 < len(questions_db):
                st.session_state["physbook_goto_title"] = display_title(questions_db[_idx_now + 1])
                st.toast("🎉 أحسنت! ننتقل إلى التمرين التالي…")
                time.sleep(1.8)
                st.rerun()

        dur = st.session_state["physbook_time_spent"].get(qid, 0)
        st.success(f"🎉 ممتاز جداً! أتقنت هذا التمرين خلال {fmt_time(dur)} (+15 XP مكافأة إنجاز).")
        if st.button("🔄 إعادة حل التمرين من البداية", key=f"restart_{qid}"):
            reset_question(qid, "interactive")
            st.rerun()

# ==========================================================
# 8ب. مسار مسائل الإثبات النظري (رمزي/عددي + LaTeX)
# ==========================================================
else:
    step_state_key = f"step_prog_{qid}"
    if step_state_key not in st.session_state:
        st.session_state[step_state_key] = 1
    current_step_user_at = st.session_state[step_state_key]

    q_progress_pct = int(((current_step_user_at - 1) / len(q["steps"])) * 100)

    top_l, top_r = st.columns([4, 1])
    with top_l:
        render_question_card_v18(
            key=f"{qid}_proof", title=q["title"], statement_html=q["text"],
            figure_markup=figure_html(qid), progress_pct=q_progress_pct,
            step_number=min(current_step_user_at, len(q["steps"])), total_steps=len(q["steps"]),
            elapsed_label=fmt_time(elapsed), kind="proof",
        )
    with top_r:
        st.write("")
        if st.button("🔁 إعادة حل هذا الإثبات", key=f"reset_{qid}", use_container_width=True):
            reset_question(qid, "proof")
            st.rerun()

    st.markdown("---")
    st.markdown('<h3 id="phys-steps-anchor">📜 خطوات الإثبات والتعويض الرمزي:</h3>', unsafe_allow_html=True)
    st.caption("الخطوات مرتبة من اليمين لليسار: مكتملة ✅ ← نشطة 🔵 ← مقفلة 🔒  |  أكمل الفراغ الرمزي أو العددي في كل معادلة لإثبات فهمك الخطوة.")

    step_cols = st.columns(len(q["steps"]))

    for idx, step in enumerate(q["steps"]):
        s_num = step["num"]
        step_key = f"{qid}_{s_num}"

        # 🟢 خطوة مكتملة
        if s_num < current_step_user_at:
            with step_cols[idx]:
                with st.container(key=f"card_{qid}_{s_num}_stepstate_completed", border=True):
                    st.markdown(f"""
                    <span class="step-badge">✅ خطوة مكتملة</span>
                    <h4>{step["title"]}</h4>
                    {law_html(step["law"])}
                    {result_html(step['completed_display'])}
                    """, unsafe_allow_html=True)
            continue

        # ⚪ خطوة مقفلة
        if s_num > current_step_user_at:
            with step_cols[idx]:
                with st.container(key=f"card_{qid}_{s_num}_stepstate_locked", border=True):
                    st.markdown(f"""
                    <div class="lock-icon">🔒</div>
                    <h4>{step["title"]}</h4>
                    <small>أكمل الخطوة {s_num - 1} أولاً لفتح هذه الخطوة.</small>
                    """, unsafe_allow_html=True)
            continue

        # 🔵 الخطوة الحالية النشطة
        with step_cols[idx]:
          with st.container(key=f"card_{qid}_{s_num}_stepstate_active", border=True):
            st.markdown(f"""
            <span class="step-badge">✍️ الخطوة النشطة</span>
            <h4>{step["title"]}</h4>
            {law_html(step["law"])}
            """, unsafe_allow_html=True)

            _only_choices = bool(step.get("choices"))
            if not _only_choices:
                st.markdown(derive_html(qid, step), unsafe_allow_html=True)

            if explain_mode:
                st.markdown(f'<div class="explain-box">💬 {step.get("label", "")}</div>', unsafe_allow_html=True)

            _revealed = st.session_state.setdefault("physbook_revealed", {}).get(step_key, False)
            _plabel = step.get("label", "")
            _fmode = "none" if (step.get("micro_only") or step.get("micro")) else "preview"
            if _only_choices:
                pass
            elif step.get("micro"):
                st.markdown(micro_html(step, final_mode=_fmode, final_say=_plabel, qid=qid, reveal=_revealed), unsafe_allow_html=True)
            else:
                st.markdown(
                    micro_html(step, final_mode=_fmode, field="__nomicro__", final_say=_plabel, qid=qid, reveal=_revealed),
                    unsafe_allow_html=True,
                )

            attempts_so_far = st.session_state["physbook_attempts"].get(step_key, 0)
            hint_lvl_current = st.session_state["physbook_hint_level"].get(step_key, 0)
            potential_points = calc_points(attempts_so_far + 1, hint_lvl_current)

            _micro_only = bool(step.get("micro_only")) or bool(step.get("micro"))
            _choices = step.get("choices") or []
            _pick = None
            _sym_key = f"symbuf_{step_key}"
            _pending = st.session_state.get(_sym_key)
            user_val = ""
            if _choices:
                st.markdown("<div class='note-box'>🧠 اختر التعليل الصحيح من بين التعليلات الثلاثة أدناه:</div>", unsafe_allow_html=True)
                st.markdown("<style>div[data-testid='stRadio'] label p{font-size:1.2rem !important;line-height:2.1 !important;font-weight:700;color:#0f172a}div[data-testid='stRadio'] label{padding:6px 2px}div[data-testid='stRadio'] input{transform:scale(1.25)}</style>", unsafe_allow_html=True)
                _pend_pick = st.session_state.pop(f"mcqpick_{step_key}", None)
                if _pend_pick is not None:
                    st.session_state.pop(f"mcq_{step_key}", None)
                _pick = st.radio(
                    "choices", options=list(range(len(_choices))),
                    format_func=lambda _ci: _choices[_ci], key=f"mcq_{step_key}",
                    index=_pend_pick, label_visibility="collapsed",
                )
            elif _micro_only:
                st.markdown("<div class='note-box'>✅ أكمل فراغات الخطوات أعلاه بالترتيب، ثم اضغط «تحقق 🎯» للانتقال للخطوة التالية.</div>", unsafe_allow_html=True)
            else:
                if _pending is not None:
                    st.session_state.pop(f"proofinput_{step_key}", None)
                with st.container(key="formula_proof_row"):
                    fc1, fc2, fc3 = st.columns([2, 1.3, 2])
                    with fc1:
                        st.markdown(f"<div class='formula-text'>{eq_frag(step['prefix'])}</div>", unsafe_allow_html=True)
                    with fc2:
                        user_val = st.text_input(
                            "input_field", key=f"proofinput_{step_key}",
                            value=(_pending if _pending is not None else (str(step["target"]) if _revealed else "")),
                            placeholder="اكتب الإجابة أو استعمل مكتبة الرموز...", label_visibility="collapsed"
                        )
                    with fc3:
                        st.markdown(f"<div class='formula-text'>{eq_frag(step['suffix'])}</div>", unsafe_allow_html=True)
                st.session_state.pop(_sym_key, None)
                st.markdown("<div style='text-align:right;color:#475569;font-weight:700;margin:8px 0 2px'>🔤 مكتبة الرموز — اضغط الرمز ليُضاف إلى إجابتك</div>", unsafe_allow_html=True)
                for _r in range(0, len(SYMBOL_LIBRARY), 9):
                    _chunk = SYMBOL_LIBRARY[_r:_r + 9]
                    _scols = st.columns(len(_chunk))
                    for _k2, _sym in enumerate(_chunk):
                        with _scols[_k2]:
                            if st.button(_sym, key=f"sym_{step_key}_{_r + _k2}", use_container_width=True):
                                _cur = st.session_state.get(f"proofinput_{step_key}", "") or ""
                                if _sym == "⌫":
                                    _new_val = _cur[:-1]
                                elif _sym == "مسح":
                                    _new_val = ""
                                elif _sym == "⬜":
                                    _new_val = _cur + " "
                                else:
                                    _new_val = _cur + _sym
                                st.session_state[_sym_key] = _new_val
                                st.session_state.pop(f"proofinput_{step_key}", None)
                                st.rerun()

            btn_col, hint_col, rev_col = st.columns(3)
            with btn_col:
                check_btn = st.button("تحقق 🎯", key=f"btn_{step_key}", use_container_width=True)
            with hint_col:
                hint_btn = st.button("💡 تلميح", key=f"hint_{step_key}", use_container_width=True)
            with rev_col:
                reveal_btn = st.button("✅ الإجابة الصحيحة", key=f"reveal_{step_key}",
                                       use_container_width=True, disabled=_revealed)

            if reveal_btn:
                st.session_state.pop(f"proofinput_{step_key}", None)
                if step.get("choices"):
                    st.session_state[f"mcqpick_{step_key}"] = step.get("answer_index", 0)
                st.session_state.setdefault("physbook_revealed", {})[step_key] = True
                st.session_state["physbook_hint_level"][step_key] = 2
                st.session_state["physbook_no_hint_flag"][qid] = False
                st.toast("تم إدخال الإجابة الصحيحة في الفراغ — اضغط «تحقق 🎯» للتقدم")
                st.rerun()

            st.markdown(f'<span class="points-chip">🎯 نقاط هذه المحاولة المتوقعة: {potential_points}</span>', unsafe_allow_html=True)

            if hint_btn:
                st.session_state["physbook_hint_level"][step_key] = min(2, hint_lvl_current + 1)
                st.session_state["physbook_no_hint_flag"][qid] = False
                st.rerun()

            if hint_lvl_current >= 1:
                msg = rich_hint(step, hint_lvl_current + 1)
                st.markdown(f'<div class="hint-box">💡 <b>شرح موجّه:</b>{msg}</div>', unsafe_allow_html=True)
                if hint_lvl_current < 2:
                    st.caption("بحاجة لمساعدة أكبر؟ اضغط 💡 تلميح مرة أخرى.")

            if check_btn:
                st.session_state["physbook_attempts"][step_key] = st.session_state["physbook_attempts"].get(step_key, 0) + 1
                attempts_now = st.session_state["physbook_attempts"][step_key]

                if _choices:
                    if _pick is None:
                        st.warning("اختر أحد التعليلات أولاً!")
                    elif _pick == step.get("answer_index", 0):
                        pts = calc_points(attempts_now, hint_lvl_current)
                        st.session_state["physbook_total_xp"] += pts
                        st.success(f"{random.choice(SUCCESS_PHRASES)} تعليل صحيح! (+{pts} XP)")
                        st.session_state[step_state_key] = s_num + 1
                        st.rerun()
                    else:
                        st.error("التعليل قريب لكنه غير دقيق — راجع خطوات الحل أعلاه ثم اختر مرة أخرى. ❌")
                elif _micro_only:
                    pts = calc_points(attempts_now, hint_lvl_current)
                    st.session_state["physbook_total_xp"] += pts
                    st.success(f"{random.choice(SUCCESS_PHRASES)} أحسنت — اكتملت خطوات التعليل! (+{pts} XP)")
                    st.session_state[step_state_key] = s_num + 1
                    st.rerun()
                elif not user_val or user_val.strip() == "":
                    st.warning("الرجاء كتابة الإجابة أولاً داخل الفراغ!")
                else:
                    is_correct = False
                    if step["type"] == "symbol":
                        case_sens = step.get("case_sensitive", False)
                        is_correct = symbol_answers_match(user_val, step["target"], case_sens)
                    else:  # number
                        try:
                            num_float = float(user_val.replace(",", "."))
                            is_correct = abs(num_float - step["target"]) <= step["tol"]
                        except ValueError:
                            st.error("يرجى كتابة رقم عددي صحيح (مثال: 0.889 أو 36)!")
                            is_correct = None

                    if is_correct:
                        pts = calc_points(attempts_now, hint_lvl_current)
                        st.session_state["physbook_total_xp"] += pts
                        if attempts_now == 1 and hint_lvl_current == 0:
                            st.session_state["physbook_streak"] += 1
                        else:
                            st.session_state["physbook_streak"] = 0
                        if st.session_state["physbook_streak"] == 3:
                            award_badge("🔥 3 إجابات متتالية بلا أخطاء")
                        if st.session_state["physbook_streak"] == 5:
                            award_badge("⚡ 5 إجابات متتالية متقنة")
                        st.success(f"{random.choice(SUCCESS_PHRASES)} إجابة صحيحة! (+{pts} XP)")
                        st.session_state[step_state_key] = s_num + 1
                        st.rerun()
                    elif is_correct is False:
                        if step["type"] == "symbol":
                            st.error("الرمز غير دقيق! تأكد من كتابة الرمز المطلوب بالضبط المطلوب. ❌")
                        else:
                            st.error("النتيجة العددية غير صحيحة، راجع العمليات الحسابية! ❌")
                        if attempts_now >= 3:
                            st.info("جرّبت عدة مرات 💪 — استخدم زر 💡 تلميح فوق للمساعدة التدريجية.")

    if current_step_user_at > len(q["steps"]):
        st.markdown(f'<div class="note-box">🎯 <b>النتيجة النهائية:</b> {q["conclusion"]}</div>', unsafe_allow_html=True)
        if qid not in st.session_state["physbook_completed_questions"]:
            st.session_state["physbook_completed_questions"].add(qid)
            duration = time.time() - st.session_state["physbook_start_time"][qid]
            st.session_state["physbook_time_spent"][qid] = duration
            st.session_state["physbook_total_xp"] += 15
            if len(st.session_state["physbook_completed_questions"]) == 1:
                award_badge("🏅 أول تمرين مكتمل")
            award_badge("🧠 عقل تحليلي (أتقن برهاناً)")
            if st.session_state["physbook_no_hint_flag"].get(qid, True):
                award_badge("⭐ إتقان بلا تلميحات")
            if len(st.session_state["physbook_completed_questions"]) == TOTAL_QUESTIONS:
                award_badge("🎓 إتقان كامل لجميع التمارين")
            st.balloons()
            _idx_now = next((_i for _i, _it in enumerate(questions_db) if _it["id"] == qid), None)
            if _idx_now is not None and _idx_now + 1 < len(questions_db):
                st.session_state["physbook_goto_title"] = display_title(questions_db[_idx_now + 1])
                st.toast("🎉 أحسنت! ننتقل إلى التمرين التالي…")
                time.sleep(1.8)
                st.rerun()

        dur = st.session_state["physbook_time_spent"].get(qid, 0)
        st.success(f"🎉 أحسنت! أتممت هذا الإثبات خلال {fmt_time(dur)} (+15 XP مكافأة إتمام).")
        if st.button("🔄 إعادة حل الإثبات من البداية", key=f"restart_{qid}"):
            reset_question(qid, "proof")
            st.rerun()

# ==========================================================
# 9. شهادة الإنجاز عند إتمام جميع التمارين
# ==========================================================
if len(st.session_state["physbook_completed_questions"]) == TOTAL_QUESTIONS:
    st.snow()
    name_display = st.session_state["physbook_student_name"] or "طالب مجتهد"
    total_time = sum(st.session_state["physbook_time_spent"].values())
    level_label, _, _ = get_level(st.session_state["physbook_total_xp"])

    st.markdown(f"""
    <div class="cert-box">
        <h2>🏆 شهادة إتمام</h2>
        <p style="font-size:1.2rem;">تُمنح هذه الشهادة إلى الطالب/ـة</p>
        <h3>{name_display}</h3>
        <p>لإتمامه/ـا بنجاح جميع تمارين درس <b>الزخم الخطي والدفع</b></p>
        <p>المستوى: <b>{level_label}</b> &nbsp;|&nbsp; إجمالي النقاط: <b>{st.session_state["physbook_total_xp"]} XP</b> &nbsp;|&nbsp; الوقت الكلي: <b>{fmt_time(total_time)}</b></p>
    </div>
    """, unsafe_allow_html=True)

    cert_text = f"""شهادة إتمام
=================
الطالب/ـة: {name_display}
الدرس: الزخم الخطي والدفع وحفظ الزخم
عدد التمارين المكتملة: {len(st.session_state["physbook_completed_questions"])} / {TOTAL_QUESTIONS}
إجمالي نقاط الخبرة: {st.session_state["physbook_total_xp"]} XP
المستوى: {level_label}
الوقت الكلي: {fmt_time(total_time)}
الأوسمة: {', '.join(sorted(st.session_state["physbook_badges"])) if st.session_state["physbook_badges"] else "لا يوجد"}
التاريخ: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
    st.download_button(
        "📄 تنزيل شهادة الإنجاز", data=cert_text,
        file_name=f"شهادة_{name_display}.txt", mime="text/plain", use_container_width=True
    )



# ==========================================================
# تجميد بطاقة التمرين (Freeze) من دون أي تغيير في بقية الواجهة:
# البطاقة تبقى في مكانها المعتاد، وعند تجاوزها أثناء النزول
# تظهر نسخة مُجمّدة منها في نفس الموضع الأفقي، وتختفي عند العودة لمكانها
# ==========================================================
components.html(
    r"""
<script>
(function () {
  var doc = (window.parent && window.parent.document) ? window.parent.document : document;
  var win = window.parent || window;
  var CLONE_ID = 'phys-frozen-card';
  var TAB_ID = 'phys-frozen-tab';
  var panelHidden = false;
  var natRight = null;

  /* إلغاء الاحتياطي لأن السكربت يعمل */
  doc.documentElement.classList.add('phys-js');

  function srcCard() {
    return doc.querySelector('.q-card');
  }

  function topOffset() {
    var h = doc.querySelector('header[data-testid="stHeader"]');
    if (!h) return 6;
    var cs = win.getComputedStyle(h);
    if (cs.position === 'static' || cs.display === 'none') return 6;
    return Math.round(h.getBoundingClientRect().height) + 6;
  }

  /* the statement lives permanently in the sidebar; the floating panel is
     only a fallback for when that sidebar is collapsed or too narrow */
  function sidebarOpen() {
    var sb = doc.querySelector('section[data-testid="stSidebar"]');
    if (!sb) return false;
    var cs = win.getComputedStyle(sb);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (sb.getAttribute('aria-expanded') === 'false') return false;
    var sr = sb.getBoundingClientRect();
    var vw2 = win.innerWidth || doc.documentElement.clientWidth || 1280;
    if (sr.width < 90) return false;
    if (sr.right <= 8 || sr.left >= vw2 - 8) return false;
    return true;
  }

  function mainSection() {
    return doc.querySelector('section[data-testid="stMain"]');
  }

  function reserveNow() {
    var ms = mainSection();
    if (!ms || !ms.dataset.physReserve) return 0;
    return parseInt(ms.dataset.physReserve, 10) || 0;
  }

  /* carve real space on the right so the panel never covers the steps */
  function reserveHosts() {
    var an = anchorEl();
    if (!an) return [];
    var root = doc.querySelector('section[data-testid="stMain"] div[data-testid="stMainBlockContainer"]')
            || doc.querySelector('section[data-testid="stMain"] .block-container');
    if (!root) return [];
    var vb = null, ch = root.children, i;
    for (i = 0; i < ch.length; i++) {
      if (ch[i].getAttribute && ch[i].getAttribute('data-testid') === 'stVerticalBlock') { vb = ch[i]; break; }
    }
    if (!vb) vb = root;
    var el = an;
    while (el && el.parentElement && el.parentElement !== vb) el = el.parentElement;
    if (!el || el.parentElement !== vb) return [];
    var out = [];
    while (el) { out.push(el); el = el.nextElementSibling; }
    return out;
  }

  function clearReserve() {
    var ms = mainSection();
    if (ms) {
      ms.style.removeProperty('padding-right');
      if (ms.dataset.physReserve) delete ms.dataset.physReserve;
    }
    var old = doc.querySelectorAll('[data-phys-res]'), i;
    for (i = 0; i < old.length; i++) {
      old[i].style.removeProperty('padding-right');
      old[i].removeAttribute('data-phys-res');
    }
  }

  function setReserve(px) {
    px = Math.max(0, Math.round(px || 0));
    var ms = mainSection();
    var hosts = reserveHosts();
    var old = doc.querySelectorAll('[data-phys-res]');
    var changed = false, i, j, keep;
    if (!hosts.length || px <= 0) {
      if (reserveNow() === 0 && old.length === 0) return false;
      clearReserve();
      return true;
    }
    for (i = 0; i < old.length; i++) {
      keep = false;
      for (j = 0; j < hosts.length; j++) { if (hosts[j] === old[i]) { keep = true; break; } }
      if (!keep) {
        old[i].style.removeProperty('padding-right');
        old[i].removeAttribute('data-phys-res');
        changed = true;
      }
    }
    for (i = 0; i < hosts.length; i++) {
      if (hosts[i].getAttribute('data-phys-res') !== String(px)) {
        hosts[i].setAttribute('data-phys-res', String(px));
        hosts[i].style.setProperty('padding-right', px + 'px', 'important');
        changed = true;
      }
    }
    if (ms) ms.dataset.physReserve = String(px);
    return changed;
  }

  function getClone() {
    var clone = doc.getElementById(CLONE_ID);
    if (!clone) {
      clone = doc.createElement('div');
      clone.id = CLONE_ID;
      clone.innerHTML =
        '<div class="phys-panel-bar">' +
          '<span class="phys-panel-title">\ud83d\udcc4 \u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646</span>' +
          '<button type="button" class="phys-panel-close" title="\u0625\u062e\u0641\u0627\u0621">\u2715</button>' +
        '</div>' +
        '<div class="phys-panel-body"></div>';
      doc.body.appendChild(clone);
      var btn = clone.querySelector('.phys-panel-close');
      if (btn) {
        btn.addEventListener('click', function (ev) {
          ev.preventDefault();
          ev.stopPropagation();
          panelHidden = true;
          update();
        });
      }
    }
    return clone;
  }

  function getTab() {
    var tab = doc.getElementById(TAB_ID);
    if (!tab) {
      tab = doc.createElement('div');
      tab.id = TAB_ID;
      tab.textContent = '\ud83d\udcc4 \u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646';
      doc.body.appendChild(tab);
      tab.addEventListener('click', function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        panelHidden = false;
        update();
      });
    }
    return tab;
  }

  /* تحويل الأرقام السفلية إلى <sub> حتى يظهر الرقم أسفل يمين الرمز */
  var SUBS = {
    '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
    '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9'
  };
  var SUB_RE = /[\u2080-\u2089]/;
  var SUB_HOSTS = '.sb-stmt, .q-card, .law-guide-box, .explain-box, .hint-box, .proof-line, h4, [data-testid="stAlert"]';

  function fixSubscripts() {
    var hosts = doc.querySelectorAll(SUB_HOSTS);
    for (var i = 0; i < hosts.length; i++) {
      var host = hosts[i];
      if (!SUB_RE.test(host.textContent)) continue;

      var walker = doc.createTreeWalker(host, NodeFilter.SHOW_TEXT, {
        acceptNode: function (n) {
          var p = n.parentNode;
          if (!p) return NodeFilter.FILTER_REJECT;
          var tag = p.nodeName;
          if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'SUB' ||
              tag === 'INPUT' || tag === 'TEXTAREA') return NodeFilter.FILTER_REJECT;
          if (p.closest && p.closest('.katex, .formula-text')) return NodeFilter.FILTER_REJECT;
          return SUB_RE.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        }
      });

      var nodes = [], n;
      while ((n = walker.nextNode())) { nodes.push(n); }

      for (var j = 0; j < nodes.length; j++) {
        var node = nodes[j];
        var text = node.nodeValue;
        var frag = doc.createDocumentFragment();
        var buf = '';
        for (var k = 0; k < text.length; k++) {
          var ch = text.charAt(k);
          if (SUBS[ch]) {
            if (buf) { frag.appendChild(doc.createTextNode(buf)); buf = ''; }
            var sub = doc.createElement('sub');
            sub.textContent = SUBS[ch];
            frag.appendChild(sub);
          } else {
            buf += ch;
          }
        }
        if (buf) { frag.appendChild(doc.createTextNode(buf)); }
        if (node.parentNode) { node.parentNode.replaceChild(frag, node); }
      }
    }
  }

  /* فرض الخاصية بقوة (لأن CSS في الملف يستعمل !important) */
  function css(el, props) {
    for (var k in props) {
      if (Object.prototype.hasOwnProperty.call(props, k)) {
        el.style.setProperty(k, props[k], 'important');
      }
    }
  }

  /* ===== معادلات LaTeX: من اليسار إلى اليمين مع رموز سفلية صحيحة ===== */
  function fixLatex() {
    var hosts = doc.querySelectorAll('[data-testid="stLatex"], .stLatex, .katex-display, .katex, .katex-html');
    for (var i = 0; i < hosts.length; i++) {
      var el = hosts[i];
      css(el, { 'direction': 'ltr', 'unicode-bidi': 'isolate' });
      if (el.classList.contains('katex-display') ||
          el.getAttribute('data-testid') === 'stLatex' ||
          el.classList.contains('stLatex')) {
        css(el, { 'text-align': 'center' });
      }
      var host = el.parentElement;
      if (host && host.getAttribute('data-testid') === 'stMarkdownContainer') {
        css(host, { 'direction': 'ltr', 'text-align': 'center' });
      }
    }
    var msub = doc.querySelectorAll('.katex .msupsub, .katex .vlist-t, .katex .vlist');
    for (var j = 0; j < msub.length; j++) {
      css(msub[j], { 'direction': 'ltr', 'text-align': 'left' });
    }
  }

  /* ===== صفوف الإدخال: سطر واحد متراصف (لا نصف فوق ونصف تحت) ===== */
  function layoutFormulaRows() {
    var rows = doc.querySelectorAll(
      '.st-key-formula_proof_row div[data-testid="stHorizontalBlock"],' +
      '.st-key-formula_blanks_row div[data-testid="stHorizontalBlock"],' +
      '.st-key-formula_res_row div[data-testid="stHorizontalBlock"],' +
      '.st-key-formula_root_row div[data-testid="stHorizontalBlock"]'
    );
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      css(row, {
        'direction': 'ltr',
        'display': 'flex',
        'flex-wrap': 'nowrap',
        'align-items': 'center',
        'justify-content': 'center',
        'gap': '5px',
        'row-gap': '0px',
        'overflow-x': 'auto',
        'overflow-y': 'visible'
      });
      for (var j = 0; j < row.children.length; j++) {
        var col = row.children[j];
        if (!col.getAttribute || col.getAttribute('data-testid') !== 'stColumn') continue;
        var input = col.querySelector('input');
        css(col, {
          'display': 'flex',
          'align-items': 'center',
          'justify-content': 'center',
          'flex': '0 0 auto',
          'min-width': '0',
          'padding': '0 2px',
          'width': input ? '104px' : 'fit-content'
        });
        if (input) { css(input, { 'width': '100%', 'min-width': '0' }); }
      }
    }
  }

  /* ===== شريط الخطوات: 3 إطارات فقط في الشاشة والبقية بالسحب الأفقي ===== */
  var VISIBLE_STEPS = 3;
  var MIN_STEP_W = 380;
  var STRIP_GAP = 14;

  function stepStrips() {
    var marks = doc.querySelectorAll('[class*="_stepstate_"]');
    var out = [];
    for (var i = 0; i < marks.length; i++) {
      var s = marks[i].closest ? marks[i].closest('div[data-testid="stHorizontalBlock"]') : null;
      if (s && out.indexOf(s) === -1) out.push(s);
    }
    return out;
  }

  function stripColumns(strip) {
    var cols = [];
    for (var i = 0; i < strip.children.length; i++) {
      var c = strip.children[i];
      if (c.getAttribute && c.getAttribute('data-testid') === 'stColumn') cols.push(c);
    }
    return cols;
  }

  function enableDrag(strip) {
    if (strip.dataset.physDrag === '1') return;
    strip.dataset.physDrag = '1';

    var down = false, startX = 0, startScroll = 0, moved = false;

    strip.addEventListener('mousedown', function (e) {
      if (e.target && e.target.closest &&
          e.target.closest('input, textarea, select, button, label, a')) return;
      down = true; moved = false;
      startX = e.pageX;
      startScroll = strip.scrollLeft;
      css(strip, { 'cursor': 'grabbing' });
    });
    strip.addEventListener('mousemove', function (e) {
      if (!down) return;
      var dx = e.pageX - startX;
      if (Math.abs(dx) > 3) { moved = true; e.preventDefault(); }
      strip.scrollLeft = startScroll - dx;
    });
    function release() { down = false; css(strip, { 'cursor': 'grab' }); }
    strip.addEventListener('mouseup', release);
    strip.addEventListener('mouseleave', release);
    doc.addEventListener('mouseup', release);
    strip.addEventListener('click', function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
    }, true);
    strip.addEventListener('wheel', function (e) {
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
        strip.scrollLeft += e.deltaY;
        e.preventDefault();
      }
    }, { passive: false });
    strip.addEventListener('touchstart', function () { }, { passive: true });
  }

  function addDragHint(strip) {
    var cols = stripColumns(strip);
    if (cols.length <= VISIBLE_STEPS) return;
    var holder = strip.parentElement;
    if (!holder || holder.querySelector(':scope > .phys-hint-drag')) return;
    var hint = doc.createElement('div');
    hint.className = 'phys-hint-drag';
    hint.textContent = '\u2194\uFE0F \u0627\u0633\u062D\u0628 \u0627\u0644\u0634\u0631\u064A\u0637 \u064A\u0645\u064A\u0646\u064B\u0627 \u0623\u0648 \u064A\u0633\u0627\u0631\u064B\u0627 \u0644\u0625\u0638\u0647\u0627\u0631 \u0628\u0627\u0642\u064A \u0627\u0644\u062E\u0637\u0648\u0627\u062A (' + cols.length + ' \u062E\u0637\u0648\u0627\u062A)';
    holder.insertBefore(hint, strip);
  }

  function layoutSteps() {
    var strips = stepStrips();
    for (var i = 0; i < strips.length; i++) {
      var strip = strips[i];
      var cols = stripColumns(strip);
      if (!cols.length) continue;

      strip.classList.add('phys-strip');
      css(strip, {
        'display': 'flex',
        'flex-wrap': 'nowrap',
        'overflow-x': 'auto',
        'overflow-y': 'visible',
        'align-items': 'stretch',
        'gap': STRIP_GAP + 'px',
        'padding-bottom': '10px',
        'cursor': 'grab',
        'scroll-behavior': 'smooth'
      });

      var avail = strip.clientWidth || Math.round(strip.getBoundingClientRect().width);
      var n = Math.min(VISIBLE_STEPS, cols.length);
      while (n > 1 && (avail - STRIP_GAP * (n - 1) - 6) / n < MIN_STEP_W) { n--; }
      var w = Math.floor((avail - STRIP_GAP * (n - 1) - 6) / n);
      if (w < MIN_STEP_W) w = MIN_STEP_W;
      if (avail > 0 && w > 200) {
        for (var j = 0; j < cols.length; j++) {
          css(cols[j], {
            'flex': '0 0 auto',
            'width': w + 'px',
            'min-width': w + 'px',
            'max-width': w + 'px'
          });
        }
      }

      enableDrag(strip);
      addDragHint(strip);

      /* توسيط الخطوة النشطة تلقائياً (حساب نسبي يعمل مع RTL) */
      var active = strip.querySelector('[class*="_stepstate_active"]');
      if (active && active.closest) {
        var col = active.closest('div[data-testid="stColumn"]');
        var idx = col ? cols.indexOf(col) : -1;
        if (col && idx >= 0 && strip.dataset.physCentered !== String(idx)) {
          strip.dataset.physCentered = String(idx);
          var cr = col.getBoundingClientRect();
          var sr = strip.getBoundingClientRect();
          var delta = (cr.left + cr.width / 2) - (sr.left + sr.width / 2);
          if (Math.abs(delta) > 2) { strip.scrollLeft += delta; }
        }
      }
    }
  }

  /* ===== إدخال القيمة داخل المعادلة مكان علامة الاستفهام ===== */
  var wantFocusAt = 0;

  function realProofInput() {
    var row = doc.querySelector('.st-key-formula_proof_row');
    return row ? row.querySelector('input') : null;
  }

  function clickCheck() {
    var cards = doc.querySelectorAll('[class*="_stepstate_active"]');
    for (var i = 0; i < cards.length; i++) {
      var btns = cards[i].querySelectorAll('button');
      for (var j = 0; j < btns.length; j++) {
        if ((btns[j].textContent || '').indexOf('\u062A\u062D\u0642\u0642') !== -1) {
          btns[j].click();
          return true;
        }
      }
    }
    return false;
  }

  var committing = false;
  var commitTimer = 0;

  function setNative(el, val) {
    try {
      var d = Object.getOwnPropertyDescriptor(win.HTMLInputElement.prototype, 'value');
      if (d && d.set) { d.set.call(el, val); } else { el.value = val; }
    } catch (err) { el.value = val; }
  }

  function fire(el, type, ctor, extra) {
    try {
      var C = win[ctor] || window[ctor];
      var ev = new C(type, extra || { bubbles: true });
      if (extra && extra.keyCode) {
        try { Object.defineProperty(ev, 'keyCode', { get: function () { return extra.keyCode; } }); } catch (e1) { }
        try { Object.defineProperty(ev, 'which', { get: function () { return extra.keyCode; } }); } catch (e2) { }
      }
      el.dispatchEvent(ev);
      return true;
    } catch (err) { return false; }
  }

  /* نسخ ما يكتبه الطالب فوراً إلى حقل ستريمليت الحقيقي */
  function mirrorValue(val) {
    var real = realProofInput();
    if (!real) return null;
    if (real.value !== val) {
      setNative(real, val);
      fire(real, 'input', 'Event');
    }
    return real;
  }

  /* تثبيت القيمة فعلياً داخل ستريمليت: هذا ما يجعل زر «تحقق» يرى الإجابة */
  function commitValue(val) {
    if (committing) return false;
    var real = mirrorValue(val);
    if (!real) return false;
    committing = true;

    var prev = doc.activeElement;
    var isSlot = !!(prev && prev.classList && prev.classList.contains('phys-slot-input'));
    var selS = null, selE = null;
    if (isSlot) { try { selS = prev.selectionStart; selE = prev.selectionEnd; } catch (e0) { } }

    var main = doc.querySelector('section[data-testid="stMain"]');
    var keepTop = main ? main.scrollTop : 0;

    /* تركيز ثم خروج حقيقي: ستريمليت يسجل القيمة عند الخروج أو عند Enter */
    try {
      if (real.focus) { real.focus({ preventScroll: true }); }
      if (real.blur) { real.blur(); }
    } catch (err) { }
    fire(real, 'keydown', 'KeyboardEvent', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true });
    fire(real, 'keypress', 'KeyboardEvent', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true });
    fire(real, 'change', 'Event');
    fire(real, 'focusout', 'FocusEvent');

    if (main) { main.scrollTop = keepTop; }
    if (isSlot) {
      try {
        prev.focus({ preventScroll: true });
        if (selS !== null) { prev.setSelectionRange(selS, selE); }
      } catch (e5) { }
    }
    committing = false;
    return true;
  }

  /* تثبيت تلقائي بعد توقف الكتابة حتى تكون الإجابة جاهزة قبل أي زر */
  function scheduleCommit() {
    if (commitTimer) { win.clearTimeout(commitTimer); }
    commitTimer = win.setTimeout(function () {
      commitTimer = 0;
      var inp = doc.querySelector('input.phys-final-input');
      if (inp) { commitValue(inp.value || ''); }
    }, 550);
  }

  /* أي ضغطة على زر تُثبّت القيمة قبل أن تُرسل */
  function installCommitGuard() {
    if (!doc.body || doc.body.dataset.physCommitGuard === '1') return;
    doc.body.dataset.physCommitGuard = '1';
    var handler = function (e) {
      var t = e.target;
      if (!t || !t.closest) return;
      if (t.closest('input.phys-slot-input')) return;
      if (!t.closest('button')) return;
      var inp = doc.querySelector('input.phys-final-input');
      if (!inp) return;
      if (commitTimer) { win.clearTimeout(commitTimer); commitTimer = 0; }
      commitValue(inp.value || '');
    };
    doc.addEventListener('mousedown', handler, true);
    doc.addEventListener('touchstart', handler, true);
  }

  function autoSize(inp) {
    var len = (inp.value || '').length;
    var w = Math.max(78, Math.min(260, 48 + len * 12));
    inp.style.width = w + 'px';
  }

  function wireSlotInput(inp) {
    inp.addEventListener('input', function () {
      autoSize(this);
      mirrorValue(this.value);
      scheduleCommit();
    });
    inp.addEventListener('focus', function () { wantFocusAt = Date.now(); showSymPadFor(this); });
    inp.addEventListener('blur', function () {
      if (committing) return;
      commitValue(this.value);
    });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.keyCode === 13) {
        e.preventDefault();
        wantFocusAt = Date.now();
        if (commitTimer) { win.clearTimeout(commitTimer); commitTimer = 0; }
        commitValue(this.value);
        win.setTimeout(clickCheck, 140);
      }
    });
    inp.addEventListener('mousedown', function (e) { e.stopPropagation(); });
    inp.addEventListener('click', function (e) { e.stopPropagation(); });
  }

  /* ===== الخطوات المبسّطة: الطالب يعوّض في كل خطوة ===== */
  var MSUB = { '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4', '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9' };

  function normAns(v, cs) {
    var t = String(v == null ? '' : v), out = '';
    for (var i = 0; i < t.length; i++) {
      var ch = t.charAt(i);
      if (MSUB[ch]) { out += MSUB[ch]; continue; }
      if (ch === ' ' || ch === '\u00A0' || ch === '_' || ch === '*' || ch === '\u00B7' || ch === '\u00D7' || ch === '{' || ch === '}') { continue; }
      out += ch;
    }
    if (!cs) { out = out.toLowerCase(); }
    return out;
  }

  function commKeyAns(v, cs) {
    var t = normAns(v, cs);
    if (/[\u0600-\u06FF]/.test(t)) { return t; }
    var sides = t.split('='), out = [], i, j;
    for (i = 0; i < sides.length; i++) {
      var sd = sides[i];
      if (sd.length > 14 || sd.indexOf('/') >= 0 || sd.indexOf('-') >= 0) { out.push(sd); continue; }
      var terms = sd.split('+');
      for (j = 0; j < terms.length; j++) {
        var fs = terms[j].split('*'), k2;
        for (k2 = fs.length - 1; k2 >= 0; k2--) { if (!fs[k2]) { fs.splice(k2, 1); } }
        if (fs.length === 1 && !/[0-9]/.test(fs[0])) { terms[j] = fs[0].split('').sort().join(''); }
        else { terms[j] = fs.sort().join('*'); }
      }
      terms.sort();
      out.push(terms.join('+'));
    }
    out.sort();
    return out.join('=');
  }

  function fracVal(t) {
    var m = /^(-?[0-9]+(?:\.[0-9]+)?)\/(-?[0-9]+(?:\.[0-9]+)?)$/.exec(t);
    if (m) { var d = parseFloat(m[2]); return (d === 0) ? null : (parseFloat(m[1]) / d); }
    if (/^-?[0-9]+(?:\.[0-9]+)?$/.test(t)) { return parseFloat(t); }
    return null;
  }

  function sameAns(a, b, cs) {
    var x = normAns(a, cs), y = normAns(b, cs);
    if (x === y) { return true; }
    if (commKeyAns(a, cs) === commKeyAns(b, cs)) { return true; }
    var fx = fracVal(x), fy = fracVal(y);
    if (fx !== null && fy !== null) { return Math.abs(fx - fy) < 0.005; }
    return false;
  }

  var legacyPurged = false;
  function purgeLegacy() {
    if (legacyPurged) { return; }
    legacyPurged = true;
    try {
      var ks = [], li;
      for (li = 0; li < win.sessionStorage.length; li++) {
        var lk = win.sessionStorage.key(li);
        if (lk && lk.indexOf('physMicro:') === 0) { ks.push(lk); }
      }
      for (li = 0; li < ks.length; li++) { win.sessionStorage.removeItem(ks[li]); }
    } catch (e) { }
  }

  function microKey(line) {
    var pk = line.getAttribute ? line.getAttribute('data-pk') : null;
    if (pk) { return 'physMicro2:' + pk; }
    var card = line.closest('[class*="_stepstate_"]');
    var base = card ? String(card.className || '') : 'x';
    var idx = 0, kids = line.parentElement ? line.parentElement.children : [];
    for (var i = 0; i < kids.length; i++) { if (kids[i] === line) { idx = i; break; } }
    var bx = line.parentElement;
    var mk = (bx && bx.getAttribute) ? (bx.getAttribute('data-mk') || 'm') : 'm';
    var sig = String(line.dataset.ans || '') + '|' + String(line.dataset.cs || '');
    var hh = 0;
    for (var q = 0; q < sig.length; q++) { hh = ((hh << 5) - hh + sig.charCodeAt(q)) | 0; }
    return 'physMicro2:' + base.replace(/\s+/g, '_') + ':' + mk + ':' + idx + ':' + (hh >>> 0).toString(36);
  }

  function loadDone(line) {
    try { return win.sessionStorage.getItem(microKey(line)); } catch (e) { return null; }
  }

  function saveDone(line, v) {
    try { win.sessionStorage.setItem(microKey(line), v); } catch (e) { }
  }

  function markPractice(line, ok, val, silent) {
    var eqw = line.querySelector('.micro-eq');
    var slot = line.querySelector('.eq-slot');
    if (!ok) {
      if (eqw) {
        eqw.classList.remove('mi-ok');
        eqw.classList.add('mi-bad');
        win.setTimeout(function () { eqw.classList.remove('mi-bad'); }, 700);
      }
      return;
    }
    line.dataset.done = '1';
    if (slot) {
      var old = slot.querySelector('input.phys-slot-input');
      if (old && old.parentNode) { old.parentNode.removeChild(old); }
      var chip = slot.querySelector('.eq-unk');
      if (chip) { chip.style.display = ''; chip.textContent = val; }
      slot.classList.add('eq-filled');
    }
    if (eqw) { eqw.classList.remove('mi-bad'); eqw.classList.add('mi-ok'); }
    var say = line.querySelector('.micro-say');
    if (say && !say.querySelector('.micro-tag')) {
      var tag = doc.createElement('span');
      tag.className = 'micro-tag';
      tag.textContent = '\u2714';
      say.appendChild(tag);
    }
    saveDone(line, val);
    if (silent) { return; }
    var nxt = line.nextElementSibling;
    while (nxt) {
      var ni = nxt.querySelector ? nxt.querySelector('input.phys-slot-input') : null;
      if (ni) { wantFocusAt = Date.now(); try { ni.focus(); ni.select(); } catch (e2) { } return; }
      nxt = nxt.nextElementSibling;
    }
  }

  function tryPractice(inp, line) {
    var val = String(inp.value || '').trim();
    if (!val || line.dataset.done === '1') { return; }
    var cs = line.dataset.cs === '1';
    var wants = String(line.dataset.ans || '').split('|');
    for (var i = 0; i < wants.length; i++) {
      if (sameAns(val, wants[i], cs)) { markPractice(line, true, val); return; }
    }
    var tries = parseInt(line.dataset.tries || '0', 10) + 1;
    line.dataset.tries = String(tries);
    markPractice(line, false, val);
    if (tries >= 3) {
      markPractice(line, true, wants[0]);
      var eqw = line.querySelector('.micro-eq');
      if (eqw) { eqw.classList.remove('mi-ok'); eqw.classList.add('mi-shown'); }
    }
  }

  function wirePracticeInput(inp, line) {
    inp.addEventListener('input', function () { autoSize(this); });
    inp.addEventListener('focus', function () { wantFocusAt = Date.now(); showSymPadFor(this); });
    inp.addEventListener('blur', function () { tryPractice(this, line); });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.keyCode === 13) {
        e.preventDefault();
        e.stopPropagation();
        wantFocusAt = Date.now();
        tryPractice(this, line);
      }
    });
    inp.addEventListener('mousedown', function (e) { e.stopPropagation(); });
    inp.addEventListener('click', function (e) { e.stopPropagation(); });
  }

  var SYM_LIST = ['Δ', 'ΔP', 'Δt', 'θ', 'π', '×', '÷', '√', '²', '³', '≈', '±', '→', '←', '°', 'm/s', 'm/s²', 'kg', 'N', 'N·s', 'kg·m/s', 'J', '−', '⌫'];
  var symPadEl = null, symPadTarget = null;
  function insertSym(sym) {
    var el = symPadTarget;
    if (!el || !el.parentNode) { return; }
    var a = el.value.length, b = el.value.length;
    try { if (el.selectionStart !== null && el.selectionStart !== undefined) { a = el.selectionStart; b = el.selectionEnd; } } catch (e1) { }
    if (sym === '⌫') {
      var p = (a === b && a > 0) ? a - 1 : a;
      el.value = el.value.slice(0, p) + el.value.slice(b);
      try { el.setSelectionRange(p, p); } catch (e2) { }
    } else {
      el.value = el.value.slice(0, a) + sym + el.value.slice(b);
      var c = a + sym.length;
      try { el.setSelectionRange(c, c); } catch (e3) { }
    }
    try { el.dispatchEvent(new Event('input', { bubbles: true })); } catch (e4) { }
    try { el.focus(); } catch (e5) { }
  }
  function ensureSymPad() {
    if (symPadEl && symPadEl.parentNode) { return symPadEl; }
    var pad = doc.createElement('div');
    pad.id = 'phys-sym-pad';
    pad.setAttribute('dir', 'rtl');
    pad.style.cssText = 'position:fixed;z-index:99999;bottom:14px;right:14px;max-width:min(94vw,520px);padding:8px 10px;border:1px solid #cbd5e1;border-radius:14px;background:#f8fafc;box-shadow:0 10px 26px rgba(15,23,42,.2);display:none;text-align:right';
    var head = doc.createElement('div');
    head.style.cssText = 'display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:.85rem;color:#334155;margin-bottom:6px';
    var ttl = doc.createElement('span');
    ttl.textContent = '🔤 مكتبة الرموز';
    var cls = doc.createElement('button');
    cls.type = 'button';
    cls.textContent = '✕';
    cls.style.cssText = 'border:none;background:transparent;font-size:1rem;cursor:pointer;color:#64748b';
    cls.addEventListener('click', function (e) { e.preventDefault(); pad.style.display = 'none'; });
    head.appendChild(ttl); head.appendChild(cls);
    pad.appendChild(head);
    var row = doc.createElement('div');
    row.style.cssText = 'display:flex;flex-wrap:wrap;gap:6px';
    for (var i = 0; i < SYM_LIST.length; i++) {
      (function (sym) {
        var b = doc.createElement('button');
        b.type = 'button';
        b.textContent = sym;
        b.style.cssText = 'min-width:40px;padding:5px 9px;border:1px solid #cbd5e1;border-radius:10px;background:#fff;font-size:1rem;font-weight:700;color:#0f172a;cursor:pointer';
        b.addEventListener('mousedown', function (e) { e.preventDefault(); e.stopPropagation(); });
        b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); insertSym(sym); });
        row.appendChild(b);
      })(SYM_LIST[i]);
    }
    pad.appendChild(row);
    doc.body.appendChild(pad);
    symPadEl = pad;
    return pad;
  }
  function showSymPadFor(inp) {
    symPadTarget = inp;
    ensureSymPad().style.display = 'block';
  }

  function wireMicroSlots() {
    purgeLegacy();
    var lines = doc.querySelectorAll('.micro-line[data-ans]');
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      if (line.closest('#' + CLONE_ID)) { continue; }
      var slot = line.querySelector('.eq-slot');
      if (!slot) { continue; }
      if (line.dataset.done === '1') {
        var chipD = slot.querySelector('.eq-unk');
        var txD = chipD ? String(chipD.textContent || '').trim() : '';
        if (txD === '' || txD === '?') {
          line.dataset.done = '';
          line.dataset.tries = '0';
          slot.classList.remove('eq-filled');
          var tgD = line.querySelector('.micro-tag');
          if (tgD && tgD.parentNode) { tgD.parentNode.removeChild(tgD); }
          try { win.sessionStorage.removeItem(microKey(line)); } catch (eR) { }
        } else { continue; }
      }
      var saved = loadDone(line);
      if (saved !== null) {
        var okSaved = false;
        var csS = line.dataset.cs === '1';
        var wantsS = String(line.dataset.ans || '').split('|');
        for (var ws = 0; ws < wantsS.length; ws++) {
          if (sameAns(saved, wantsS[ws], csS)) { okSaved = true; break; }
        }
        if (okSaved) { markPractice(line, true, saved, true); continue; }
        try { win.sessionStorage.removeItem(microKey(line)); } catch (eS) { }
      }
      if (slot.querySelector('input.phys-slot-input')) { continue; }
      var chip = slot.querySelector('.eq-unk');
      if (chip) { chip.style.display = 'none'; }
      var inp = doc.createElement('input');
      inp.type = 'text';
      inp.className = 'phys-slot-input';
      inp.placeholder = '?';
      inp.setAttribute('autocomplete', 'off');
      inp.setAttribute('spellcheck', 'false');
      slot.appendChild(inp);
      wirePracticeInput(inp, line);
      autoSize(inp);
      if (slot.dataset.physSlot !== '1') {
        slot.dataset.physSlot = '1';
        slot.addEventListener('click', function () {
          var t = this.querySelector('input.phys-slot-input');
          if (t) { t.focus(); t.select(); }
        });
      }
    }
  }

  function wireEqInputs() {
    var rows = doc.querySelectorAll('.st-key-formula_proof_row');
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      var real = row.querySelector('input');
      if (!real) continue;

      var card = row.closest('[class*="_stepstate_active"]') || row.closest('div[data-testid="stColumn"]');
      if (!card) continue;
      var box = card.querySelector('.eq-box');
      if (!box) continue;
      var slot = box.querySelector('.eq-slot');
      if (!slot) continue;

      var inp = slot.querySelector('input.phys-slot-input');
      if (!inp) {
        var chip = slot.querySelector('.eq-unk');
        if (chip) { chip.style.display = 'none'; }
        inp = doc.createElement('input');
        inp.type = 'text';
        inp.className = 'phys-slot-input';
        inp.placeholder = '?';
        inp.setAttribute('autocomplete', 'off');
        inp.setAttribute('spellcheck', 'false');
        inp.title = '\u0623\u062F\u062E\u0644 \u0627\u0644\u0642\u064A\u0645\u0629 \u0647\u0646\u0627 \u062B\u0645 \u0627\u0636\u063A\u0637 Enter';
        slot.appendChild(inp);
        inp.classList.add('phys-final-input');
        wireSlotInput(inp);
        inp.value = real.value || '';
        autoSize(inp);
      } else if (doc.activeElement !== inp && inp.value !== (real.value || '')) {
        inp.value = real.value || '';
        autoSize(inp);
      }

      /* طيّ صف الإدخال القديم دون حذفه: يبقى موجوداً وقابلاً للتركيز حتى يعمل التحقق */
      css(row, {
        'height': '0px',
        'min-height': '0px',
        'max-height': '0px',
        'margin': '0px',
        'padding': '0px',
        'border': 'none',
        'overflow': 'hidden',
        'opacity': '0',
        'pointer-events': 'none'
      });

      /* تلميح صغير أسفل المعادلة */
      var holder = box.parentElement;
      if (holder && !holder.querySelector('.eq-hint')) {
        var hint = doc.createElement('div');
        hint.className = 'eq-hint';
        hint.textContent = '\u270D\uFE0F \u0627\u0643\u062A\u0628 \u0627\u0644\u0642\u064A\u0645\u0629 \u062F\u0627\u062E\u0644 \u0627\u0644\u062E\u0627\u0646\u0629 \u0627\u0644\u062D\u0645\u0631\u0627\u0621 \u062B\u0645 \u0627\u0636\u063A\u0637 Enter \u0623\u0648 \u0632\u0631 \u062A\u062D\u0642\u0642';
        holder.appendChild(hint);
      }

      /* إعادة التركيز بعد إعادة الرسم إن كان الطالب يكتب */
      if (wantFocusAt && Date.now() - wantFocusAt < 6000) {
        var ae = doc.activeElement;
        if (!ae || ae === doc.body || (ae.tagName && ae.tagName.toUpperCase() === 'BODY')) {
          try { inp.focus(); } catch (e3) { }
        }
      }

      /* النقر على مكان علامة الاستفهام يفتح الكتابة */
      if (slot.dataset.physSlot !== '1') {
        slot.dataset.physSlot = '1';
        slot.addEventListener('click', function () {
          var t = this.querySelector('input.phys-slot-input');
          if (t) { t.focus(); t.select(); }
        });
      }
    }
  }

  /* ================= \u0644\u0648\u062d\u0629 \u0627\u0644\u0623\u064a\u0642\u0648\u0646\u062a\u064a\u0646: \u0627\u0644\u0642\u0648\u0627\u0646\u064a\u0646 \u0627\u0644\u0633\u0631\u064a\u0639\u0629 / \u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646 ================= */
  var DOCK_ID = 'phys-dock';
  var dockSt = null;

  function dockRead() {
    if (dockSt) return dockSt;
    var v = 'stmt';
    try { v = win.sessionStorage.getItem('physDockPane') || 'stmt'; } catch (e) { v = 'stmt'; }
    if (v !== 'laws' && v !== 'stmt' && v !== 'calc' && v !== 'none') v = 'stmt';
    dockSt = v;
    return v;
  }

  function dockWrite(v) {
    dockSt = v;
    try { win.sessionStorage.setItem('physDockPane', v); } catch (e) {}
  }

  /* \u0645\u0633\u062a\u0648\u0649 \u0627\u0644\u0628\u062f\u0627\u064a\u0629: \u0639\u0646\u0648\u0627\u0646 \u0645\u0631\u0627\u062d\u0644 \u0627\u0644\u062a\u0639\u0648\u064a\u0636 / \u062e\u0637\u0648\u0627\u062a \u0627\u0644\u0625\u062b\u0628\u0627\u062a */
  function anchorEl() {
    var a = doc.getElementById('phys-steps-anchor');
    if (a) return a;
    var hs = doc.querySelectorAll('h1, h2, h3');
    for (var i = 0; i < hs.length; i++) {
      var t = hs[i].textContent || '';
      if (t.indexOf('\u0645\u0631\u0627\u062d\u0644 \u0627\u0644\u062a\u0639\u0648\u064a\u0636') >= 0 || t.indexOf('\u062e\u0637\u0648\u0627\u062a \u0627\u0644\u0625\u062b\u0628\u0627\u062a') >= 0) return hs[i];
    }
    return null;
  }

  function calcHtml() {
    var keys = [
      ['C', 'c'], ['\u232b', 'back'], ['(', '('], [')', ')'],
      ['7', '7'], ['8', '8'], ['9', '9'], ['\u00f7', '/'],
      ['4', '4'], ['5', '5'], ['6', '6'], ['\u00d7', '*'],
      ['1', '1'], ['2', '2'], ['3', '3'], ['-', '-'],
      ['0', '0'], ['.', '.'], ['\u221a', 'sqrt'], ['+', '+'],
      ['x\u00b2', 'sq'], ['=', 'eq']
    ];
    var h = '<div class="phys-calc" data-expr="">' +
      '<div class="phys-calc-disp">' +
        '<div class="phys-calc-expr">0</div>' +
        '<div class="phys-calc-val">0</div>' +
      '</div><div class="phys-calc-pad">';
    for (var i = 0; i < keys.length; i++) {
      var cls = 'phys-calc-key';
      if (keys[i][1] === 'eq') cls += ' k-eq';
      if (keys[i][1] === 'c' || keys[i][1] === 'back') cls += ' k-fn';
      h += '<button type="button" class="' + cls + '" data-k="' + keys[i][1] + '">' + keys[i][0] + '</button>';
    }
    return h + '</div></div>';
  }

  function calcPretty(e) {
    return String(e || '')
      .replace(/Math\.sqrt\(/g, '\u221a(')
      .replace(/\*\*2/g, '\u00b2')
      .replace(/\*/g, '\u00d7')
      .replace(/\//g, '\u00f7');
  }

  function calcEval(e) {
    var src = String(e || '');
    if (!src) return '';
    if (!/^[0-9+\-*/(). ]*$/.test(src.replace(/Math\.sqrt/g, ''))) return '';
    try {
      var v = (new win.Function('return (' + src + ')'))();
      if (typeof v !== 'number' || !isFinite(v)) return '';
      return String(Math.round(v * 1000000) / 1000000);
    } catch (err) { return ''; }
  }

  function calcPaint(d) {
    var pane = d.querySelector('.phys-calc');
    if (!pane) return;
    var e = pane.getAttribute('data-expr') || '';
    var ex = pane.querySelector('.phys-calc-expr');
    var vl = pane.querySelector('.phys-calc-val');
    if (ex) ex.textContent = calcPretty(e) || '0';
    if (vl) {
      var v = calcEval(e);
      vl.textContent = (e === '') ? '0' : (v === '' ? '\u2026' : v);
    }
  }

  function calcKey(d, k) {
    var pane = d.querySelector('.phys-calc');
    if (!pane) return;
    var e = pane.getAttribute('data-expr') || '';
    if (k === 'c') { e = ''; }
    else if (k === 'back') {
      if (/Math\.sqrt\($/.test(e)) e = e.slice(0, -10);
      else if (/\*\*2$/.test(e)) e = e.slice(0, -3);
      else e = e.slice(0, -1);
    }
    else if (k === 'sqrt' || k === 'sq') {
      var base = (e === '') ? (pane.getAttribute('data-last') || '') : calcEval(e);
      var bv = parseFloat(base);
      if (base !== '' && !isNaN(bv)) {
        var out = (k === 'sqrt') ? Math.sqrt(bv) : (bv * bv);
        if (isFinite(out)) {
          e = String(Math.round(out * 1000000) / 1000000);
          pane.setAttribute('data-last', e);
        }
      } else {
        e += (k === 'sqrt') ? 'Math.sqrt(' : '**2';
      }
    }
    else if (k === 'eq') {
      var v = calcEval(e);
      if (v !== '') { e = v; pane.setAttribute('data-last', v); }
    }
    else { e += k; }
    pane.setAttribute('data-expr', e);
    calcPaint(d);
  }

  function paneHtml(kind) {
    if (kind === 'calc') {
      return '<div class="phys-pane-head">\ud83e\uddee \u0622\u0644\u0629 \u062d\u0627\u0633\u0628\u0629</div>' + calcHtml();
    }
    var s = doc.getElementById(kind === 'laws' ? 'phys-src-laws' : 'phys-src-stmt');
    var inner = s ? s.innerHTML : '';
    var ttl = (kind === 'laws') ? '\ud83d\udcd0 \u0648\u0631\u0642\u0629 \u0627\u0644\u0642\u0648\u0627\u0646\u064a\u0646 \u0627\u0644\u0633\u0631\u064a\u0639\u0629' : '\ud83d\udcc4 \u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646';
    return '<div class="phys-pane-head">' + ttl + '</div>' + inner;
  }

  function dockBuild() {
    var d = doc.getElementById(DOCK_ID);
    if (d) return d;
    d = doc.createElement('div');
    d.id = DOCK_ID;
    d.innerHTML =
      '<div class="phys-pane"><div class="phys-pane-in"></div></div>' +
      '<div class="phys-rail">' +
        '<div class="phys-ic-wrap" data-kind="laws" title="\u0648\u0631\u0642\u0629 \u0627\u0644\u0642\u0648\u0627\u0646\u064a\u0646 \u0627\u0644\u0633\u0631\u064a\u0639\u0629">' +
          '<button type="button" class="phys-ic phys-ic-laws">\ud83d\udcd0</button>' +
          '<span class="phys-ic-lbl lbl-laws">\u0648\u0631\u0642\u0629 \u0627\u0644\u0642\u0648\u0627\u0646\u064a\u0646 \u0627\u0644\u0633\u0631\u064a\u0639\u0629</span>' +
        '</div>' +
        '<div class="phys-ic-wrap" data-kind="stmt" title="\u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646">' +
          '<button type="button" class="phys-ic phys-ic-stmt">\ud83d\udcc4</button>' +
          '<span class="phys-ic-lbl lbl-stmt">\u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646</span>' +
        '</div>' +
        '<div class="phys-ic-wrap" data-kind="calc" title="\u0622\u0644\u0629 \u062d\u0627\u0633\u0628\u0629">' +
          '<button type="button" class="phys-ic phys-ic-calc">\ud83e\uddee</button>' +
          '<span class="phys-ic-lbl lbl-calc">\u0622\u0644\u0629 \u062d\u0627\u0633\u0628\u0629</span>' +
        '</div>' +
      '</div>';
    doc.body.appendChild(d);
    var wraps = d.querySelectorAll('.phys-ic-wrap'), wi;
    for (wi = 0; wi < wraps.length; wi++) {
      (function (el) {
        el.addEventListener('click', function (e) {
          e.preventDefault(); e.stopPropagation();
          dockToggle(el.getAttribute('data-kind'));
        });
      })(wraps[wi]);
    }
    d.addEventListener('click', function (e) {
      var t = e.target;
      var b = (t && t.closest) ? t.closest('.phys-calc-key') : null;
      if (!b) return;
      e.preventDefault(); e.stopPropagation();
      calcKey(d, b.getAttribute('data-k'));
    });
    var cur = dockRead();
    if (cur !== 'none') {
      var pane = d.querySelector('.phys-pane');
      var box = d.querySelector('.phys-pane-in');
      var h = paneHtml(cur);
      box.dataset.sig = h;
      box.innerHTML = h;
      pane.dataset.open = '1';
      pane.style.display = 'block';
    }
    return d;
  }

  function dockIcons() {
    var d = doc.getElementById(DOCK_ID);
    if (!d) return;
    var cur = dockRead();
    var a = d.querySelector('.phys-ic-laws');
    var b = d.querySelector('.phys-ic-stmt');
    var c = d.querySelector('.phys-ic-calc');
    if (a) a.className = 'phys-ic phys-ic-laws' + (cur === 'laws' ? ' on' : '');
    if (b) b.className = 'phys-ic phys-ic-stmt' + (cur === 'stmt' ? ' on' : '');
    if (c) c.className = 'phys-ic phys-ic-calc' + (cur === 'calc' ? ' on' : '');
    var wl = d.querySelector('.phys-ic-wrap[data-kind="laws"]');
    var ws = d.querySelector('.phys-ic-wrap[data-kind="stmt"]');
    var wc = d.querySelector('.phys-ic-wrap[data-kind="calc"]');
    if (wl) wl.className = 'phys-ic-wrap' + (cur === 'laws' ? ' on' : '');
    if (ws) ws.className = 'phys-ic-wrap' + (cur === 'stmt' ? ' on' : '');
    if (wc) wc.className = 'phys-ic-wrap' + (cur === 'calc' ? ' on' : '');
  }

  function paneFill(kind) {
    var d = dockBuild();
    var box = d.querySelector('.phys-pane-in');
    var h = paneHtml(kind);
    box.dataset.sig = h;
    box.innerHTML = h;
  }

  /* \u0627\u0644\u0645\u0639\u0631\u0648\u0636 \u062d\u0627\u0644\u064a\u0627\u064b \u064a\u0646\u0633\u062d\u0628 \u0644\u0644\u0623\u0633\u0641\u0644 \u062b\u0645 \u064a\u062d\u0644 \u0645\u062d\u0644\u0647 \u0627\u0644\u0645\u0637\u0644\u0648\u0628 */
  function dockShow(kind) {
    var d = dockBuild();
    var pane = d.querySelector('.phys-pane');
    if (pane.dataset.open === '1') {
      pane.classList.add('pane-out');
      win.setTimeout(function () {
        paneFill(kind);
        pane.classList.remove('pane-out');
        pane.classList.add('pane-start');
        positionDock();
        win.setTimeout(function () { pane.classList.remove('pane-start'); }, 30);
      }, 200);
    } else {
      paneFill(kind);
      pane.style.display = 'block';
      pane.classList.add('pane-start');
      positionDock();
      win.setTimeout(function () { pane.classList.remove('pane-start'); }, 30);
    }
    pane.dataset.open = '1';
  }

  function dockHide() {
    var d = dockBuild();
    var pane = d.querySelector('.phys-pane');
    pane.dataset.open = '0';
    pane.classList.add('pane-out');
    win.setTimeout(function () {
      if (pane.dataset.open === '0') {
        pane.style.display = 'none';
        pane.classList.remove('pane-out');
      }
      positionDock();
    }, 200);
  }

  function dockToggle(kind) {
    var cur = dockRead();
    if (cur === kind) { dockWrite('none'); dockHide(); }
    else { dockWrite(kind); dockShow(kind); }
    dockIcons();
    positionDock();
  }

  function dockSync() {
    var cur = dockRead();
    if (cur !== 'laws' && cur !== 'stmt') return;
    var d = doc.getElementById(DOCK_ID);
    if (!d) return;
    var pane = d.querySelector('.phys-pane');
    if (pane.dataset.open !== '1') return;
    var box = d.querySelector('.phys-pane-in');
    var h = paneHtml(cur);
    if (box.dataset.sig !== h) { box.dataset.sig = h; box.innerHTML = h; }
  }

  function positionDock() {
    var d = dockBuild();
    var pane = d.querySelector('.phys-pane');
    var cur = dockRead();
    var open = (cur !== 'none');
    var vw = win.innerWidth || doc.documentElement.clientWidth || 1280;
    var vh = win.innerHeight || doc.documentElement.clientHeight || 800;
    var off = topOffset();
    var an = anchorEl();

    if (!an) { d.style.display = 'none'; setReserve(0); return; }
    d.style.display = 'flex';

    var ar = an.getBoundingClientRect();
    var top = Math.max(off, Math.round(ar.top));

    var railW = 96;
    var w = 0;
    if (open) {
      w = Math.max(320, Math.min(430, Math.round(vw * 0.31)));
      if (w > vw - railW - 40) w = Math.max(200, Math.round(vw - railW - 40));
    }

    /* \u062d\u062c\u0632 \u0645\u0633\u0627\u062d\u0629 \u062d\u0642\u064a\u0642\u064a\u0629 \u062d\u062a\u0649 \u0644\u0627 \u062a\u063a\u0637\u064a \u0627\u0644\u0644\u0648\u062d\u0629 \u0627\u0644\u062e\u0637\u0648\u0627\u062a */
    var curRes = reserveNow();
    if (curRes === 0 || natRight === null) { natRight = ar.right; }
    var baseRight = (curRes === 0) ? ar.right : natRight;
    var need = railW + (open ? w + 10 : 0) + 24;
    var gap = vw - baseRight;
    var resChanged = setReserve(Math.max(0, Math.round(need - gap)));
    if (resChanged) { try { layoutFormulaRows(); layoutSteps(); } catch (e) {} }

    var total = railW + (open ? w + 10 : 0);
    d.style.top = top + 'px';
    d.style.left = Math.round(vw - 12 - total) + 'px';
    d.style.width = total + 'px';

    if (open) {
      pane.style.width = w + 'px';
      pane.style.maxHeight = Math.max(160, Math.round(vh - top - 18)) + 'px';
    }
  }

  function update() {
    fixSubscripts();
    fixLatex();
    layoutFormulaRows();
    layoutSteps();
    installCommitGuard();
    wireEqInputs();
    wireMicroSlots();
    dockBuild();
    dockSync();
    dockIcons();
    positionDock();
  }

  /* أي تمرير داخل أي حاوية (مرحلة الالتقاط) */
  doc.addEventListener('scroll', update, { capture: true, passive: true });
  win.addEventListener('scroll', update, { passive: true });
  win.addEventListener('resize', function () {
    natRight = null;
    setReserve(0);
    update();
  });

  update();
  setTimeout(update, 250);
  setTimeout(update, 900);

  var t = null;
  new MutationObserver(function () {
    clearTimeout(t);
    t = setTimeout(update, 100);
  }).observe(doc.body, { childList: true, subtree: true });
})();
</script>
""",
    height=0,
)


# FINAL_UI_V18_EXERCISE_THEME
apply_ui_theme("exercise")
apply_exercise_ui_v18()
render_exercise_footer_v18("pages/physics_textbook_exercises.py")
