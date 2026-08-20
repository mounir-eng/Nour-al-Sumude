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
APP_UNIT     = "الكيمياء · الصف الثاني عشر · تمارين الكتاب المدرسي — الوحدة الأولى"
TEXTBOOK_PAGE_VERSION = "book-unit1-platform-integrated-v10"

# ==========================================================
# 1. إعدادات الصفحة
# ==========================================================
st.set_page_config(
    page_title=APP_NAME + " — تمارين الكتاب المدرسي",
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

    .phys-calc { direction: ltr; font-family: "Segoe UI", Arial, sans-serif; }
    .phys-calc-top {
        display:flex; align-items:center; justify-content:space-between; gap:8px;
        margin:0 0 8px; direction:ltr;
    }
    .phys-calc-badge {
        background:#eef2ff; color:#3730a3; border:1px solid #c7d2fe;
        border-radius:999px; padding:4px 9px; font-size:.72rem; font-weight:900;
    }
    .phys-calc-mode-note { color:#64748b; font-size:.7rem; font-weight:700; }
    .phys-calc-disp {
        background: linear-gradient(145deg,#0f172a,#1e293b); color:#ffffff; border-radius:14px;
        padding:10px 12px; margin-bottom:9px; text-align:right; min-height:74px;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.05);
    }
    .phys-calc-expr { font-size:.82rem; color:#94a3b8; min-height:20px; word-break:break-all; }
    .phys-calc-val { font-size:1.55rem; font-weight:900; word-break:break-all; direction:ltr; }
    .phys-calc-history {
        max-height:68px; overflow:auto; margin:0 0 8px; padding:0 2px;
        color:#64748b; font-size:.68rem; direction:ltr; text-align:right;
    }
    .phys-calc-history div { border-bottom:1px dashed #e2e8f0; padding:3px 1px; }
    .phys-calc-pad { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:6px; }
    .phys-calc-key {
        border:1px solid #e2e8f0; background:#f8fafc; color:#0f172a;
        border-radius:9px; padding:9px 2px; min-height:39px; font-size:.83rem; font-weight:850;
        cursor:pointer; transition:background .12s ease,transform .12s ease,border-color .12s ease;
        direction:ltr; text-align:center;
    }
    .phys-calc-key:hover { background:#e2e8f0; transform:translateY(-1px); }
    .phys-calc-key.k-sci { background:#eef2ff; border-color:#c7d2fe; color:#3730a3; }
    .phys-calc-key.k-op { background:#fff7ed; border-color:#fed7aa; color:#9a3412; }
    .phys-calc-key.k-fn { background:#fee2e2; border-color:#fecaca; color:#991b1b; }
    .phys-calc-key.k-mode { background:#ecfeff; border-color:#a5f3fc; color:#155e75; }
    .phys-calc-key.k-eq { border:none; color:#fff; background:linear-gradient(135deg,#2563eb,#60a5fa); }
    .phys-calc-help {
        margin-top:8px; color:#64748b; font-size:.68rem; line-height:1.6;
        text-align:center; direction:rtl;
    }
    @media (max-width:720px) {
        .phys-calc-pad { gap:4px; }
        .phys-calc-key { min-height:36px; padding:7px 1px; font-size:.72rem; }
        .phys-calc-val { font-size:1.25rem; }
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


    /* ===== النسخة النهائية: لوحة أدوات جانبية بثلاث أيقونات ===== */
    #phys-dock {
        z-index: 2147483000 !important;
        gap: 12px !important;
        filter: drop-shadow(0 8px 18px rgba(15, 23, 42, .08));
    }
    #phys-dock .phys-rail {
        width: 88px !important;
        gap: 12px !important;
        padding-top: 2px;
    }
    #phys-dock .phys-ic-wrap { gap: 4px !important; user-select: none; }
    #phys-dock .phys-ic {
        width: 56px !important;
        height: 56px !important;
        min-height: 56px !important;
        border: 3px solid #fff !important;
        box-shadow: 0 7px 18px rgba(15,23,42,.28), 0 0 0 1px rgba(15,23,42,.08) !important;
    }
    #phys-dock .phys-ic-lbl {
        max-width: 88px !important;
        padding: 4px 7px !important;
        border-radius: 8px !important;
        background: rgba(255,255,255,.98) !important;
        color: #334155 !important;
        font-size: .64rem !important;
        font-weight: 900 !important;
        line-height: 1.35 !important;
        box-shadow: 0 4px 10px rgba(15,23,42,.11) !important;
    }
    #phys-dock .phys-pane {
        border: 1px solid #dbe4ef !important;
        border-radius: 18px !important;
        background: rgba(255,255,255,.985) !important;
        box-shadow: 0 22px 48px rgba(15,23,42,.18) !important;
        padding: 16px 16px 17px !important;
    }
    #phys-dock .phys-pane-head {
        color: #0f172a !important;
        font-size: 1.03rem !important;
        font-weight: 900 !important;
        border-bottom: 2px solid #dbeafe !important;
        padding: 0 1px 10px !important;
        margin-bottom: 12px !important;
    }
    #phys-dock .phys-pane .sb-chip {
        display: inline-flex !important;
        align-items: center;
        border-radius: 999px !important;
        padding: 5px 10px !important;
    }
    #phys-dock .phys-pane .qprogress-bg { height: 10px !important; }
    #phys-dock .phys-pane .formula-row {
        border: 1px solid #e2e8f0;
        border-right: 4px solid #f59e0b;
        border-radius: 11px;
        background: #fffdf7;
        padding: 9px 10px;
        margin-bottom: 8px !important;
    }
    #phys-dock .phys-pane .f-name {
        display: block;
        color: #92400e;
        font-size: .75rem;
        font-weight: 900;
        margin-bottom: 3px;
    }
    #phys-dock .phys-pane .f-eq {
        display: block;
        direction: ltr;
        unicode-bidi: isolate;
        text-align: center;
        color: #0f172a;
    }
    @media (max-width: 720px) {
        #phys-dock { gap: 7px !important; }
        #phys-dock .phys-rail { width: 76px !important; gap: 9px !important; }
        #phys-dock .phys-ic { width: 49px !important; height: 49px !important; min-height: 49px !important; }
        #phys-dock .phys-ic-lbl { max-width: 74px !important; font-size: .57rem !important; padding: 3px 4px !important; }
        #phys-dock .phys-pane { padding: 12px !important; border-radius: 14px !important; }
    }

    </style>
""", unsafe_allow_html=True)


# --- اتجاه المعادلات حسب نوع الرموز (عربي RTL / لاتيني LTR) ---
st.markdown("""
<style>
.eq.eq-rtl,
.law-eq.eq-flow-rtl,
.micro-eq.eq-flow-rtl,
.result-eq.eq-flow-rtl,
.eq-inline.eq-flow-rtl,
.formula-row .f-eq.eq-flow-rtl,
#phys-dock .phys-pane .f-eq.eq-flow-rtl {
    direction: rtl !important;
    unicode-bidi: isolate !important;
    text-align: right !important;
}
.eq.eq-ltr,
.law-eq.eq-flow-ltr,
.micro-eq.eq-flow-ltr,
.result-eq.eq-flow-ltr,
.eq-inline.eq-flow-ltr,
.formula-row .f-eq.eq-flow-ltr,
#phys-dock .phys-pane .f-eq.eq-flow-ltr {
    direction: ltr !important;
    unicode-bidi: isolate !important;
    text-align: left !important;
}
.eq.eq-rtl { font-family: "Noto Sans Arabic", Tahoma, "Cambria Math", serif; }
.eq.eq-ltr { font-family: "Cambria Math", "Times New Roman", Georgia, serif; }
.eq-fr, .eq-num, .eq-den, .eq-slot, .eq-op, .eq-eq {
    unicode-bidi: isolate;
}
.law-eq.eq-flow-rtl, .micro-eq.eq-flow-rtl, .result-eq.eq-flow-rtl {
    white-space: nowrap;
    overflow-x: auto;
    overflow-y: hidden;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. بنك الأسئلة (تمارين تفاعلية + مسائل إثبات نظرية)
# ==========================================================
questions_db = [{'id': 'tb1',
  'type': 'proof',
  'title': 'تمرين الكتاب (1) · استنتاج وحدة قياس التردد',
  'text': 'استخدم العلاقة س = ل × ت لإيجاد وحدة قياس التردد ت، حيث س بوحدة m/s ول بوحدة m.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: عزل التردد من العلاقة',
             'law': 'العلاقة الموجية: س = ل × ت',
             'latex_preview': 'ت = \\frac{س}{\\mathbf{?}}',
             'micro': [('اقسم طرفي العلاقة على الطول الموجي ل:', 'ت = س / ?', 'ل|lambda|λ')],
             'label': 'اكتب رمز المقام:',
             'prefix': 'ت = س / ',
             'suffix': '',
             'target': 'ل|lambda|λ',
             'completed_display': 'ت = س / ل',
             'hint': 'المقام هو الطول الموجي ل.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: اختصار الوحدات',
             'law': 'وحدة ت = (m/s) ÷ m',
             'latex_preview': '[ت] = \\mathbf{?}',
             'micro': [('اختصر المتر من البسط والمقام:', '(m/s) / m = ?', '1/s|s-1|Hz|هيرتز')],
             'label': 'اكتب الوحدة 1/s أو Hz:',
             'prefix': '[ت] = ',
             'suffix': '',
             'target': '1/s|s-1|Hz|هيرتز',
             'completed_display': 'وحدة التردد = s⁻¹ = Hz',
             'hint': 'بعد اختصار m تبقى 1/s، وتسمى هيرتز.'}],
  'conclusion': 'وحدة قياس التردد هي 1/s أو s⁻¹، وتسمى الهيرتز Hz.'},
 {'id': 'tb2',
  'type': 'interactive',
  'title': 'تمرين الكتاب (2) · طول موجة محطة راديو',
  'text': 'تذيع محطة راديو بتردد 95.2 MHz. احسب الطول الموجي للموجة التي تبثها. اعتبر س = 3 × 10⁸ m/s و1 MHz = 10⁶ '
          'Hz.',
  'steps': [{'num': 1,
             'title': 'الخطوة 1: التعويض في ل = س/ت',
             'micro': [('نحوّل التردد من MHz إلى Hz:', 'ت = 95.2 × 10⁶ Hz'),
                       ('نعزل الطول الموجي من س = ل×ت:', 'ل = س / ت'),
                       ('أكمل معامل سرعة الضوء:', 'س = ? × 10⁸ m/s', '3')],
             'law': 'ل = س / ت',
             'simple_explain': 'أدخل معامل سرعة الضوء 3، ثم التردد 95.2، واحسب الناتج بالمتر.',
             'prefix': 'ل = (',
             'blanks': [{'label': 'c', 'target': 3.0, 'suffix': '×10⁸)/('},
                        {'label': 'f', 'target': 95.2, 'suffix': '×10⁶)'}],
             'has_root': False,
             'result_target': 3.151,
             'result_tol': 0.02,
             'result_label': 'احسب الطول الموجي ل (m):',
             'hint': 'ل = (3×10⁸)/(95.2×10⁶) = 3.151 m.'}]},
 {'id': 'tb3',
  'type': 'proof',
  'title': 'تمرين الكتاب (3) · الطيف المتصل والمنفصل',
  'text': 'قارن بين الطيف المتصل والطيف المنفصل من حيث تتابع المناطق المضيئة، وأعط مثالًا لكل منهما.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: مناطق الطيف المتصل',
             'law': 'الطيف المتصل لا توجد بين ألوانه حدود فاصلة',
             'latex_preview': 'المناطق\\ المضيئة = \\mathbf{?}',
             'micro': [('ألوان الطيف تظهر متجاورة دون مناطق معتمة:', 'المناطق المضيئة ?', 'متتابعة|متصلة')],
             'label': 'أكمل الوصف:',
             'prefix': 'مناطق مضيئة ',
             'suffix': '',
             'target': 'متتابعة|متصلة',
             'completed_display': 'الطيف المتصل: مناطق مضيئة متتابعة دون حدود فاصلة',
             'hint': 'اكتب: متتابعة.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: مثال على الطيف المتصل',
             'law': 'من أمثلته ضوء الشمس ومصباح سلك التنجستون',
             'latex_preview': 'مثال = \\mathbf{?}',
             'micro': [('اختر مثالًا صحيحًا من الدرس:', 'مثال: ?', 'الشمس|الطيفالشمسي|مصباحالتنجستون|سلكالتنجستون')],
             'label': 'اكتب مثالًا:',
             'prefix': '',
             'suffix': '',
             'target': 'الشمس|الطيفالشمسي|مصباحالتنجستون|سلكالتنجستون',
             'completed_display': 'مثال: الطيف الشمسي أو طيف مصباح سلك التنجستون',
             'hint': 'اكتب الشمس أو مصباح التنجستون.'},
            {'num': 3,
             'type': 'symbol',
             'title': 'الخطوة 3: مناطق الطيف المنفصل',
             'law': 'الطيف المنفصل يتكون من خطوط ملونة تفصلها مناطق معتمة',
             'latex_preview': 'الخطوط = \\mathbf{?}',
             'micro': [('بين الخطوط الملونة توجد مناطق مظلمة:', 'الخطوط ?', 'منفصلة|غيرمتتابعة')],
             'label': 'أكمل الوصف:',
             'prefix': 'خطوط ملونة ',
             'suffix': '',
             'target': 'منفصلة|غيرمتتابعة',
             'completed_display': 'الطيف المنفصل: خطوط ملونة تفصلها مناطق معتمة',
             'hint': 'اكتب: منفصلة.'},
            {'num': 4,
             'type': 'symbol',
             'title': 'الخطوة 4: مثال على الطيف المنفصل',
             'law': 'من أمثلته طيف مصباح غاز الهيليوم',
             'latex_preview': 'مثال = \\mathbf{?}',
             'micro': [('اختر مثالًا غازيًا ورد في الدرس:', 'مثال: ?', 'الهيليوم|مصباحالهيليوم|غازالهيليوم')],
             'label': 'اكتب المثال:',
             'prefix': '',
             'suffix': '',
             'target': 'الهيليوم|مصباحالهيليوم|غازالهيليوم',
             'completed_display': 'مثال: طيف مصباح غاز الهيليوم',
             'hint': 'اكتب: الهيليوم.'}],
  'conclusion': 'المتصل مناطق مضيئة متتابعة مثل الطيف الشمسي؛ والمنفصل خطوط ملونة تفصلها مناطق معتمة مثل طيف '
                'الهيليوم.'},
 {'id': 'tb4',
  'type': 'proof',
  'title': 'تمرين الكتاب (4) · التمييز بين نترات البوتاسيوم والصوديوم',
  'text': 'كيف تساعد مزارعًا في التمييز بين ملح نترات البوتاسيوم وملح نترات الصوديوم؟',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: اختيار الاختبار',
             'law': 'تعطي أملاح العناصر ألوانًا مميزة عند تسخينها في اللهب',
             'latex_preview': 'الاختبار = \\mathbf{?}',
             'micro': [('نسخّن كمية قليلة من كل ملح على سلك نكروم نظيف:', 'نستخدم اختبار ?', 'اللهب|اختباراللهب')],
             'label': 'اكتب اسم الاختبار:',
             'prefix': 'اختبار ',
             'suffix': '',
             'target': 'اللهب|اختباراللهب',
             'completed_display': 'نستخدم اختبار اللهب بسلك نكروم',
             'hint': 'اكتب: اللهب.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: لون ملح البوتاسيوم',
             'law': 'تعطي أملاح البوتاسيوم لونًا بنفسجيًا',
             'latex_preview': 'K^+ \\rightarrow \\mathbf{?}',
             'micro': [('راقب لون اللهب بعد تسخين الملح الأول:', 'البوتاسيوم → ?', 'بنفسجي|البنفسجي')],
             'label': 'اكتب اللون:',
             'prefix': 'البوتاسيوم: ',
             'suffix': '',
             'target': 'بنفسجي|البنفسجي',
             'completed_display': 'إذا تلون اللهب بالبنفسجي فالملح نترات البوتاسيوم',
             'hint': 'لون البوتاسيوم بنفسجي.'},
            {'num': 3,
             'type': 'symbol',
             'title': 'الخطوة 3: لون ملح الصوديوم',
             'law': 'تعطي أملاح الصوديوم لونًا أصفر',
             'latex_preview': 'Na^+ \\rightarrow \\mathbf{?}',
             'micro': [('راقب لون اللهب للملح الآخر:', 'الصوديوم → ?', 'اصفر|أصفر|الاصفر|الأصفر')],
             'label': 'اكتب اللون:',
             'prefix': 'الصوديوم: ',
             'suffix': '',
             'target': 'اصفر|أصفر|الاصفر|الأصفر',
             'completed_display': 'إذا تلون اللهب بالأصفر فالملح نترات الصوديوم',
             'hint': 'لون الصوديوم أصفر.'}],
  'conclusion': 'نسخّن الملحين في اختبار اللهب: البنفسجي يدل على نترات البوتاسيوم، والأصفر يدل على نترات الصوديوم.'},
 {'id': 'tb5',
  'type': 'proof',
  'title': 'تمرين الكتاب (5) · طاقات مدارات الهيدروجين',
  'text': 'باستخدام معادلة بور، احسب طاقة إلكترون ذرة الهيدروجين في المدار الثاني والخامس وعند ن=∞، ثم رتبها واستنتج '
          'أثر زيادة ن.',
  'steps': [{'num': 1,
             'type': 'number',
             'title': 'الخطوة 1: طاقة المدار الثاني',
             'law': 'طₙ = −أ/ن²، و أ = 2.18×10⁻¹⁸ J',
             'latex_preview': 'ط_2 = \\mathbf{?}\\times10^{-19}\\ J',
             'micro': [('عوّض ن=2:', 'ط₂ = −2.18×10⁻¹⁸ / ?', '4')],
             'label': 'أدخل المعامل بوحدة ×10⁻¹⁹ J:',
             'prefix': 'ط₂ = ',
             'suffix': ' ×10⁻¹⁹ J',
             'target': -5.45,
             'completed_display': 'ط₂ = −5.45 ×10⁻¹⁹ J',
             'hint': '−2.18×10⁻¹⁸ ÷4 = −5.45×10⁻¹⁹.',
             'tol': 0.03},
            {'num': 2,
             'type': 'number',
             'title': 'الخطوة 2: طاقة المدار الخامس',
             'law': 'طₙ = −أ/ن²',
             'latex_preview': 'ط_5 = \\mathbf{?}\\times10^{-20}\\ J',
             'micro': [('عوّض ن=5:', 'ط₅ = −2.18×10⁻¹⁸ / ?', '25')],
             'label': 'أدخل المعامل بوحدة ×10⁻²⁰ J:',
             'prefix': 'ط₅ = ',
             'suffix': ' ×10⁻²⁰ J',
             'target': -8.72,
             'completed_display': 'ط₅ = −8.72 ×10⁻²⁰ J',
             'hint': '−2.18×10⁻¹⁸ ÷25 = −8.72×10⁻²⁰.',
             'tol': 0.04},
            {'num': 3,
             'type': 'number',
             'title': 'الخطوة 3: الطاقة عند ن=∞',
             'law': 'عند التأين يصبح ن=∞',
             'latex_preview': 'ط_{\\infty}=\\mathbf{?}\\ J',
             'micro': [('قسمة ثابت محدود على ∞ تؤول إلى:', 'أ/∞² = ?', '0')],
             'label': 'أدخل الطاقة:',
             'prefix': 'ط∞ = ',
             'suffix': ' J',
             'target': 0,
             'completed_display': 'ط∞ = 0 J',
             'hint': 'عند ن=∞ تصبح الطاقة صفرًا.',
             'tol': 0.001},
            {'num': 4,
             'type': 'symbol',
             'title': 'الخطوة 4: ترتيب الطاقات والاستنتاج',
             'law': 'القيم: ط₂ سالب أكبر مقدارًا، ط₅ أقرب للصفر، ط∞=0',
             'latex_preview': 'ط_2\\ \\mathbf{?}\\ ط_5\\ \\mathbf{?}\\ ط_{\\infty}',
             'micro': [('رتب من الأقل إلى الأعلى:', '?', 'ط2<ط5<طinf|ط2<ط5<ط∞')],
             'label': 'اكتب الترتيب دون مسافات:',
             'prefix': '',
             'suffix': '',
             'target': 'ط2<ط5<طinf|ط2<ط5<ط∞',
             'completed_display': 'ط₂ < ط₅ < ط∞؛ تزداد طاقة المدار بزيادة ن',
             'hint': 'اكتب ط2<ط5<ط∞.'}],
  'conclusion': 'ط₂ = −5.45×10⁻¹⁹ J، و ط₅ = −8.72×10⁻²⁰ J، و ط∞=0؛ لذلك تزداد طاقة المدار كلما زادت ن.'},
 {'id': 'tb6',
  'type': 'interactive',
  'title': 'تمرين الكتاب (6) · طاقة الانتقال من 1 إلى 4',
  'text': 'احسب مقدار الطاقة اللازمة لنقل إلكترون ذرة الهيدروجين من المدار الأول إلى المدار الرابع مباشرة. استخدم أ '
          '= 2.18×10⁻¹⁸ J.',
  'steps': [{'num': 1,
             'title': 'الخطوة 1: حساب فرق الطاقة الممتصة',
             'micro': [('الانتقال صاعد؛ لذلك الطاقة ممتصة وموجبة:', 'Δط = أ(1/ن₁² − 1/ن₂²)'),
                       ('حدد المدار الابتدائي:', 'ن₁ = ?', '1'),
                       ('حدد المدار النهائي:', 'ن₂ = ?', '4')],
             'law': 'Δط = أ(1/ن₁² − 1/ن₂²)',
             'simple_explain': 'عوّض ن₁=1 ون₂=4، واكتب معامل الناتج بوحدة ×10⁻¹⁸ J.',
             'prefix': 'Δط₁₈ = 2.18×(1/(',
             'blanks': [{'label': 'n1', 'target': 1.0, 'suffix': ')² − 1/('},
                        {'label': 'n2', 'target': 4.0, 'suffix': ')²)'}],
             'has_root': False,
             'result_target': 2.0437,
             'result_tol': 0.01,
             'result_label': 'احسب معامل الطاقة Δط (×10⁻¹⁸ J):',
             'hint': 'Δط = 2.18×(1 − 1/16)×10⁻¹⁸ = 2.0437×10⁻¹⁸ J.'}]},
 {'id': 'tb7',
  'type': 'interactive',
  'title': 'تمرين الكتاب (7) · طاقة الانبعاث من 3 إلى 1',
  'text': 'احسب مقدار الطاقة المنبعثة عند انتقال إلكترون ذرة الهيدروجين المهيجة من المدار الثالث إلى حالة الاستقرار '
          'مباشرة.',
  'steps': [{'num': 1,
             'title': 'الخطوة 1: مقدار فرق الطاقة',
             'micro': [('العودة إلى الاستقرار تعني الانتقال 3→1:', 'ن₂=3، ن₁=1'),
                       ('نحسب المقدار الموجب لطاقة الفوتون:', '|Δط| = أ(1/ن₁² − 1/ن₂²)')],
             'law': '|Δط| = أ(1/ن₁² − 1/ن₂²)',
             'simple_explain': 'عوّض المدار الأدنى ن₁=1 أولًا والمدار الأعلى ن₂=3 ثانيًا.',
             'prefix': '|Δط|₁₈ = 2.18×(1/(',
             'blanks': [{'label': 'nf', 'target': 1.0, 'suffix': ')² − 1/('},
                        {'label': 'ni', 'target': 3.0, 'suffix': ')²)'}],
             'has_root': False,
             'result_target': 1.9378,
             'result_tol': 0.01,
             'result_label': 'احسب معامل الطاقة المنبعثة |Δط| (×10⁻¹⁸ J):',
             'hint': '|Δط| = 2.18×(1 − 1/9)×10⁻¹⁸ = 1.9378×10⁻¹⁸ J.'}]},
 {'id': 'tb8',
  'type': 'interactive',
  'title': 'تمرين الكتاب (8) · انتقال الهيدروجين من 5 إلى 1',
  'text': 'انتقل إلكترون ذرة الهيدروجين المهيجة من المدار الخامس إلى المدار الأول مباشرة. احسب طاقة الفوتون المنبعث '
          'وتردده.',
  'steps': [{'num': 1,
             'title': 'الخطوة 1: طاقة الفوتون المنبعث',
             'micro': [('حدد الانتقال:', '5 → 1'),
                       ('طاقة الفوتون هي مقدار فرق الطاقة:', 'ط الفوتون = أ(1/1² − 1/5²)')],
             'law': 'ط الفوتون = أ(1/ن₁² − 1/ن₂²)',
             'simple_explain': 'عوّض ن₁=1 ون₂=5، ثم اكتب معامل طاقة الفوتون ×10⁻¹⁸ J.',
             'prefix': 'ط₁₈ = 2.18×(1/(',
             'blanks': [{'label': 'nf', 'target': 1.0, 'suffix': ')² − 1/('},
                        {'label': 'ni', 'target': 5.0, 'suffix': ')²)'}],
             'has_root': False,
             'result_target': 2.0928,
             'result_tol': 0.01,
             'result_label': 'احسب معامل طاقة الفوتون ط (×10⁻¹⁸ J):',
             'hint': 'ط الفوتون = 2.18×(1 − 1/25)×10⁻¹⁸ = 2.0928×10⁻¹⁸ J.'},
            {'num': 2,
             'title': 'الخطوة 2: تردد الفوتون',
             'micro': [('نستخدم علاقة بلانك:', 'ت = ط الفوتون/هـ'),
                       ('اكتب معامل الطاقة من الخطوة السابقة:', 'ط₁₈ = ?', '2.0928')],
             'law': 'ت = ط الفوتون/هـ، و هـ = 6.626×10⁻³⁴ J·s',
             'simple_explain': 'قسمة 10⁻¹⁸ على 10⁻³⁴ تعطي 10¹⁶، ثم عبّر عن الناتج ×10¹⁵ Hz.',
             'prefix': 'ت₁₅ = (',
             'blanks': [{'label': 'E', 'target': 2.0928, 'suffix': ')/('},
                        {'label': 'h', 'target': 6.626, 'suffix': ')×10'}],
             'has_root': False,
             'result_target': 3.1585,
             'result_tol': 0.02,
             'result_label': 'احسب معامل التردد ت (×10¹⁵ Hz):',
             'hint': 'ت = (2.0928×10⁻¹⁸)/(6.626×10⁻³⁴) = 3.1585×10¹⁵ Hz.'}]},
 {'id': 'tb9',
  'type': 'proof',
  'title': 'تمرين الكتاب (9) · مقارنة فروق الطاقة',
  'text': 'أيهما فرق طاقته أقل: بين المدارين الثاني والأول، أم بين المدارين الرابع والثالث؟ وما الاستنتاج؟',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: اختيار فرق الطاقة الأقل',
             'law': 'تتقارب مستويات الطاقة كلما ابتعدنا عن النواة',
             'latex_preview': 'أقل\\ فرق = \\mathbf{?}',
             'micro': [('قارن المسافتين في مخطط الطاقة:', 'الأقل بين المدارين ?', '4-3|3-4')],
             'label': 'اكتب الزوج 4-3:',
             'prefix': '',
             'suffix': '',
             'target': '4-3|3-4',
             'completed_display': 'فرق الطاقة بين المدارين الرابع والثالث هو الأقل',
             'hint': 'اكتب 4-3.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: صياغة الاستنتاج',
             'law': 'تتقارب المدارات المتتابعة عند زيادة ن',
             'latex_preview': 'بزيادة\\ ن\\ فإن\\ فرق\\ الطاقة\\ \\mathbf{?}',
             'micro': [('كلما ابتعدنا عن النواة يصبح الفرق:', 'فرق الطاقة ?', 'يتناقص|يقل')],
             'label': 'أكمل:',
             'prefix': 'فرق الطاقة ',
             'suffix': '',
             'target': 'يتناقص|يقل',
             'completed_display': 'كلما زادت ن تناقص فرق الطاقة بين كل مدارين متتابعين',
             'hint': 'اكتب: يتناقص.'}],
  'conclusion': 'فرق الطاقة بين المدارين 4 و3 أقل من الفرق بين 2 و1؛ لأن مستويات الطاقة تتقارب بزيادة ن.'},
 {'id': 'tb10',
  'type': 'interactive',
  'title': 'تمرين الكتاب (10) · ذرة هيدروجين طاقتها −أ/25',
  'text': 'هُيّجت ذرة هيدروجين إلى مدار طاقته −أ/25. أوجد رقم المدار، وعدد خطوط الطيف الممكنة، وطول موجة أعلى طاقة '
          'إشعاع، وتردد أقل طاقة إشعاع.',
  'steps': [{'num': 1,
             'title': 'الخطوة 1: إيجاد رقم المدار ن',
             'micro': [('من معادلة بور:', 'طₙ = −أ/ن²'), ('بالمقارنة مع −أ/25:', 'ن² = 25')],
             'law': 'طₙ = −أ/ن²',
             'simple_explain': 'ساوِ ن² بالمقام 25 ثم خذ الجذر الموجب.',
             'prefix': 'ن² = (',
             'blanks': [{'label': 'n2', 'target': 25.0, 'suffix': ')'}],
             'has_root': True,
             'result_target': 5.0,
             'result_tol': 0.01,
             'result_label': 'احسب رقم المدار ن:',
             'hint': 'ن = √25 = 5.',
             'root_prefix': 'ن = √(',
             'root_target': 25.0,
             'root_suffix': ')'},
            {'num': 2,
             'title': 'الخطوة 2: عدد خطوط الطيف الممكنة',
             'micro': [('عدد الخطوط من المستوى ن إلى الاستقرار:', 'عدد الخطوط = ن(ن−1)/2'),
                       ('استخدم ن الناتج:', 'ن = ?', '5')],
             'law': 'عدد الخطوط = ن(ن−1)/2',
             'simple_explain': 'عوّض ن=5 واحسب عدد الأزواج الممكنة بين المستويات.',
             'prefix': 'عدد الخطوط = (',
             'blanks': [{'label': 'n', 'target': 5.0, 'suffix': ')×('},
                        {'label': 'n_again', 'target': 5.0, 'suffix': '−1)/2'}],
             'has_root': False,
             'result_target': 10.0,
             'result_tol': 0.01,
             'result_label': 'احسب عدد الخطوط:',
             'hint': 'عدد الخطوط = 5×4÷2 = 10 خطوط.'},
            {'num': 3,
             'title': 'الخطوة 3: طول موجة أعلى طاقة إشعاع',
             'micro': [('أعلى طاقة تنتج من أكبر هبوط:', '5 → 1'),
                       ('نطبق علاقة رايدبرج بوحدة nm:', 'ل = 100/[1.1(1/1² − 1/5²)]')],
             'law': '1/ل = 1.1×10⁷(1/ن₁² − 1/ن₂²)',
             'simple_explain': 'أعلى طاقة تقابل أقصر طول موجي، أي الانتقال 5→1.',
             'prefix': 'ل = 100/[1.1×(1/(',
             'blanks': [{'label': 'nf', 'target': 1.0, 'suffix': ')² − 1/('},
                        {'label': 'ni', 'target': 5.0, 'suffix': ')²)]'}],
             'has_root': False,
             'result_target': 94.69,
             'result_tol': 0.2,
             'result_label': 'احسب الطول الموجي ل (nm):',
             'hint': 'ل = 100/[1.1(1 − 1/25)] = 94.69 nm.'},
            {'num': 4,
             'title': 'الخطوة 4: تردد أقل طاقة إشعاع',
             'micro': [('أقل طاقة تنتج من أصغر هبوط:', '5 → 4'),
                       ('طول هذه الموجة:', 'ل = 4.0404×10⁻⁶ m'),
                       ('ثم:', 'ت = س/ل')],
             'law': 'ت = س/ل، والانتقال الأقل طاقة هو 5→4',
             'simple_explain': 'عوّض س=3×10⁸ ول=4.0404×10⁻⁶، واكتب معامل التردد ×10¹³ Hz.',
             'prefix': 'ت₁₃ = (',
             'blanks': [{'label': 'c', 'target': 3.0, 'suffix': ')/('},
                        {'label': 'lambda', 'target': 4.0404, 'suffix': ')×10'}],
             'has_root': False,
             'result_target': 7.425,
             'result_tol': 0.03,
             'result_label': 'احسب معامل التردد ت (×10¹³ Hz):',
             'hint': 'ت = (3×10⁸)/(4.0404×10⁻⁶) = 7.425×10¹³ Hz.'}]},
 {'id': 'tb11',
  'type': 'proof',
  'title': 'تمرين الكتاب (11) · المستويات الفرعية عند n=4',
  'text': 'في المستوى الرئيس n=4: اكتب جميع قيم ℓ الممكنة، ثم رموز المستويات الفرعية وعددها.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: قيم العدد الكمي الفرعي ℓ',
             'law': 'قيم ℓ تبدأ من 0 وتنتهي عند n−1',
             'latex_preview': '\\ell = \\mathbf{?}',
             'micro': [('عندما n=4 تكون النهاية:', 'n−1 = ?', '3')],
             'label': 'اكتب القيم بفواصل:',
             'prefix': 'ℓ = ',
             'suffix': '',
             'target': '0,1,2,3|0123',
             'completed_display': 'ℓ = 0، 1، 2، 3',
             'hint': 'اكتب 0,1,2,3.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: رموز المستويات الفرعية',
             'law': 'ℓ=0,1,2,3 تقابل s,p,d,f',
             'latex_preview': '4s,4p,4d,\\mathbf{?}',
             'micro': [('اربط القيم بالرموز:', '4s,4p,4d,?', '4f')],
             'label': 'اكتب الرموز دون مسافات:',
             'prefix': '',
             'suffix': '',
             'target': '4s4p4d4f|4s,4p,4d,4f',
             'completed_display': '4s، 4p، 4d، 4f',
             'hint': 'اكتب 4s4p4d4f.'},
            {'num': 3,
             'type': 'number',
             'title': 'الخطوة 3: عدد المستويات الفرعية',
             'law': 'عدد المستويات الفرعية يساوي n',
             'latex_preview': 'N_{sub}=\\mathbf{?}',
             'micro': [('لأن n=4:', 'N_sub = ?', '4')],
             'label': 'أدخل العدد:',
             'prefix': 'N_sub = ',
             'suffix': '',
             'target': 4,
             'completed_display': 'عددها 4 مستويات فرعية',
             'hint': 'العدد يساوي n.',
             'tol': 0.01}],
  'conclusion': 'عند n=4 تكون ℓ=0،1،2،3، والرموز 4s و4p و4d و4f، وعددها أربعة.'},
 {'id': 'tb12',
  'type': 'proof',
  'title': 'تمرين الكتاب (12) · ترتيب طاقة المستويات الفرعية',
  'text': 'رتب حسب الطاقة: (1s، 3s، 2s)، ثم (3p، 3d، 3s). اكتب من الأعلى طاقة إلى الأقل.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: مقارنة أفلاك s',
             'law': 'للمستويات من النوع نفسه تزداد الطاقة بزيادة n',
             'latex_preview': '\\mathbf{?}',
             'micro': [('قارن n=3 ثم 2 ثم 1:', '?', '3s>2s>1s')],
             'label': 'اكتب الترتيب:',
             'prefix': '',
             'suffix': '',
             'target': '3s>2s>1s',
             'completed_display': '3s > 2s > 1s',
             'hint': 'اكتب 3s>2s>1s.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: مستويات لها n=3',
             'law': 'ضمن n نفسه تزداد الطاقة بزيادة ℓ: s ثم p ثم d',
             'latex_preview': '\\mathbf{?}',
             'micro': [('رتب d ثم p ثم s من الأعلى إلى الأقل:', '?', '3d>3p>3s')],
             'label': 'اكتب الترتيب:',
             'prefix': '',
             'suffix': '',
             'target': '3d>3p>3s',
             'completed_display': '3d > 3p > 3s',
             'hint': 'اكتب 3d>3p>3s.'}],
  'conclusion': 'من الأعلى إلى الأقل: 3s>2s>1s، و3d>3p>3s.'},
 {'id': 'tb13',
  'type': 'proof',
  'title': 'تمرين الكتاب (13) · أفلاك المستوى الفرعي 4d',
  'text': 'في المستوى الرئيس n=4: اكتب قيم ℓ الممكنة، وقيم mₗ عندما ℓ=2، وعدد الأفلاك ورمز مجموعتها.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: قيم ℓ عند n=4',
             'law': 'ℓ = 0 إلى n−1',
             'latex_preview': '\\ell=\\mathbf{?}',
             'micro': [('عند n=4:', 'ℓ = ?', '0,1,2,3|0123')],
             'label': 'اكتب القيم:',
             'prefix': '',
             'suffix': '',
             'target': '0,1,2,3|0123',
             'completed_display': 'ℓ = 0،1،2،3',
             'hint': 'اكتب 0,1,2,3.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: قيم mₗ عندما ℓ=2',
             'law': 'mₗ يأخذ القيم الصحيحة من −ℓ إلى +ℓ',
             'latex_preview': 'm_l=\\mathbf{?}',
             'micro': [('ابدأ من −2 وانتهِ عند +2:', 'mₗ = ?', '-2,-1,0,+1,+2|-2,-1,0,1,2')],
             'label': 'اكتب القيم:',
             'prefix': '',
             'suffix': '',
             'target': '-2,-1,0,+1,+2|-2,-1,0,1,2',
             'completed_display': 'mₗ = −2، −1، 0، +1، +2',
             'hint': 'اكتب -2,-1,0,+1,+2.'},
            {'num': 3,
             'type': 'number',
             'title': 'الخطوة 3: عدد الأفلاك',
             'law': 'عدد الأفلاك = 2ℓ+1',
             'latex_preview': 'N=2(2)+1=\\mathbf{?}',
             'micro': [('عوّض ℓ=2:', 'N = ?', '5')],
             'label': 'أدخل العدد:',
             'prefix': 'N = ',
             'suffix': '',
             'target': 5,
             'completed_display': 'عدد الأفلاك = 5',
             'hint': '2×2+1=5.',
             'tol': 0.01},
            {'num': 4,
             'type': 'symbol',
             'title': 'الخطوة 4: رمز مجموعة الأفلاك',
             'law': 'ℓ=2 يقابل d، وn=4',
             'latex_preview': 'الرمز=\\mathbf{?}',
             'micro': [('ادمج رقم المستوى مع رمز المستوى الفرعي:', '?', '4d')],
             'label': 'اكتب الرمز:',
             'prefix': '',
             'suffix': '',
             'target': '4d',
             'completed_display': 'رمز المجموعة = 4d',
             'hint': 'اكتب 4d.'}],
  'conclusion': 'ℓ=0،1،2،3؛ وعند ℓ=2 تكون قيم mₗ خمسًا من −2 إلى +2، لذا توجد خمسة أفلاك ورمز المجموعة 4d.'},
 {'id': 'tb14',
  'type': 'proof',
  'title': 'تمرين الكتاب (14) · ثلاثة إلكترونات في فلك واحد',
  'text': 'كيف يتعارض وجود ثلاثة إلكترونات في الفلك 2pₓ مع قاعدة باولي؟',
  'steps': [{'num': 1,
             'type': 'number',
             'title': 'الخطوة 1: سعة الفلك الواحد',
             'law': 'وفق قاعدة باولي لا يتسع الفلك لأكثر من إلكترونين متعاكسي الغزل',
             'latex_preview': 'N_{max}=\\mathbf{?}',
             'micro': [('السعة القصوى لكل فلك:', 'N_max = ?', '2')],
             'label': 'أدخل العدد:',
             'prefix': 'N_max = ',
             'suffix': '',
             'target': 2,
             'completed_display': 'السعة القصوى للفلك = إلكترونان',
             'hint': 'الفلك الواحد يتسع لإلكترونين فقط.',
             'tol': 0.01},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: تحديد القاعدة المخالفة',
             'law': 'مع ثلاثة إلكترونات سيشترك إلكترونان في الأعداد الكمية الأربعة نفسها',
             'latex_preview': 'المخالفة=\\mathbf{?}',
             'micro': [('هذا يخالف مبدأ الاستبعاد المعروف باسم:', '?', 'باولي|قاعدةباولي')],
             'label': 'اكتب اسم القاعدة:',
             'prefix': '',
             'suffix': '',
             'target': 'باولي|قاعدةباولي',
             'completed_display': 'يتعارض ذلك مع قاعدة باولي',
             'hint': 'اكتب: باولي.'}],
  'conclusion': 'ثلاثة إلكترونات في الفلك نفسه تجبر إلكترونين على امتلاك الأعداد الكمية الأربعة نفسها، وهذا يخالف '
                'قاعدة باولي.'},
 {'id': 'tb15',
  'type': 'proof',
  'title': 'تمرين الكتاب (15) · علاقات السعة في المستويات',
  'text': 'استنتج العلاقات بين n وعدد المستويات الفرعية والأفلاك والإلكترونات، ثم علاقة ℓ بسعة المستوى الفرعي.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: عدد المستويات الفرعية',
             'law': 'عدد المستويات الفرعية يساوي رقم المستوى الرئيس',
             'latex_preview': 'N_{sub}=\\mathbf{?}',
             'micro': [('العلاقة المباشرة:', 'N_sub = ?', 'n')],
             'label': 'اكتب العلاقة:',
             'prefix': 'N_sub = ',
             'suffix': '',
             'target': 'n',
             'completed_display': 'N_sub = n',
             'hint': 'اكتب n.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: عدد الأفلاك الكلي',
             'law': 'عدد الأفلاك الكلي في المستوى الرئيس',
             'latex_preview': 'N_{orbitals}=\\mathbf{?}',
             'micro': [('من الجدول 1،4،9،16:', 'N_orbitals = ?', 'n2|n^2|n²')],
             'label': 'اكتب العلاقة:',
             'prefix': 'N_orbitals = ',
             'suffix': '',
             'target': 'n2|n^2|n²',
             'completed_display': 'N_orbitals = n²',
             'hint': 'اكتب n2 أو n^2.'},
            {'num': 3,
             'type': 'symbol',
             'title': 'الخطوة 3: أقصى إلكترونات المستوى الرئيس',
             'law': 'كل فلك يتسع لإلكترونين',
             'latex_preview': 'N_e=\\mathbf{?}',
             'micro': [('نضرب عدد الأفلاك n² في 2:', 'N_e = ?', '2n2|2n^2|2n²')],
             'label': 'اكتب العلاقة:',
             'prefix': 'N_e = ',
             'suffix': '',
             'target': '2n2|2n^2|2n²',
             'completed_display': 'N_e = 2n²',
             'hint': 'اكتب 2n2.'},
            {'num': 4,
             'type': 'symbol',
             'title': 'الخطوة 4: أقصى إلكترونات المستوى الفرعي',
             'law': 'عدد أفلاك المستوى الفرعي = 2ℓ+1، وكل فلك يسع 2',
             'latex_preview': 'N_e=\\mathbf{?}',
             'micro': [('اضرب عدد الأفلاك في 2:', 'N_e = ?', '2(2l+1)|2(2ℓ+1)')],
             'label': 'اكتب العلاقة:',
             'prefix': 'N_e = ',
             'suffix': '',
             'target': '2(2l+1)|2(2ℓ+1)',
             'completed_display': 'N_e = 2(2ℓ+1)',
             'hint': 'اكتب 2(2l+1).'}],
  'conclusion': 'عدد المستويات الفرعية=n، وعدد الأفلاك=n²، وأقصى إلكترونات المستوى=2n²، وأقصى إلكترونات المستوى '
                'الفرعي=2(2ℓ+1).'},
 {'id': 'tb16',
  'type': 'proof',
  'title': 'تمرين الكتاب (16) · ترتيب مستويات مختلفة حسب الطاقة',
  'text': 'رتب المستويات الفرعية 5s، 3d، 4s، 4f، 5p حسب الطاقة، من الأقل إلى الأعلى.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: كتابة الترتيب التصاعدي',
             'law': 'نستخدم ترتيب أوفباو للمستويات الفرعية',
             'latex_preview': '\\mathbf{?}',
             'micro': [('اقرأ مواقع المستويات في مخطط البناء التصاعدي:', '?', '4s<3d<5s<5p<4f')],
             'label': 'اكتب الترتيب:',
             'prefix': '',
             'suffix': '',
             'target': '4s<3d<5s<5p<4f',
             'completed_display': '4s < 3d < 5s < 5p < 4f',
             'hint': 'اكتب 4s<3d<5s<5p<4f.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: تسمية القاعدة',
             'law': 'توزع الإلكترونات بدءًا بالمستوى الأقل طاقة',
             'latex_preview': 'القاعدة=\\mathbf{?}',
             'micro': [('اسم مبدأ البناء التصاعدي:', '?', 'اوفباو|أوفباو|قاعدةاوفباو|قاعدةأوفباو')],
             'label': 'اكتب الاسم:',
             'prefix': '',
             'suffix': '',
             'target': 'اوفباو|أوفباو|قاعدةاوفباو|قاعدةأوفباو',
             'completed_display': 'القاعدة المستخدمة: أوفباو',
             'hint': 'اكتب أوفباو.'}],
  'conclusion': 'الترتيب التصاعدي للطاقة: 4s < 3d < 5s < 5p < 4f.'},
 {'id': 'tb17',
  'type': 'proof',
  'title': 'تمرين الكتاب (17) · كتابة التركيب الإلكتروني الكامل',
  'text': 'اكتب التركيب الإلكتروني الكامل لكل من F (Z=9)، Mg (Z=12)، Sc (Z=21)، Mo (Z=42).',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: ذرة الفلور F',
             'law': 'وزع 9 إلكترونات حسب أوفباو',
             'latex_preview': 'F:\\ \\mathbf{?}',
             'micro': [('بعد 1s²2s² يتبقى خمسة إلكترونات:', '2p?', '5')],
             'label': 'اكتب دون مسافات:',
             'prefix': '',
             'suffix': '',
             'target': '1s22s22p5',
             'completed_display': 'F: 1s² 2s² 2p⁵',
             'hint': 'اكتب 1s22s22p5.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: ذرة المغنيسيوم Mg',
             'law': 'وزع 12 إلكترونًا',
             'latex_preview': 'Mg:\\ \\mathbf{?}',
             'micro': [('بعد [Ne] يتبقى إلكترونان:', '3s?', '2')],
             'label': 'اكتب دون مسافات:',
             'prefix': '',
             'suffix': '',
             'target': '1s22s22p63s2',
             'completed_display': 'Mg: 1s² 2s² 2p⁶ 3s²',
             'hint': 'اكتب 1s22s22p63s2.'},
            {'num': 3,
             'type': 'symbol',
             'title': 'الخطوة 3: ذرة السكانديوم Sc',
             'law': 'بعد [Ar] يملأ 4s ثم 3d',
             'latex_preview': 'Sc:\\ \\mathbf{?}',
             'micro': [('الإلكترون الحادي والعشرون يدخل:', '?', '3d1')],
             'label': 'اكتب دون مسافات:',
             'prefix': '',
             'suffix': '',
             'target': '1s22s22p63s23p64s23d1',
             'completed_display': 'Sc: 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹',
             'hint': 'اكتب 1s22s22p63s23p64s23d1.'},
            {'num': 4,
             'type': 'symbol',
             'title': 'الخطوة 4: ذرة الموليبدينوم Mo',
             'law': 'Mo حالة خاصة تنتهي 5s¹4d⁵ لتحقيق نصف امتلاء d',
             'latex_preview': 'Mo:\\ \\mathbf{?}',
             'micro': [('النهاية الأكثر استقرارًا:', '[Kr] ?', '5s14d5|4d55s1')],
             'label': 'اكتب التركيب الكامل دون مسافات:',
             'prefix': '',
             'suffix': '',
             'target': '1s22s22p63s23p64s23d104p65s14d5|1s22s22p63s23p64s23d104p64d55s1',
             'completed_display': 'Mo: 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶ 5s¹ 4d⁵',
             'hint': 'اكتب النهاية 5s14d5 بعد تركيب [Kr].'}],
  'conclusion': 'F: 1s²2s²2p⁵؛ Mg: 1s²2s²2p⁶3s²؛ Sc: [Ar]4s²3d¹؛ Mo: [Kr]5s¹4d⁵.'},
 {'id': 'tb18',
  'type': 'proof',
  'title': 'تمرين الكتاب (18) · التركيب بدلالة العنصر النبيل',
  'text': 'اكتب التركيب الإلكتروني بدلالة العنصر النبيل لكل من B، Ne، Cl، Ca، Fe، Cr، Cu.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: B',
             'law': 'يسبقه He',
             'latex_preview': 'B:\\ \\mathbf{?}',
             'micro': [('بعد [He]:', '?', '2s22p1')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[He]2s22p1|He2s22p1',
             'completed_display': 'B: [He] 2s² 2p¹',
             'hint': 'اكتب [He]2s22p1.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: Ne',
             'law': 'نواة الهيليوم ثم المستوى الثاني',
             'latex_preview': 'Ne:\\ \\mathbf{?}',
             'micro': [('بعد [He]:', '?', '2s22p6')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[He]2s22p6|He2s22p6',
             'completed_display': 'Ne: [He] 2s² 2p⁶',
             'hint': 'اكتب [He]2s22p6.'},
            {'num': 3,
             'type': 'symbol',
             'title': 'الخطوة 3: Cl',
             'law': 'يسبقه Ne',
             'latex_preview': 'Cl:\\ \\mathbf{?}',
             'micro': [('بعد [Ne]:', '?', '3s23p5')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[Ne]3s23p5|Ne3s23p5',
             'completed_display': 'Cl: [Ne] 3s² 3p⁵',
             'hint': 'اكتب [Ne]3s23p5.'},
            {'num': 4,
             'type': 'symbol',
             'title': 'الخطوة 4: Ca',
             'law': 'يسبقه Ar',
             'latex_preview': 'Ca:\\ \\mathbf{?}',
             'micro': [('بعد [Ar]:', '?', '4s2')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[Ar]4s2|Ar4s2',
             'completed_display': 'Ca: [Ar] 4s²',
             'hint': 'اكتب [Ar]4s2.'},
            {'num': 5,
             'type': 'symbol',
             'title': 'الخطوة 5: Fe',
             'law': 'يسبقه Ar',
             'latex_preview': 'Fe:\\ \\mathbf{?}',
             'micro': [('بعد [Ar]:', '?', '4s23d6|3d64s2')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[Ar]4s23d6|[Ar]3d64s2|Ar4s23d6|Ar3d64s2',
             'completed_display': 'Fe: [Ar] 4s² 3d⁶',
             'hint': 'اكتب [Ar]4s23d6.'},
            {'num': 6,
             'type': 'symbol',
             'title': 'الخطوة 6: Cr',
             'law': 'استثناء نصف امتلاء d',
             'latex_preview': 'Cr:\\ \\mathbf{?}',
             'micro': [('النهاية المستقرة:', '?', '4s13d5|3d54s1')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[Ar]4s13d5|[Ar]3d54s1|Ar4s13d5|Ar3d54s1',
             'completed_display': 'Cr: [Ar] 4s¹ 3d⁵',
             'hint': 'اكتب [Ar]4s13d5.'},
            {'num': 7,
             'type': 'symbol',
             'title': 'الخطوة 7: Cu',
             'law': 'استثناء امتلاء d',
             'latex_preview': 'Cu:\\ \\mathbf{?}',
             'micro': [('النهاية المستقرة:', '?', '4s13d10|3d104s1')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[Ar]4s13d10|[Ar]3d104s1|Ar4s13d10|Ar3d104s1',
             'completed_display': 'Cu: [Ar] 4s¹ 3d¹⁰',
             'hint': 'اكتب [Ar]4s13d10.'}],
  'conclusion': 'التراكيب المختصرة الصحيحة: B [He]2s²2p¹، Ne [He]2s²2p⁶، Cl [Ne]3s²3p⁵، Ca [Ar]4s²، Fe [Ar]4s²3d⁶، '
                'Cr [Ar]4s¹3d⁵، Cu [Ar]4s¹3d¹⁰.'},
 {'id': 'tb19',
  'type': 'proof',
  'title': 'تمرين الكتاب (19) · التمثيل الفلكي والخواص المغناطيسية',
  'text': 'للذرات Ne وB وNi: اكتب التركيب الإلكتروني، ثم حدّد عدد الإلكترونات المفردة والصفة المغناطيسية. يظهر '
          'التمثيل الفلكي الصحيح بعد إكمال كل تركيب.',
  'steps': [{'num': 1,
             'type': 'symbol',
             'title': 'الخطوة 1: تركيب Ne',
             'law': 'Ne: عشرة إلكترونات',
             'latex_preview': 'Ne:\\ \\mathbf{?}',
             'micro': [('بعد [He] يمتلئ 2s و2p:', '?', '2s22p6')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[He]2s22p6|He2s22p6',
             'completed_display': 'Ne: [He]2s²2p⁶  |  2s[↑↓] 2p[↑↓][↑↓][↑↓]',
             'hint': 'اكتب [He]2s22p6.'},
            {'num': 2,
             'type': 'symbol',
             'title': 'الخطوة 2: تركيب B',
             'law': 'B: خمسة إلكترونات',
             'latex_preview': 'B:\\ \\mathbf{?}',
             'micro': [('بعد [He] يكون:', '?', '2s22p1')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[He]2s22p1|He2s22p1',
             'completed_display': 'B: [He]2s²2p¹  |  2s[↑↓] 2p[↑][ ][ ]',
             'hint': 'اكتب [He]2s22p1.'},
            {'num': 3,
             'type': 'symbol',
             'title': 'الخطوة 3: تركيب Ni',
             'law': 'Ni: ثمانية وعشرون إلكترونًا',
             'latex_preview': 'Ni:\\ \\mathbf{?}',
             'micro': [('بعد [Ar] يكون:', '?', '4s23d8|3d84s2')],
             'label': 'اكتب التركيب:',
             'prefix': '',
             'suffix': '',
             'target': '[Ar]4s23d8|[Ar]3d84s2|Ar4s23d8|Ar3d84s2',
             'completed_display': 'Ni: [Ar]4s²3d⁸  |  4s[↑↓] 3d[↑↓][↑↓][↑↓][↑][↑]',
             'hint': 'اكتب [Ar]4s23d8.'},
            {'num': 4,
             'type': 'number',
             'title': 'الخطوة 4: مفردة Ne',
             'law': 'جميع أفلاك 2s و2p مزدوجة',
             'latex_preview': 'N_u(Ne)=\\mathbf{?}',
             'micro': [('عد الأسهم غير المزدوجة:', '?', '0')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 0,
             'completed_display': 'Ne: صفر إلكترونات مفردة',
             'hint': 'كل الإلكترونات مزدوجة.',
             'tol': 0.01},
            {'num': 5,
             'type': 'number',
             'title': 'الخطوة 5: مفردة B',
             'law': 'يوجد إلكترون واحد في 2p',
             'latex_preview': 'N_u(B)=\\mathbf{?}',
             'micro': [('فلك p الأول يحوي سهمًا منفردًا:', '?', '1')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 1,
             'completed_display': 'B: إلكترون مفرد واحد',
             'hint': '2p¹ يعني إلكترونًا مفردًا.',
             'tol': 0.01},
            {'num': 6,
             'type': 'number',
             'title': 'الخطوة 6: مفردة Ni',
             'law': 'في 3d⁸ يبقى إلكترونان مفردان',
             'latex_preview': 'N_u(Ni)=\\mathbf{?}',
             'micro': [('طبق قاعدة هوند على خمسة أفلاك d:', '?', '2')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 2,
             'completed_display': 'Ni: إلكترونان مفردان',
             'hint': '3d⁸ يترك فلكين بكل منهما إلكترون مفرد.',
             'tol': 0.01},
            {'num': 7,
             'type': 'symbol',
             'title': 'الخطوة 7: صفة Ne',
             'law': 'انعدام الإلكترونات المفردة يعني ديامغناطيسية',
             'latex_preview': 'Ne\\rightarrow\\mathbf{?}',
             'micro': [('0 إلكترونات مفردة:', '?', 'دايامغناطيسية|ديامغناطيسية|دايامغناطيسي|ديامغناطيسي')],
             'label': 'اكتب الصفة:',
             'prefix': '',
             'suffix': '',
             'target': 'دايامغناطيسية|ديامغناطيسية|دايامغناطيسي|ديامغناطيسي',
             'completed_display': 'Ne ذرة دايامغناطيسية',
             'hint': 'اكتب دايامغناطيسية.'},
            {'num': 8,
             'type': 'symbol',
             'title': 'الخطوة 8: صفة B',
             'law': 'وجود إلكترون مفرد يعني بارامغناطيسية',
             'latex_preview': 'B\\rightarrow\\mathbf{?}',
             'micro': [('إلكترون مفرد واحد:', '?', 'بارامغناطيسية|بارامغناطيسي')],
             'label': 'اكتب الصفة:',
             'prefix': '',
             'suffix': '',
             'target': 'بارامغناطيسية|بارامغناطيسي',
             'completed_display': 'B ذرة بارامغناطيسية',
             'hint': 'اكتب بارامغناطيسية.'},
            {'num': 9,
             'type': 'symbol',
             'title': 'الخطوة 9: صفة Ni',
             'law': 'وجود إلكترونين مفردين يعني بارامغناطيسية',
             'latex_preview': 'Ni\\rightarrow\\mathbf{?}',
             'micro': [('إلكترونان مفردان:', '?', 'بارامغناطيسية|بارامغناطيسي')],
             'label': 'اكتب الصفة:',
             'prefix': '',
             'suffix': '',
             'target': 'بارامغناطيسية|بارامغناطيسي',
             'completed_display': 'Ni ذرة بارامغناطيسية',
             'hint': 'اكتب بارامغناطيسية.'}],
  'conclusion': 'Ne: صفر مفرد ودايامغناطيسية؛ B: مفرد واحد وبارامغناطيسية؛ Ni: مفردان وبارامغناطيسية.'},
 {'id': 'tb20',
  'type': 'proof',
  'title': 'تمرين الكتاب (20) · حساب إلكترونات التكافؤ',
  'text': 'احسب عدد إلكترونات التكافؤ لكل من N (Z=7)، Al (Z=13)، Ar (Z=18)، V (Z=23) حسب قاعدة الكتاب.',
  'steps': [{'num': 1,
             'type': 'number',
             'title': 'الخطوة 1: N',
             'law': 'N: [He]2s²2p³',
             'latex_preview': 'N_v(N)=2+3=\\mathbf{?}',
             'micro': [('اجمع إلكترونات 2s و2p:', '?', '5')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 5,
             'completed_display': 'N له 5 إلكترونات تكافؤ',
             'hint': '2+3=5.',
             'tol': 0.01},
            {'num': 2,
             'type': 'number',
             'title': 'الخطوة 2: Al',
             'law': 'Al: [Ne]3s²3p¹',
             'latex_preview': 'N_v(Al)=2+1=\\mathbf{?}',
             'micro': [('اجمع إلكترونات 3s و3p:', '?', '3')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 3,
             'completed_display': 'Al له 3 إلكترونات تكافؤ',
             'hint': '2+1=3.',
             'tol': 0.01},
            {'num': 3,
             'type': 'number',
             'title': 'الخطوة 3: Ar',
             'law': 'Ar: [Ne]3s²3p⁶',
             'latex_preview': 'N_v(Ar)=2+6=\\mathbf{?}',
             'micro': [('اجمع إلكترونات 3s و3p:', '?', '8')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 8,
             'completed_display': 'Ar له 8 إلكترونات تكافؤ',
             'hint': '2+6=8.',
             'tol': 0.01},
            {'num': 4,
             'type': 'number',
             'title': 'الخطوة 4: V',
             'law': 'V: [Ar]4s²3d³ وd غير ممتلئ',
             'latex_preview': 'N_v(V)=2+3=\\mathbf{?}',
             'micro': [('للعنصر الانتقالي ذي d غير الممتلئ نجمع ns و(n−1)d:', '?', '5')],
             'label': 'أدخل العدد:',
             'prefix': '',
             'suffix': '',
             'target': 5,
             'completed_display': 'V له 5 إلكترونات تكافؤ',
             'hint': '2+3=5.',
             'tol': 0.01}],
  'conclusion': 'إلكترونات التكافؤ: N=5، Al=3، Ar=8، V=5.'}]

TOTAL_QUESTIONS = len(questions_db)

FORMULA_SHEET = [('العلاقة الموجية', 'س = ل · ت'),
 ('طاقة الفوتون', 'ط = هـ · ت = هـ · س / ل'),
 ('طاقة مدار الهيدروجين', 'طₙ = −أ / ن²'),
 ('فرق طاقة الانتقال', '|Δط| = أ |1/ن₁² − 1/ن₂²|'),
 ('علاقة رايدبرج', '1/ل = ر(1/ن₁² − 1/ن₂²)'),
 ('عدد خطوط الطيف', 'عدد الخطوط = ن(ن−1)/2'),
 ('عدد المستويات الفرعية', 'N_sub = n'),
 ('عدد أفلاك المستوى الرئيس', 'N_orbitals = n²'),
 ('سعة المستوى الرئيس', 'N_e = 2n²'),
 ('أفلاك وسعة المستوى الفرعي', 'N_orbitals = 2ℓ+1 ، N_e = 2(2ℓ+1)'),
 ('قيم أعداد الكم', 'ℓ = 0…n−1 ، mₗ = −ℓ…+ℓ ، mₛ = ±1/2'),
 ('ثوابت الكتاب', 'أ = 2.18×10⁻¹⁸ J ، هـ = 6.626×10⁻³⁴ J·s ، س = 3×10⁸ m/s ، ر = 1.1×10⁷ m⁻¹')]

STUDY_TIPS = ['📘 نصيحة: اقرأ رقم التمرين والمعطيات كما وردت في الكتاب قبل اختيار القانون.',
 '📘 نصيحة: في معادلة رايدبرج ضع المدار الأقل طاقة في الحد الأول.',
 '📘 نصيحة: الطاقة الأعلى تعني ترددًا أعلى وطولًا موجيًا أقصر.',
 '📘 نصيحة: عند كتابة التركيب الإلكتروني اتبع أوفباو ثم باولي ثم هوند.',
 '📘 نصيحة: اكتب الأسس بوضوح وتحقق أن مجموع الإلكترونات يساوي العدد الذري.',
 '📘 نصيحة: للعنصر الانتقالي اتبع قاعدة الكتاب في حساب إلكترونات التكافؤ، وانتبه لامتلاء d.']

SUCCESS_PHRASES = ["أحسنت! 👏🏼", "رائع جداً! 🌟", "ممتاز! 🔥", "عمل احترافي! 🚀", "بالضبط! 🎯"]

# ==========================================================
# 4. إدارة الحالة (Session State)
# ==========================================================
def init_state():
    defaults = {
        "book_student_name": "", "book_total_xp": 0, "book_streak": 0,
        "book_badges": set(), "book_completed_questions": set(),
        "book_no_hint_flag": {}, "book_attempts": {}, "book_hint_level": {},
        "book_start_time": {}, "book_time_spent": {},
        "book_daily_tip": random.choice(STUDY_TIPS),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
# مزامنة اسم الطالب من الحساب المحلي للمنصة دون المساس بتقدم المواد الأخرى.
if st.session_state.get("student_profile") and not st.session_state.get("book_student_name"):
    st.session_state["book_student_name"] = st.session_state["student_profile"].get("name", "")

def award_badge(name):
    if name not in st.session_state["book_badges"]:
        st.session_state["book_badges"].add(name)
        if hasattr(st, "toast"):
            st.toast(f"🏅 وسام جديد: {name}", icon="🏅")

def normalize_symbol(symbol_str: str, case_sensitive: bool = False) -> str:
    """توحيد صيغة الإجابة الرمزية للمقارنة (حذف الفراغات/الشرطات السفلية/النجوم)."""
    if not symbol_str:
        return ""
    cleaned = symbol_str.replace(" ", "").replace("_", "").replace("*", "")
    return cleaned if case_sensitive else cleaned.lower()

def _contains_arabic(value) -> bool:
    text = str(value or "")
    return any(
        ("\u0600" <= ch <= "\u06ff")
        or ("\u0750" <= ch <= "\u077f")
        or ("\ufb50" <= ch <= "\ufeff")
        for ch in text
    )


def equation_direction(value) -> str:
    text = str(value or "").strip()
    if not text:
        return "ltr"
    positions = [text.find(mark) for mark in ("=", "⇒", "⇔", "≈", "≠", "≤", "≥", "<", ">") if text.find(mark) >= 0]
    head = text[:min(positions)] if positions else text
    if _contains_arabic(head):
        return "rtl"
    if any(("A" <= ch <= "Z") or ("a" <= ch <= "z") or ("\u0370" <= ch <= "\u03ff") or ("\u2100" <= ch <= "\u214f") for ch in head):
        return "ltr"
    return "rtl" if _contains_arabic(text) else "ltr"


def eq_html(tex: str) -> str:
    """يحول معادلة LaTeX البسيطة إلى HTML عملي يُقرأ من اليسار إلى اليمين (بدون KaTeX)."""
    if not tex:
        return ""
    flow = equation_direction(tex)

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
            if c == "<":
                out.append("&lt;")
                i += 1
                continue
            if c == ">":
                out.append("&gt;")
                i += 1
                continue
            if c == "\\":
                i += 1
                continue

            out.append(c)
            i += 1
        return "".join(out)

    return ('<span class="eq eq-' + flow + '" dir="' + flow + '">'
            + conv(str(tex).strip()) + "</span>")


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
_UNIT_TOKENS = ["J.s", "J·s", "m⁻¹", "m^-1", "Hz", "nm",
                "Kg.m/s²", "kg.m/s²", "Kg.m/s", "kg.m/s", "Kg·m/s", "kg·m/s",
                "N.s", "N·s", "m/s²", "m/s^2", "m/s", "km/h", "J/kg"]
_REL_SEPS = ["=", "⇒", "⇔", "⇐", "≈", "≠", "≤", "≥", "→", "+", " − ", " - "]


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
    """يعرض المعادلة كوحدة واحدة باتجاه رموزها، والنص العربي كنص RTL."""
    raw = str(text).strip()
    if not raw:
        return ""

    flow = equation_direction(raw)
    relation_marks = ("=", "⇒", "⇔", "≈", "≠", "≤", "≥", "<", ">")
    if any(mark in raw for mark in relation_marks) and (flow == "rtl" or not _contains_arabic(raw)):
        return (
            '<span class="' + eq_cls + ' eq-flow-' + flow + '" dir="' + flow + '">'
            + plain_to_eq(raw) + "</span>"
        )

    segs = _split_ar_math(raw)
    if not segs:
        return ""
    if not any(m == "ar" for m, _t in segs):
        return (
            '<span class="' + eq_cls + ' eq-flow-ltr" dir="ltr">'
            + plain_to_eq(raw) + "</span>"
        )

    body = ""
    for mode, part in segs:
        if mode == "ar" or not any(ch.isalnum() for ch in part):
            body += part
        else:
            pflow = equation_direction(part)
            body += (
                '<span class="eq-inline eq-flow-' + pflow + '" dir="' + pflow + '">'
                + plain_to_eq(part) + "</span>"
            )
    return '<span class="' + note_cls + '" dir="rtl">' + body + "</span>"


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


DERIVE_STEPS = {}

FIGURES = {}

FIGURE_CAPTIONS = {}

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


DERIVE_TITLES = {}

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

def micro_html(step, final_mode="preview", field="micro", start=0, final_say=None, qid=""):
    """صندوق الخطوات المبسّطة: يعوّض الطالب في كل خطوة حتى يصل للعبارة الكاملة"""
    micro = step.get(field) or []
    cs = "1" if step.get("case_sensitive") else "0"
    rows = []
    n = start
    for item in micro:
        say = item[0] if len(item) > 0 else ""
        eq = item[1] if len(item) > 1 else ""
        ans = item[2] if len(item) > 2 else None
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
            + '<div class="eq-box">' + eq_html(step.get("latex_preview", "")) + "</div></div>"
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
    flow = equation_direction(t)
    return ('<span class="eq eq-' + flow + '" dir="' + flow + '">'
            + "".join(out) + "</span>")


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
        return "🏆 خبير تمارين الكتاب", "#f59e0b", max(xp + 20, 150)

def fmt_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"

def reset_question(qid, qtype):
    st.session_state["book_completed_questions"].discard(qid)
    st.session_state["book_start_time"][qid] = time.time()
    st.session_state["book_time_spent"].pop(qid, None)
    st.session_state[f"book_step_prog_{qid}"] = 1
    st.session_state["book_no_hint_flag"][qid] = True
    keys_to_clear = [k for k in st.session_state["book_attempts"] if k.startswith(f"{qid}_")]
    for k in keys_to_clear:
        st.session_state["book_attempts"].pop(k, None)
        st.session_state["book_hint_level"].pop(k, None)

def reset_everything():
    keep_name = st.session_state.get("book_student_name", "")
    book_state_keys = {
        "book_student_name", "book_total_xp", "book_streak", "book_badges",
        "book_completed_questions", "book_no_hint_flag", "book_attempts",
        "book_hint_level", "book_start_time", "book_time_spent", "book_daily_tip",
        "book_samed_view", "book_samed_grade", "book_samed_subject",
        "_chem_book_startup_version",
    }
    book_widget_prefixes = (
        "book_step_prog_tb", "input_tb", "result_tb", "root_tb", "proof_tb",
        "check_tb", "hint_tb", "solve_tb", "reset_tb",
    )
    for key in list(st.session_state.keys()):
        if key in book_state_keys or str(key).startswith(book_widget_prefixes):
            del st.session_state[key]
    init_state()
    st.session_state["book_student_name"] = keep_name

# ==========================================================
# 5. زر الملف الشخصي (نافذة منبثقة) في أعلى يمين الصفحة
# ==========================================================
with st.container(key="avatar_row"):
    _pc_avatar = st.columns([1, 11])[0]
with _pc_avatar:
    level_label, level_color, next_threshold = get_level(st.session_state["book_total_xp"])
    xp = st.session_state["book_total_xp"]
    progress_pct = min(100, int((xp / next_threshold) * 100)) if next_threshold else 100
    name_display = st.session_state["book_student_name"] or "طالب مجتهد"
    avatar_letter = name_display.strip()[0] if name_display.strip() else "🧑‍🎓"
    done_count = len(st.session_state["book_completed_questions"])
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

            st.session_state["book_student_name"] = st.text_input(
                "✏️ اسم الطالب/ـة", value=st.session_state["book_student_name"],
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
            if st.session_state["book_badges"]:
                tiles = ""
                for b in sorted(st.session_state["book_badges"]):
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
    subject="الكيمياء", track="تمارين الكتاب", unit_title="حلول تمارين الكتاب · البناء الإلكتروني للذرة",
    current_page="pages/chemistry_textbook_exercises.py", tip=st.session_state["book_daily_tip"], subject_icon="🧪",
)

st.caption("📚 تشمل الصفحة تمارين الكتاب المدرسي (1–20) في الوحدة الأولى، والقيم النهائية مطابقة لملف الإجابات النموذجية المرفق.")

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
        12: ["تمارين الكتاب المدرسي · البناء الإلكتروني للذرة", "الحسابات الكيميائية", "الاتزان الكيميائي", "الكيمياء العضوية"],
    },
}

# الوحدة المبنية فعليًا الآن: (المادة، الصف، رقم الوحدة)
HOME_LIVE = ("chem", 12, 0)

for _k, _v in (("book_samed_view", "app"), ("book_samed_grade", 12), ("book_samed_subject", "chem")):
    if _k not in st.session_state:
        st.session_state[_k] = _v

# افتح شاشة التمارين مباشرة في أول تشغيل لهذه النسخة، حتى لو بقيت حالة
# "home" من نسخة أقدم داخل جلسة Streamlit الحالية. بعد ذلك يبقى زر العودة فعالًا.
CHEM_BOOK_STARTUP_VERSION = "chem-book-direct-v1"
if st.session_state.get("_chem_book_startup_version") != CHEM_BOOK_STARTUP_VERSION:
    st.session_state["book_samed_view"] = "app"
    st.session_state["book_samed_grade"] = 12
    st.session_state["book_samed_subject"] = "chem"
    st.session_state["_chem_book_startup_version"] = CHEM_BOOK_STARTUP_VERSION

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


if st.session_state["book_samed_view"] == "home":

    _xp   = int(st.session_state.get("book_total_xp", 0) or 0)
    _done = len(st.session_state.get("book_completed_questions", set()) or set())
    _bdg  = len(st.session_state.get("book_badges", set()) or set())
    _strk = int(st.session_state.get("book_streak", 0) or 0)
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
            "<b>📘 تمارين الكتاب المدرسي — الوحدة الأولى</b>"
            "<small>الكيمياء · الصف الثاني عشر</small>"
            "<div class='home-bar'><i style='width:" + str(_pct) + "%'></i></div>"
            "<small>أنجزتَ " + str(_done) + " من " + str(TOTAL_QUESTIONS) +
            " تمرينًا (" + str(_pct) + "%)</small></div>",
            unsafe_allow_html=True)
        if st.button("▶️ ابدأ / تابِع الحل", key="samed_go",
                     use_container_width=True, type="primary"):
            st.session_state["book_samed_view"] = "app"
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
            _on = (st.session_state["book_samed_grade"] == _gn)
            if st.button(str(_gn) + " · " + _gl, key="samed_g_" + str(_gn),
                         use_container_width=True,
                         type=("primary" if _on else "secondary")):
                st.session_state["book_samed_grade"] = _gn
                st.rerun()

    # ---------- المواد ----------
    _grade = st.session_state["book_samed_grade"]
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
            _open = (st.session_state["book_samed_subject"] == _sk2)
            if st.button(("▼ إخفاء الوحدات" if _open else "عرض الوحدات ←"),
                         key="samed_s_" + _sk2, use_container_width=True,
                         type=("primary" if _open else "secondary")):
                st.session_state["book_samed_subject"] = (None if _open else _sk2)
                st.rerun()

    # ---------- الوحدات ----------
    _subj = st.session_state["book_samed_subject"]
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
                    st.session_state["book_samed_view"] = "app"
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
        if st.button("← لوحة الطالب", key="samed_back", use_container_width=True):
            st.session_state["samed_view"] = "dashboard"
            st.switch_page("app.py")


# ==========================================================
# 7. اختيار التمرين + وضع الشرح المبسط
# ==========================================================
def display_title(item):
    icon = "🧮" if item["type"] == "interactive" else "🧠"
    return f"{icon} {item['title']}"

with st.container(key="exercise_controls"):
    col_sel, col_toggle = st.columns([3, 1])
    with col_sel:
        selected_title = st.selectbox(
            "📌 اختر التمرين المراد حله تفاعلياً:",
            [display_title(item) for item in questions_db]
        )
    with col_toggle:
        explain_mode = st.toggle("🔍 شرح مبسط", value=False)

q = next(item for item in questions_db if display_title(item) == selected_title)
qid = q["id"]
qtype = q["type"]

if qid not in st.session_state["book_start_time"]:
    st.session_state["book_start_time"][qid] = time.time()
if qid not in st.session_state["book_no_hint_flag"]:
    st.session_state["book_no_hint_flag"][qid] = True

elapsed = st.session_state["book_time_spent"].get(qid)
if elapsed is None:
    elapsed = time.time() - st.session_state["book_start_time"][qid]

# --- مصدر مخفي تقرأ منه لوحة الأيقونتين (نص التمرين + القوانين) ---
_sb_total = len(q["steps"])
_sb_at = min(st.session_state.get(f"book_step_prog_{qid}", 1), _sb_total)
_sb_pct = int(((_sb_at - 1) / _sb_total) * 100)
_sb_chip = "🧠 تمرين مفاهيمي ورمزي" if qtype == "proof" else "🧮 تمرين حسابي تفاعلي"
_stmt_src = (
    f'<div class="sb-stmt"><span class="sb-chip">{_sb_chip}</span>'
    f'<h4>{q["title"]}</h4><p>{q["text"]}</p>{figure_html(qid)}'
    f'<div class="qprogress-bg"><div class="qprogress-fill" style="width:{_sb_pct}%;"></div></div>'
    f'<small>الخطوة {_sb_at} من {_sb_total}</small></div>'
)
_laws_src = "".join(
    f'<div class="formula-row"><span class="f-name">{_n}</span>'
    f'<span class="f-eq eq-flow-{equation_direction(_f)}" 'f'dir="{equation_direction(_f)}">{plain_to_eq(_f)}</span></div>'
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
    step_state_key = f"book_step_prog_{qid}"
    if step_state_key not in st.session_state:
        st.session_state[step_state_key] = 1
    current_step_user_at = st.session_state[step_state_key]

    q_progress_pct = int(((current_step_user_at - 1) / len(q["steps"])) * 100)

    top_l, top_r = st.columns([4, 1])
    with top_l:
        # نبني البطاقة كسلسلة HTML متصلة بلا أسطر مزاحة. عند غياب صورة السؤال
        # كان السطر الفارغ يجعل Markdown يعرض شريط التقدم كنص برمجي ظاهر.
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
    with st.container(key="book_steps_anchor"):
        st.markdown('<h3 id="phys-steps-anchor">📝 مراحل الحل والتعويض:</h3>', unsafe_allow_html=True)
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

            attempts_so_far = st.session_state["book_attempts"].get(step_key, 0)
            hint_lvl_current = st.session_state["book_hint_level"].get(step_key, 0)
            potential_points = calc_points(attempts_so_far + 1, hint_lvl_current)
            _mn = 0
            if step.get("micro"):
                st.markdown(micro_html(step, final_mode="none", qid=qid), unsafe_allow_html=True)
                _mn = len(step["micro"])
            user_blank_inputs = []
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
                            value=None, placeholder="..", label_visibility="collapsed"
                        )
                        user_blank_inputs.append(val)
                    col_idx += 1
                    with cols[col_idx]:
                        st.markdown(f"<div class='formula-text'>{eq_frag(b['suffix'])}</div>", unsafe_allow_html=True)
                    col_idx += 1

            _mn2 = 0
            if step.get("micro2"):
                st.markdown(
                    micro_html(step, final_mode="none", field="micro2", start=_mn + 1, qid=qid),
                    unsafe_allow_html=True,
                )
                _mn2 = len(step["micro2"])

            user_root_val = None
            if step.get("has_root"):
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
                            value=None, placeholder="..", label_visibility="collapsed"
                        )
                    with r_c3:
                        st.markdown(f"<div class='formula-text'>{eq_frag(step['root_suffix'])}</div>", unsafe_allow_html=True)

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
                        value=None, placeholder="..", label_visibility="collapsed"
                    )
                with rc3:
                    st.markdown(f"<div class='formula-text'>{eq_frag(_runit)}</div>", unsafe_allow_html=True)

            with st.container(key="step_actions_row"):
                _bc1, _bc2 = st.columns(2)
                with _bc1:
                    check_btn = st.button("تحقق 🎯", key=f"btn_{qid}_{s_num}", use_container_width=True)
                with _bc2:
                    hint_btn = st.button("💡 تلميح", key=f"hint_{qid}_{s_num}", use_container_width=True)

            st.markdown(f'<span class="points-chip">🎯 نقاط هذه المحاولة المتوقعة: {potential_points}</span>', unsafe_allow_html=True)

            if hint_btn:
                new_level = min(3, hint_lvl_current + 1)
                st.session_state["book_hint_level"][step_key] = new_level
                st.session_state["book_no_hint_flag"][qid] = False
                st.rerun()

            if hint_lvl_current >= 1:
                if hint_lvl_current == 1:
                    msg = "ابدأ بالتعويض عن كل قيمة معطاة في نص السؤال داخل مكانها الصحيح في القانون أعلاه، بنفس الترتيب من اليسار لليمين."
                elif hint_lvl_current == 2:
                    substituted = step["prefix"]
                    for b in step["blanks"]:
                        substituted += f"({b['target']})" + b["suffix"]
                    msg = f"عوّض القيم كالتالي: {substituted}"
                else:
                    msg = step["hint"]
                st.markdown(f'<div class="hint-box">💡 <b>تلميح (مستوى {hint_lvl_current}):</b> {msg}</div>', unsafe_allow_html=True)
                if hint_lvl_current < 3:
                    st.caption("بحاجة لمساعدة أكبر؟ اضغط 💡 تلميح مرة أخرى.")

            if check_btn:
                st.session_state["book_attempts"][step_key] = st.session_state["book_attempts"].get(step_key, 0) + 1
                attempts_now = st.session_state["book_attempts"][step_key]

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
                    st.session_state["book_total_xp"] += pts
                    if attempts_now == 1 and hint_lvl_current == 0:
                        st.session_state["book_streak"] += 1
                    else:
                        st.session_state["book_streak"] = 0
                    if st.session_state["book_streak"] == 3:
                        award_badge("🔥 3 إجابات متتالية بلا أخطاء")
                    if st.session_state["book_streak"] == 5:
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
        if qid not in st.session_state["book_completed_questions"]:
            st.session_state["book_completed_questions"].add(qid)
            duration = time.time() - st.session_state["book_start_time"][qid]
            st.session_state["book_time_spent"][qid] = duration
            st.session_state["book_total_xp"] += 15
            if len(st.session_state["book_completed_questions"]) == 1:
                award_badge("🏅 أول تمرين مكتمل")
            if st.session_state["book_no_hint_flag"].get(qid, False):
                award_badge("⭐ إتقان بلا تلميحات")
            if len(st.session_state["book_completed_questions"]) == TOTAL_QUESTIONS:
                award_badge("🎓 إتقان كامل لجميع التمارين")
            st.balloons()

        dur = st.session_state["book_time_spent"].get(qid, 0)
        st.success(f"🎉 ممتاز جداً! أتقنت هذا التمرين خلال {fmt_time(dur)} (+15 XP مكافأة إنجاز).")
        if st.button("🔄 إعادة حل التمرين من البداية", key=f"restart_{qid}"):
            reset_question(qid, "interactive")
            st.rerun()

# ==========================================================
# 8ب. مسار مسائل الإثبات النظري (رمزي/عددي + LaTeX)
# ==========================================================
else:
    step_state_key = f"book_step_prog_{qid}"
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
        if st.button("🔁 إعادة حل هذا التمرين", key=f"reset_{qid}", use_container_width=True):
            reset_question(qid, "proof")
            st.rerun()

    st.markdown("---")
    with st.container(key="book_steps_anchor"):
        st.markdown('<h3 id="phys-steps-anchor">🧠 خطوات الفهم والتطبيق الرمزي:</h3>', unsafe_allow_html=True)
    st.caption("الخطوات مرتبة من اليمين لليسار: مكتملة ✅ ← نشطة 🔵 ← مقفلة 🔒  |  أكمل الفراغ الرمزي أو العددي في كل خطوة لإثبات فهمك.")

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

            st.markdown(derive_html(qid, step), unsafe_allow_html=True)

            if explain_mode:
                st.markdown(f'<div class="explain-box">💬 {step.get("label", "")}</div>', unsafe_allow_html=True)

            _plabel = step.get("label", "")
            if step.get("micro"):
                st.markdown(micro_html(step, final_say=_plabel, qid=qid), unsafe_allow_html=True)
            else:
                st.markdown(
                    micro_html(step, field="__nomicro__", final_say=_plabel, qid=qid),
                    unsafe_allow_html=True,
                )

            attempts_so_far = st.session_state["book_attempts"].get(step_key, 0)
            hint_lvl_current = st.session_state["book_hint_level"].get(step_key, 0)
            potential_points = calc_points(attempts_so_far + 1, hint_lvl_current)

            with st.container(key="formula_proof_row"):
                fc1, fc2, fc3 = st.columns([2, 1.3, 2])
                with fc1:
                    st.markdown(f"<div class='formula-text'>{eq_frag(step['prefix'])}</div>", unsafe_allow_html=True)
                with fc2:
                    user_val = st.text_input(
                        "input_field", key=f"proofinput_{step_key}",
                        placeholder="أدخل الإجابة...", label_visibility="collapsed"
                    )
                with fc3:
                    st.markdown(f"<div class='formula-text'>{eq_frag(step['suffix'])}</div>", unsafe_allow_html=True)

            btn_col, hint_col = st.columns(2)
            with btn_col:
                check_btn = st.button("تحقق 🎯", key=f"btn_{step_key}", use_container_width=True)
            with hint_col:
                hint_btn = st.button("💡 تلميح", key=f"hint_{step_key}", use_container_width=True)

            st.markdown(f'<span class="points-chip">🎯 نقاط هذه المحاولة المتوقعة: {potential_points}</span>', unsafe_allow_html=True)

            if hint_btn:
                st.session_state["book_hint_level"][step_key] = min(2, hint_lvl_current + 1)
                st.session_state["book_no_hint_flag"][qid] = False
                st.rerun()

            if hint_lvl_current >= 1:
                msg = step["hint"] if hint_lvl_current >= 2 else "راجع القانون/المعطى المذكور أعلاه جيداً قبل التعويض."
                st.markdown(f'<div class="hint-box">💡 <b>تلميح:</b> {msg}</div>', unsafe_allow_html=True)
                if hint_lvl_current < 2:
                    st.caption("بحاجة لمساعدة أكبر؟ اضغط 💡 تلميح مرة أخرى.")

            if check_btn:
                st.session_state["book_attempts"][step_key] = st.session_state["book_attempts"].get(step_key, 0) + 1
                attempts_now = st.session_state["book_attempts"][step_key]

                if not user_val or user_val.strip() == "":
                    st.warning("الرجاء كتابة الإجابة أولاً داخل الفراغ!")
                else:
                    is_correct = False
                    if step["type"] == "symbol":
                        case_sens = step.get("case_sensitive", False)
                        clean_user = normalize_symbol(user_val, case_sens)
                        clean_targets = [
                            normalize_symbol(candidate, case_sens)
                            for candidate in str(step["target"]).split("|")
                        ]
                        is_correct = (clean_user in clean_targets)
                    else:  # number
                        try:
                            num_float = float(user_val.replace(",", "."))
                            is_correct = abs(num_float - step["target"]) <= step["tol"]
                        except ValueError:
                            st.error("يرجى كتابة رقم عددي صحيح (مثال: 0.889 أو 36)!")
                            is_correct = None

                    if is_correct:
                        pts = calc_points(attempts_now, hint_lvl_current)
                        st.session_state["book_total_xp"] += pts
                        if attempts_now == 1 and hint_lvl_current == 0:
                            st.session_state["book_streak"] += 1
                        else:
                            st.session_state["book_streak"] = 0
                        if st.session_state["book_streak"] == 3:
                            award_badge("🔥 3 إجابات متتالية بلا أخطاء")
                        if st.session_state["book_streak"] == 5:
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
        if qid not in st.session_state["book_completed_questions"]:
            st.session_state["book_completed_questions"].add(qid)
            duration = time.time() - st.session_state["book_start_time"][qid]
            st.session_state["book_time_spent"][qid] = duration
            st.session_state["book_total_xp"] += 15
            if len(st.session_state["book_completed_questions"]) == 1:
                award_badge("🏅 أول تمرين مكتمل")
            award_badge("🧠 عقل تحليلي (أتقن تمرينًا مفاهيميًا)")
            if st.session_state["book_no_hint_flag"].get(qid, True):
                award_badge("⭐ إتقان بلا تلميحات")
            if len(st.session_state["book_completed_questions"]) == TOTAL_QUESTIONS:
                award_badge("🎓 إتقان كامل لجميع التمارين")
            st.balloons()

        dur = st.session_state["book_time_spent"].get(qid, 0)
        st.success(f"🎉 أحسنت! أتممت هذا التمرين خلال {fmt_time(dur)} (+15 XP مكافأة إتمام).")
        if st.button("🔄 إعادة حل التمرين من البداية", key=f"restart_{qid}"):
            reset_question(qid, "proof")
            st.rerun()

# ==========================================================
# 9. شهادة الإنجاز عند إتمام جميع التمارين
# ==========================================================
if len(st.session_state["book_completed_questions"]) == TOTAL_QUESTIONS:
    st.snow()
    name_display = st.session_state["book_student_name"] or "طالب مجتهد"
    total_time = sum(st.session_state["book_time_spent"].values())
    level_label, _, _ = get_level(st.session_state["book_total_xp"])

    st.markdown(f"""
    <div class="cert-box">
        <h2>🏆 شهادة إتمام</h2>
        <p style="font-size:1.2rem;">تُمنح هذه الشهادة إلى الطالب/ـة</p>
        <h3>{name_display}</h3>
        <p>لإتمامه/ـا بنجاح جميع <b>تمارين الكتاب المدرسي للوحدة الأولى</b></p>
        <p>المستوى: <b>{level_label}</b> &nbsp;|&nbsp; إجمالي النقاط: <b>{st.session_state["book_total_xp"]} XP</b> &nbsp;|&nbsp; الوقت الكلي: <b>{fmt_time(total_time)}</b></p>
    </div>
    """, unsafe_allow_html=True)

    cert_text = f"""شهادة إتمام
=================
الطالب/ـة: {name_display}
الوحدة: الأولى — البناء الإلكتروني للذرة
المسار: تمارين الكتاب المدرسي (1–20)
عدد التمارين المكتملة: {len(st.session_state["book_completed_questions"])} / {TOTAL_QUESTIONS}
إجمالي نقاط الخبرة: {st.session_state["book_total_xp"]} XP
المستوى: {level_label}
الوقت الكلي: {fmt_time(total_time)}
الأوسمة: {', '.join(sorted(st.session_state["book_badges"])) if st.session_state["book_badges"] else "لا يوجد"}
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
  var AR_RE = /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFEFF]/;
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
  function elementEquationDirection(el) {
    if (!el) return 'ltr';
    if (el.classList && (el.classList.contains('eq-rtl') || el.classList.contains('eq-flow-rtl'))) return 'rtl';
    if (el.classList && (el.classList.contains('eq-ltr') || el.classList.contains('eq-flow-ltr'))) return 'ltr';
    var text = el.textContent || '';
    var pos = -1, marks = ['=', '⇒', '⇔', '≈', '≠', '≤', '≥', '<', '>'];
    for (var i = 0; i < marks.length; i++) {
      var p = text.indexOf(marks[i]);
      if (p >= 0 && (pos < 0 || p < pos)) pos = p;
    }
    var head = pos >= 0 ? text.slice(0, pos) : text;
    if (AR_RE.test(head)) return 'rtl';
    if (/[A-Za-z\u0370-\u03FF\u2100-\u214F]/.test(head)) return 'ltr';
    return AR_RE.test(text) ? 'rtl' : 'ltr';
  }

  function fixEquationDirections() {
    var nodes = doc.querySelectorAll('.eq, .law-eq, .micro-eq, .result-eq, .eq-inline, .f-eq, .formula-text');
    for (var i = 0; i < nodes.length; i++) {
      var d = elementEquationDirection(nodes[i]);
      css(nodes[i], {
        'direction': d,
        'unicode-bidi': 'isolate',
        'text-align': d === 'rtl' ? 'right' : 'left'
      });
      nodes[i].setAttribute('dir', d);
      nodes[i].classList.remove(d === 'rtl' ? 'eq-flow-ltr' : 'eq-flow-rtl');
      nodes[i].classList.add('eq-flow-' + d);
    }
  }

  /* ===== معادلات LaTeX: عربية RTL ولاتينية LTR ===== */
  function fixLatex() {
    var hosts = doc.querySelectorAll('[data-testid="stLatex"], .stLatex, .katex-display, .katex, .katex-html');
    for (var i = 0; i < hosts.length; i++) {
      var el = hosts[i];
      var d = elementEquationDirection(el);
      css(el, { 'direction': d, 'unicode-bidi': 'isolate' });
      if (el.classList.contains('katex-display') ||
          el.getAttribute('data-testid') === 'stLatex' ||
          el.classList.contains('stLatex')) {
        css(el, { 'text-align': d === 'rtl' ? 'right' : 'center' });
      }
      var host = el.parentElement;
      if (host && host.getAttribute('data-testid') === 'stMarkdownContainer') {
        css(host, { 'direction': d, 'text-align': d === 'rtl' ? 'right' : 'center' });
      }
    }
    var msub = doc.querySelectorAll('.katex .msupsub, .katex .vlist-t, .katex .vlist');
    for (var j = 0; j < msub.length; j++) {
      css(msub[j], { 'unicode-bidi': 'isolate', 'text-align': 'left' });
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
      var rowDir = AR_RE.test(row.textContent || '') ? 'rtl' : 'ltr';
      css(row, {
        'direction': rowDir,
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
    inp.addEventListener('focus', function () { wantFocusAt = Date.now(); });
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

  function fracVal(t) {
    var m = /^(-?[0-9]+(?:\.[0-9]+)?)\/(-?[0-9]+(?:\.[0-9]+)?)$/.exec(t);
    if (m) { var d = parseFloat(m[2]); return (d === 0) ? null : (parseFloat(m[1]) / d); }
    if (/^-?[0-9]+(?:\.[0-9]+)?$/.test(t)) { return parseFloat(t); }
    return null;
  }

  function sameAns(a, b, cs) {
    var x = normAns(a, cs), y = normAns(b, cs);
    if (x === y) { return true; }
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
        if (lk && lk.indexOf('chemBook0:') === 0) { ks.push(lk); }
      }
      for (li = 0; li < ks.length; li++) { win.sessionStorage.removeItem(ks[li]); }
    } catch (e) { }
  }

  function microKey(line) {
    var pk = line.getAttribute ? line.getAttribute('data-pk') : null;
    if (pk) { return 'chemBook1:' + pk; }
    var card = line.closest('[class*="_stepstate_"]');
    var base = card ? String(card.className || '') : 'x';
    var idx = 0, kids = line.parentElement ? line.parentElement.children : [];
    for (var i = 0; i < kids.length; i++) { if (kids[i] === line) { idx = i; break; } }
    var bx = line.parentElement;
    var mk = (bx && bx.getAttribute) ? (bx.getAttribute('data-mk') || 'm') : 'm';
    var sig = String(line.dataset.ans || '') + '|' + String(line.dataset.cs || '');
    var hh = 0;
    for (var q = 0; q < sig.length; q++) { hh = ((hh << 5) - hh + sig.charCodeAt(q)) | 0; }
    return 'chemBook1:' + base.replace(/\s+/g, '_') + ':' + mk + ':' + idx + ':' + (hh >>> 0).toString(36);
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
    inp.addEventListener('focus', function () { wantFocusAt = Date.now(); });
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
  var DOCK_VERSION = 'chem-book-all-exercises-final-v9';
  var TOOL_RUN_ID = DOCK_VERSION + '-' + String(Date.now()) + '-' + String(Math.random());
  win.__chemBookToolRun = TOOL_RUN_ID;
  var dockSt = null;
  var ownedDock = null;

  function dockRead() {
    if (dockSt) return dockSt;
    var v = 'stmt';
    try { v = win.sessionStorage.getItem('chemBookDockPaneFinalV9') || 'stmt'; } catch (e) { v = 'stmt'; }
    if (v !== 'laws' && v !== 'stmt' && v !== 'calc' && v !== 'none') v = 'stmt';
    dockSt = v;
    return v;
  }

  function dockWrite(v) {
    dockSt = v;
    try { win.sessionStorage.setItem('chemBookDockPaneFinalV9', v); } catch (e) {}
  }

  /* \u0645\u0633\u062a\u0648\u0649 \u0627\u0644\u0628\u062f\u0627\u064a\u0629: \u0639\u0646\u0648\u0627\u0646 \u0645\u0631\u0627\u062d\u0644 \u0627\u0644\u062a\u0639\u0648\u064a\u0636 / \u062e\u0637\u0648\u0627\u062a \u0627\u0644\u0625\u062b\u0628\u0627\u062a */
  function anchorEl() {
    /* الخيار الأقوى: class يولدها st.container(key=...) ولا ينزعها Markdown. */
    var keyed = doc.querySelector('.st-key-book_steps_anchor');
    if (keyed) return keyed.querySelector('h1, h2, h3') || keyed;

    var a = doc.getElementById('phys-steps-anchor');
    if (a) return a;

    /* دعم كل عناوين المسارين الحسابي والرمزي. */
    var hs = doc.querySelectorAll('h1, h2, h3');
    var needles = [
      'مراحل الحل والتعويض',
      'خطوات الفهم والتطبيق الرمزي',
      'مراحل التعويض',
      'خطوات الإثبات'
    ];
    for (var i = 0; i < hs.length; i++) {
      var t = hs[i].textContent || '';
      for (var j = 0; j < needles.length; j++) {
        if (t.indexOf(needles[j]) >= 0) return hs[i];
      }
    }

    /* آخر بديل: بطاقة السؤال نفسها؛ لا نعيد null كي لا تختفي الأيقونات. */
    return doc.querySelector('.q-card') ||
           doc.querySelector('section[data-testid="stMain"] div[data-testid="stMainBlockContainer"]') ||
           doc.body;
  }

  var calcMemory = { last: '0', angle: 'DEG', second: false, history: [] };

  function calcHtml() {
    var keys = [
      ['2nd','second','sci'], ['DEG','mode','mode'], ['Ans','ans','sci'], ['C','c','fn'], ['⌫','back','fn'],
      ['sin','sin','sci','sin'], ['cos','cos','sci','cos'], ['tan','tan','sci','tan'], ['log','log','sci'], ['ln','ln','sci'],
      ['√','sqrt','sci'], ['x²','sq','sci'], ['xʸ','pow','sci'], ['10ˣ','exp10','sci'], ['eˣ','ex','sci'],
      ['π','pi','sci'], ['e','euler','sci'], ['(', '(','op'], [')',')','op'], ['1/x','recip','sci'],
      ['7','7','num'], ['8','8','num'], ['9','9','num'], ['÷','/','op'], ['EXP','exp','sci'],
      ['4','4','num'], ['5','5','num'], ['6','6','num'], ['×','*','op'], ['|x|','abs','sci'],
      ['1','1','num'], ['2','2','num'], ['3','3','num'], ['−','-','op'], ['n!','fact','sci'],
      ['±','neg','sci'], ['0','0','num'], ['.','.','num'], ['+','+','op'], ['=','eq','eq']
    ];
    var h = '<div class="phys-calc" tabindex="0" data-expr="">' +
      '<div class="phys-calc-top"><span class="phys-calc-badge">SCIENTIFIC</span>' +
      '<span class="phys-calc-mode-note">DEG/RAD · ذاكرة Ans</span></div>' +
      '<div class="phys-calc-disp"><div class="phys-calc-expr">0</div>' +
      '<div class="phys-calc-val">0</div></div>' +
      '<div class="phys-calc-history"></div><div class="phys-calc-pad">';
    for (var i=0;i<keys.length;i++) {
      var cls='phys-calc-key';
      if (keys[i][2]==='sci') cls+=' k-sci';
      if (keys[i][2]==='op') cls+=' k-op';
      if (keys[i][2]==='fn') cls+=' k-fn';
      if (keys[i][2]==='mode') cls+=' k-mode';
      if (keys[i][2]==='eq') cls+=' k-eq';
      var extra = keys[i][3] ? ' data-trig="'+keys[i][3]+'"' : '';
      h += '<button type="button" class="'+cls+'" data-k="'+keys[i][1]+'"'+extra+'>'+keys[i][0]+'</button>';
    }
    return h + '</div><div class="phys-calc-help">يدعم الدوال المثلثية، اللوغاريتمات، القوى، الجذور، المضروب، النسب المئوية والصيغة العلمية.</div></div>';
  }

  function calcPretty(e) {
    return String(e||'')
      .replace(/ASIN/g,'sin⁻¹').replace(/ACOS/g,'cos⁻¹').replace(/ATAN/g,'tan⁻¹')
      .replace(/SIN/g,'sin').replace(/COS/g,'cos').replace(/TAN/g,'tan')
      .replace(/SQRT/g,'√').replace(/LOG/g,'log').replace(/LN/g,'ln').replace(/ABS/g,'abs')
      .replace(/EULER/g,'e').replace(/PI/g,'π').replace(/ANS/g,'Ans')
      .replace(/\^/g,'ʸ').replace(/\*/g,'×').replace(/\//g,'÷');
  }

  function calcNumber(v) {
    if (typeof v!=='number' || !isFinite(v)) return '';
    if (Math.abs(v)<1e-14) v=0;
    var a=Math.abs(v);
    if ((a!==0 && a<1e-8) || a>=1e12) {
      return v.toExponential(10).replace(/\.0+e/,'e').replace(/(\.\d*?)0+e/,'$1e');
    }
    return String(Number(v.toPrecision(12)));
  }

  function calcEval(e,pane) {
    var src=String(e||'').trim();
    if (!src) return '';
    var residue=src
      .replace(/ASIN|ACOS|ATAN|SQRT|EULER|ANS|SIN|COS|TAN|LOG|LN|ABS|PI/g,'')
      .replace(/(?:\d+(?:\.\d*)?|\.\d+)(?:e[+\-]?\d+)?/gi,'0');
    if (!/^[0+\-*/^().,\s]*$/.test(residue)) return '';
    var mode=(pane&&pane.getAttribute('data-angle'))||calcMemory.angle||'DEG';
    var toRad=function(x){return mode==='DEG'?x*Math.PI/180:x;};
    var fromRad=function(x){return mode==='DEG'?x*180/Math.PI:x;};
    var ans=parseFloat(calcMemory.last||'0'); if (!isFinite(ans)) ans=0;
    var code=src.replace(/\^/g,'**');
    try {
      var fn=new win.Function('SIN','COS','TAN','ASIN','ACOS','ATAN','LOG','LN','SQRT','ABS','PI','EULER','ANS',
        '"use strict"; return ('+code+');');
      var v=fn(function(x){return Math.sin(toRad(x));},function(x){return Math.cos(toRad(x));},
        function(x){return Math.tan(toRad(x));},function(x){return fromRad(Math.asin(x));},
        function(x){return fromRad(Math.acos(x));},function(x){return fromRad(Math.atan(x));},
        function(x){return Math.log10(x);},function(x){return Math.log(x);},Math.sqrt,Math.abs,
        Math.PI,Math.E,ans);
      return (typeof v==='number'&&isFinite(v))?calcNumber(v):'';
    } catch(err){return '';}
  }

  function calcSetSecond(d) {
    var pane=d.querySelector('.phys-calc'); if(!pane)return;
    var second=pane.getAttribute('data-second')==='1';
    var trig=pane.querySelectorAll('[data-trig]');
    for(var i=0;i<trig.length;i++){
      var base=trig[i].getAttribute('data-trig');
      trig[i].textContent=second?(base+'⁻¹'):base;
      trig[i].setAttribute('data-k',second?('a'+base):base);
    }
    var b=pane.querySelector('[data-k="second"]');
    if(b) b.style.boxShadow=second?'inset 0 0 0 2px #4f46e5':'';
  }

  function calcHistoryPaint(pane) {
    var h=pane.querySelector('.phys-calc-history'); if(!h)return;
    var rows=calcMemory.history.slice(-3).reverse();
    h.innerHTML=rows.map(function(x){return '<div>'+calcPretty(x[0])+' = <b>'+x[1]+'</b></div>';}).join('');
  }

  function calcPaint(d) {
    var pane=d.querySelector('.phys-calc'); if(!pane)return;
    if(!pane.getAttribute('data-angle')) pane.setAttribute('data-angle',calcMemory.angle||'DEG');
    if(!pane.getAttribute('data-second')) pane.setAttribute('data-second',calcMemory.second?'1':'0');
    var e=pane.getAttribute('data-expr')||'';
    var ex=pane.querySelector('.phys-calc-expr'),vl=pane.querySelector('.phys-calc-val');
    if(ex) ex.textContent=calcPretty(e)||'0';
    if(vl){var v=calcEval(e,pane);vl.textContent=e===''?'0':(v===''?'…':v);}
    var mb=pane.querySelector('[data-k="mode"]'); if(mb)mb.textContent=pane.getAttribute('data-angle')||'DEG';
    calcHistoryPaint(pane); calcSetSecond(d);
  }

  function calcBack(e) {
    var toks=['EULER','SQRT(','ASIN(','ACOS(','ATAN(','SIN(','COS(','TAN(','LOG(','ABS(','ANS','LN(','PI'];
    for(var i=0;i<toks.length;i++) if(e.slice(-toks[i].length)===toks[i]) return e.slice(0,-toks[i].length);
    return e.slice(0,-1);
  }

  function calcUnary(pane,e,k) {
    var base=e===''?(calcMemory.last||''):calcEval(e,pane),v=parseFloat(base);
    if(base===''||!isFinite(v)){return e;}
    var out='';
    if(k==='sqrt'&&v>=0)out=calcNumber(Math.sqrt(v));
    else if(k==='sq')out=calcNumber(v*v);
    else if(k==='recip'&&v!==0)out=calcNumber(1/v);
    else if(k==='abs')out=calcNumber(Math.abs(v));
    else if(k==='neg')out=calcNumber(-v);
    else if(k==='percent')out=calcNumber(v/100);
    else if(k==='exp10')out=calcNumber(Math.pow(10,v));
    else if(k==='ex')out=calcNumber(Math.exp(v));
    else if(k==='fact'&&v>=0&&v<=170&&Math.floor(v)===v){var f=1;for(var i=2;i<=v;i++)f*=i;out=calcNumber(f);}
    return out===''?e:out;
  }

  function calcKey(d,k) {
    var pane=d.querySelector('.phys-calc'); if(!pane)return;
    var e=pane.getAttribute('data-expr')||'';
    if(k==='c')e='';
    else if(k==='back')e=calcBack(e);
    else if(k==='mode'){
      calcMemory.angle=(pane.getAttribute('data-angle')==='RAD')?'DEG':'RAD';
      pane.setAttribute('data-angle',calcMemory.angle);
    }
    else if(k==='second'){
      calcMemory.second=!(pane.getAttribute('data-second')==='1');
      pane.setAttribute('data-second',calcMemory.second?'1':'0');
    }
    else if(['sqrt','sq','recip','abs','neg','percent','exp10','ex','fact'].indexOf(k)>=0)e=calcUnary(pane,e,k);
    else if(k==='eq'){
      var v=calcEval(e,pane);
      if(v!==''){calcMemory.history.push([e,v]);if(calcMemory.history.length>12)calcMemory.history.shift();calcMemory.last=v;e=v;}
    }
    else if(k==='ans')e+='ANS';
    else if(k==='pi')e+='PI';
    else if(k==='euler')e+='EULER';
    else if(k==='pow')e+='^';
    else if(k==='exp')e+='e';
    else if(k==='sin')e+='SIN(';
    else if(k==='cos')e+='COS(';
    else if(k==='tan')e+='TAN(';
    else if(k==='asin')e+='ASIN(';
    else if(k==='acos')e+='ACOS(';
    else if(k==='atan')e+='ATAN(';
    else if(k==='log')e+='LOG(';
    else if(k==='ln')e+='LN(';
    else {if(e.length<180)e+=k;}
    pane.setAttribute('data-expr',e); calcPaint(d);
  }

  function calcKeyboard(d,e) {
    var k=e.key;
    if(/^[0-9.+\-*/()^]$/.test(k)){calcKey(d,k);e.preventDefault();return;}
    if(k==='Enter'||k==='='){calcKey(d,'eq');e.preventDefault();}
    else if(k==='Backspace'){calcKey(d,'back');e.preventDefault();}
    else if(k==='Escape'||k==='Delete'){calcKey(d,'c');e.preventDefault();}
    else if(k==='%'){calcKey(d,'percent');e.preventDefault();}
  }

  function paneHtml(kind) {
    if (kind === 'calc') {
      return '<div class="phys-pane-head">\ud83e\uddee \u0622\u0644\u0629 \u062d\u0627\u0633\u0628\u0629 \u0639\u0644\u0645\u064a\u0629</div>' + calcHtml();
    }
    var s = doc.getElementById(kind === 'laws' ? 'phys-src-laws' : 'phys-src-stmt');
    var inner = s ? s.innerHTML : '';
    var ttl = (kind === 'laws') ? '\ud83d\udcd0 \u0648\u0631\u0642\u0629 \u0627\u0644\u0642\u0648\u0627\u0646\u064a\u0646 \u0627\u0644\u0633\u0631\u064a\u0639\u0629' : '\ud83d\udcc4 \u0646\u0635 \u0627\u0644\u062a\u0645\u0631\u064a\u0646';
    return '<div class="phys-pane-head">' + ttl + '</div>' + inner;
  }

  function dockBuild() {
    var d = doc.getElementById(DOCK_ID);
    if (d && d !== ownedDock) {
      try { d.parentNode.removeChild(d); } catch (e) {}
      d = null;
    }
    if (d) return d;
    d = doc.createElement('div');
    d.id = DOCK_ID;
    d.setAttribute('data-tool-version', DOCK_VERSION);
    ownedDock = d;
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
        '<div class="phys-ic-wrap" data-kind="calc" title="\u0622\u0644\u0629 \u062d\u0627\u0633\u0628\u0629 \u0639\u0644\u0645\u064a\u0629">' +
          '<button type="button" class="phys-ic phys-ic-calc">\ud83e\uddee</button>' +
          '<span class="phys-ic-lbl lbl-calc">\u0622\u0644\u0629 \u062d\u0627\u0633\u0628\u0629 \u0639\u0644\u0645\u064a\u0629</span>' +
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
      var cp = d.querySelector('.phys-calc');
      if (cp) { try { cp.focus({preventScroll:true}); } catch (e2) {} }
    });
    d.addEventListener('keydown', function (e) {
      if (dockRead() === 'calc' && !(e.target && /INPUT|TEXTAREA/.test(e.target.tagName || ''))) calcKeyboard(d, e);
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
    if (kind === 'calc') { calcPaint(d); }
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
    if ((!ar.width && !ar.height) || an === doc.body) top = Math.max(off, 132);

    var railW = 96;
    var w = 0;
    if (open) {
      w = Math.max(360, Math.min(440, Math.round(vw * 0.32)));
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
    if (win.__chemBookToolRun !== TOOL_RUN_ID) return;
    fixSubscripts();
    fixEquationDirections();
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
render_exercise_footer_v18("pages/chemistry_textbook_exercises.py")
