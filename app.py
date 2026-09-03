import streamlit as st
import streamlit.components.v1 as components
from ui_theme_v13 import apply_ui_theme
from exercise_ui_v18 import (apply_exercise_ui_v18, render_exercise_header_v18, render_question_card_v18, render_exercise_footer_v18)
import random
import time
import json
import hashlib
import uuid
from datetime import datetime
from pathlib import Path

# ==========================================================
# 0. هوية المنصة  —  غيّر هذه السطور وحدها لتغيير الاسم في كل المنصة
# ==========================================================
APP_NAME     = "الطالب الصامد"
APP_ICON     = "🛡️"
APP_TAGLINE  = "لا تتوقّف عند أول خطأ"
APP_SUBTITLE = "الدعم التعليمي في الفيزياء والكيمياء · الصفوف 6 — 12"
APP_UNIT     = "الفيزياء · الصف الثاني عشر · وحدة الزخم الخطي والدفع"

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
questions_db = [
    {
        "id": "q1", "type": "interactive",
        "title": "السؤال الأول: الحركة تحت تأثير الجاذبية والزخم",
        "text": "قُذف جسم كتلته (2 kg) رأسياً للأعلى بسرعة (10 m/s). أحسب زخم الجسم عندما يصبح على ارتفاع (1 m) عن سطح الأرض؟ (اعتبر تسارع الجاذبية g = 10 m/s²)",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: حساب السرعة v عند ارتفاع 1 متر",
                "micro": [
                    ('نطبّق قانون السقوط الحر على الحركة الصاعدة:', 'v² = v₀² - 2·g·h'),
                    ('نحدّد السرعة الابتدائية v₀ من نص التمرين (m/s):', 'v₀ = ?', '10'),
                    ('نحدّد الارتفاع h المطلوب (m):', 'h = ?', '1'),
                ],
                "micro2": [
                    ('احسب ما تحت الجذر ثم اكتب ناتج مربّع السرعة:', 'v² = ?', '80'),
                ],
                "law": "المعادلة: v² = v₀² - 2·g·h",
                "simple_explain": "نعوض بالسرعة الابتدائية وقيمة الجاذبية والارتفاع داخل القانون، ثم نأخذ الجذر التربيعي للناتج لنحصل على السرعة.",
                "prefix": "v² = (",
                "blanks": [
                    {"label": "v0", "target": 10.0, "suffix": ")²-2×("},
                    {"label": "g", "target": 10.0, "suffix": ")×("},
                    {"label": "h", "target": 1.0, "suffix": ")"}
                ],
                "has_root": True, "root_prefix": "v = √(", "root_target": 80.0, "root_suffix": ")",
                "result_target": 8.94, "result_tol": 0.1,
                "result_label": "احسب الناتج النهائي للسرعة v (m/s):",
                "hint": "v² = (10)² - 2(10)(1) = 80  ⇒  v = √80 ≈ 8.94 m/s"
            },
            {
                "num": 2, "title": "الخطوة 2: حساب الزخم الخطي p عند هذا الارتفاع",
                "micro": [
                    ('نطبّق قانون الزخم الخطي:', 'p = m · v'),
                    ('نعوّض الكتلة m (kg):', 'm = ?', '2'),
                    ('نستعمل السرعة v الناتجة عن الخطوة 1 (m/s):', 'v = ?', '8.94|8,94|8.9|8,9'),
                ],
                "law": "المعادلة: p = m · v",
                "simple_explain": "نضرب كتلة الجسم في السرعة التي حسبناها في الخطوة السابقة لنحصل على الزخم.",
                "prefix": "p = (",
                "blanks": [
                    {"label": "m", "target": 2.0, "suffix": ")×("},
                    {"label": "v", "target": 8.94, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 17.88, "result_tol": 0.2, "alt_result_target": 18.0,
                "result_label": "احسب الناتج النهائي للزخم p (N.s):",
                "hint": "p = 2 kg × 8.94 m/s = 17.88 N.s"
            }
        ]
    },
    {
        "id": "q2", "type": "proof",
        "title": "السؤال الثاني: (إثبات) العلاقة بين الطاقة الحركية لجسمين",
        "text": "جسمان: كتلة الأول (m₁) وكتلة الثاني (2m₁). إذا عُلم أن الزخم الخطي للجسم الأول يساوي ثلثي الزخم الخطي للجسم الثاني (p₁ = ⅔ p₂)، وأن مجموع الطاقة الحركية للجسمين (68 J)، جد الطاقة الحركية للجسم الثاني K₂.",
        "steps": [
            {
                "num": 1, "type": "symbol",
                "title": "الخطوة 1: التعويض الرمزي عن p₁ بدلالة p₂",
                "law": "قانون الطاقة الحركية: K = p² / (2m)  ،  المعطى: p₁ = ⅔ p₂",
                "latex_preview": r"K_1 = \frac{(\frac{2}{3} \cdot \mathbf{?})^2}{2m_1}",
                "micro": [
                    ("نطبّق قانون الطاقة الحركية على الجسم الأول وحده. أكمل المقام:", "K₁ = p₁² / (2 ?)", "m1"),
                    ("وبما أن لدينا المعطى:", "p₁ = ⅔ p₂"),
                ],
                "label": "أدخل الرمز المناسب للزخم داخل القوس للتربيع:",
                "prefix": "K₁ = ( ⅔ ", "suffix": " )² / (2m₁)",
                "target": "p2",
                "completed_display": "K₁ = ( ⅔ p₂ )² / (2m₁)",
                "hint": "عوّض عن p₁ بالرمز p₂ حسب معطى السؤال (اكتب: p2)"
            },
            {
                "num": 2, "type": "symbol",
                "title": "الخطوة 2: التعويض الرمزي عن m₂ بدلالة m₁",
                "law": "قانون الطاقة الحركية: K = p² / (2m)",
                "latex_preview": r"K_2 = \frac{p_2^2}{2 \cdot (\mathbf{?})}",
                "micro": [
                    ("نطبّق القانون نفسه على الجسم الثاني وحده. أكمل المقام:", "K₂ = p₂² / (2 ?)", "m2"),
                    ("وبما أن لدينا المعطى:", "m₂ = 2m₁"),
                ],
                "label": "أدخل القيمة الرمزية للكتلة في المقام بدلاً من m₂:",
                "prefix": "K₂ = p₂² / 2(", "suffix": ")",
                "target": "2m1",
                "completed_display": "K₂ = p₂² / 2( 2m₁ )",
                "hint": "استخدم العلاقة الرمزية المعطاة للكتلة (اكتب: 2m1)"
            },
            {
                "num": 3, "type": "number",
                "title": "الخطوة 3: حساب نسبة الطاقة الحركية (K₁ / K₂) عددياً",
                "law": "بقسمة معادلة K₁ على K₂ واختصار الرموز المتشابهة (p₂ , m₁)",
                "latex_preview": r"\frac{K_1}{K_2} = \mathbf{?}",
                "micro": [
                    ("من الخطوة 1 بعد التربيع والاختصار:", "K₁ = (2/9) p₂² / m₁"),
                    ("ومن الخطوة 2 بعد الاختصار:", "K₂ = (1/4) p₂² / m₁"),
                    ("نقسم الأولى على الثانية فيُختصر p₂² و m₁. أكمل المقام:", "K₁ / K₂ = (2/9) / (?)", "1/4"),
                ],
                "label": "أدخل النسبة الحسابية العددية لـ (K₁ / K₂) — مقربة لثلاث منازل عشرية:",
                "prefix": "K₁ / K₂ = ", "suffix": "",
                "target": 0.889, "tol": 0.03,
                "completed_display": "K₁ / K₂ = 0.889  ⇒  K₁ = (8/9) K₂",
                "hint": "K₁/K₂ = [(4/9) ÷ 2] ÷ [1/4] = 8/9 ≈ 0.889"
            },
            {
                "num": 4, "type": "number",
                "title": "الخطوة 4: حل المعادلة المجموعية وإيجاد K₂",
                "law": "نستعمل معطى مجموع الطاقتين مع النسبة التي وجدتها في الخطوة 3",
                "latex_preview": r"K_2 = \mathbf{?} \text{ J}",
                "micro": [
                    ("المعطى الأخير هو مجموع الطاقتين:", "K₁ + K₂ = 68 J"),
                    ("ومن الخطوة 3 وجدنا:", "K₁ = (8/9) K₂"),
                    ("نعوّض عن K₁ فقط في المجموع. أكمل المعامل:", "? K₂ + K₂ = 68", "8/9"),
                    ("نجمع الحدّين المتشابهين. أكمل المعامل:", "? K₂ = 68", "17/9"),
                ],
                "label": "أدخل الناتج العددي النهائي للطاقة الحركية K₂ بوحدة الجول:",
                "prefix": "K₂ = ", "suffix": " J",
                "target": 36.0, "tol": 0.5,
                "completed_display": "K₂ = 36 J",
                "hint": "K₂ = (68 × 9) / 17 = 36 J"
            }
        ],
        "conclusion": "الطاقة الحركية للجسم الثاني K₂ = 36 J"
    },
    {
        "id": "q3", "type": "proof",
        "title": "السؤال الثالث: (إثبات) إيجاد الزخم الخطي من نسبة الطاقة الحركية",
        "text": "جسمان: كتلة الأول (2m) وكتلة الثاني (m). إذا عُلم أن الطاقة الحركية للجسم الأول تساوي مثلي الطاقة الحركية للجسم الثاني، وأن مجموع الزخم الخطي للجسمين (90 Kg.m/s)، جد الزخم الخطي للجسم الأول.",
        "steps": [
            {
                "num": 1, "type": "symbol",
                "title": "الخطوة 1: التعويض الرمزي عن K₁ بدلالة K₂",
                "law": "قانون الطاقة الحركية: p² = 2mK",
                "latex_preview": r"p_1^2 = 2(2m) \times \mathbf{?}",
                "micro": [
                    ("نطبّق القانون على الجسم الأول وحده. أكمل الكتلة:", "p₁² = 2 ? K₁", "m1"),
                    ("وبما أن لدينا معطى الكتلة:", "m₁ = 2m"),
                    ("نعوّض عن m₁ فقط ولا نغيّر باقي المعادلة:", "p₁² = 2 (?) K₁", "2m"),
                    ("ولدينا أيضاً معطى الطاقة:", "K₁ = 2K₂"),
                ],
                "label": "أدخل الرمز الصحيح بدلاً من K₁ (استخدم معطى المسألة):",
                "prefix": "p₁² = 2(2m) × (", "suffix": ")",
                "target": "2K2",
                "completed_display": "p₁² = 2(2m) × (2K₂) = 8mK₂",
                "hint": "بما أن K₁ = 2K₂، عوّض عنها بالرمز 2K2 (اكتب: 2K2)"
            },
            {
                "num": 2, "type": "number",
                "title": "الخطوة 2: حساب نسبة الزخمين (p₁ / p₂) عددياً",
                "law": "قانون الطاقة الحركية: p² = 2mK",
                "latex_preview": r"\frac{p_1}{p_2} = \mathbf{?}",
                "micro": [
                    ("نطبّق القانون على الجسم الثاني (كتلته m). أكمل الطاقة:", "p₂² = 2 m ?", "K2"),
                    ("ومن الخطوة 1 لدينا:", "p₁² = 8mK₂"),
                    ("نقسم فيُختصر m و K₂. أكمل الناتج:", "p₁² / p₂² = ?", "4"),
                ],
                "label": "أدخل قيمة النسبة p₁ / p₂:",
                "prefix": "p₁ / p₂ = ", "suffix": "",
                "target": 2.0, "tol": 0.1,
                "completed_display": "p₁ / p₂ = 2  ⇒  p₁ = 2p₂",
                "hint": "p₁/p₂ = √(8mK₂ / 2mK₂) = √4 = 2"
            },
            {
                "num": 3, "type": "number",
                "title": "الخطوة 3: إيجاد قيمة p₂ من معادلة المجموع",
                "law": "نستعمل معطى مجموع الزخمين مع النسبة التي وجدتها في الخطوة 2",
                "latex_preview": r"p_2 = \mathbf{?} \text{ Kg.m/s}",
                "micro": [
                    ("المعطى هو مجموع الزخمين:", "p₁ + p₂ = 90 Kg.m/s"),
                    ("ومن الخطوة 2 وجدنا:", "p₁ = 2p₂"),
                    ("نعوّض عن p₁ فقط. أكمل المعامل:", "? p₂ + p₂ = 90", "2"),
                    ("نجمع الحدّين المتشابهين. أكمل المعامل:", "? p₂ = 90", "3"),
                ],
                "label": "أدخل قيمة p₂ الناتجة (Kg.m/s):",
                "prefix": "p₂ = ", "suffix": " Kg.m/s",
                "target": 30.0, "tol": 0.5,
                "completed_display": "p₂ = 30 Kg.m/s",
                "hint": "3p₂ = 90  ⇒  p₂ = 30 Kg.m/s"
            },
            {
                "num": 4, "type": "number",
                "title": "الخطوة 4: إيجاد الزخم الخطي للجسم الأول p₁",
                "law": "بما أن p₁ = 2p₂",
                "latex_preview": r"p_1 = \mathbf{?} \text{ Kg.m/s}",
                "micro": [
                    ("لدينا العلاقة بين الزخمين:", "p₁ = 2p₂"),
                    ("نعوّض قيمة p₂ التي وجدناها. أكمل:", "p₁ = 2 · ?", "30"),
                ],
                "label": "أدخل الناتج النهائي لـ p₁ (Kg.m/s):",
                "prefix": "p₁ = ", "suffix": " Kg.m/s",
                "target": 60.0, "tol": 0.5,
                "completed_display": "p₁ = 60 Kg.m/s",
                "hint": "p₁ = 2 × 30 = 60 Kg.m/s"
            }
        ],
        "conclusion": "الزخم الخطي للجسم الأول p₁ = 60 Kg.m/s"
    },
    {
        "id": "q4", "type": "interactive",
        "title": "السؤال الرابع: اصطدام كرة بالسقف وارتدادها",
        "text": "قُذفت كرة كتلتها (0.5 kg) رأسياً للأعلى بسرعة (12 m/s)، فاصطدمت بالسقف وارتدت بسرعة (6 m/s) بعد أن لامسته لمدة (0.1 s). إذا كان ارتفاع السقف (4 m) و g = 10 m/s²، احسب: 1) الدفع على الكرة أثناء اصطدامها بالسقف، 2) متوسط قوة دفع السقف للكرة.",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد سرعة وصول الكرة للسقف قبل التصادم (v₁)",
                "micro": [
                    ('نطبّق قانون السقوط حتى ارتفاع السقف:', 'v₁² = v₀² - 2·g·h'),
                    ('السرعة الابتدائية v₀ (m/s):', 'v₀ = ?', '12'),
                    ('الارتفاع h حتى السقف (m):', 'h = ?', '4'),
                ],
                "micro2": [
                    ('احسب ما تحت الجذر ثم اكتب ناتج مربّع السرعة:', 'v₁² = ?', '64'),
                ],
                "law": "المعادلة: v₁² = v₀² - 2·g·h",
                "simple_explain": "نفس فكرة السؤال الأول: نعوض السرعة الابتدائية والجاذبية وارتفاع السقف، ثم نأخذ الجذر التربيعي.",
                "prefix": "v1² = (",
                "blanks": [
                    {"label": "v0", "target": 12.0, "suffix": ")²-2×("},
                    {"label": "g", "target": 10.0, "suffix": ")×("},
                    {"label": "h", "target": 4.0, "suffix": ")"}
                ],
                "has_root": True, "root_prefix": "v1 = √(", "root_target": 64.0, "root_suffix": ")",
                "result_target": 8.0, "result_tol": 0.1,
                "result_label": "احسب الناتج النهائي للسرعة v₁ (m/s):",
                "hint": "v₁² = (12)² - 2(10)(4) = 144 - 80 = 64  ⇒  v₁ = √64 = 8 m/s"
            },
            {
                "num": 2, "title": "الخطوة 2: حساب مقدار الدفع المؤثر على الكرة (I)",
                "micro": [
                    ('نطبّق نظرية الدفع والزخم (بالقيمة المطلقة):', 'I = m · (v₂ - v₁)'),
                    ('كتلة الكرة m (kg):', 'm = ?', '0.5|0,5|.5'),
                    ('سرعة الارتداد v₂ سالبة لأنها معاكسة (m/s):', 'v₂ = ?', '-6'),
                    ('سرعة الوصول v₁ من الخطوة 1 (m/s):', 'v₁ = ?', '8'),
                ],
                "law": "المعادلة: I = | m · (v₂ - v₁) |",
                "simple_explain": "الدفع هو التغير في الزخم. انتبه أن سرعة الارتداد (v₂) تكون بإشارة سالبة لأن اتجاهها معاكس لاتجاه v₁.",
                "prefix": "I = |(",
                "blanks": [
                    {"label": "m", "target": 0.5, "suffix": ")×[("},
                    {"label": "v2", "target": -6.0, "suffix": ")-("},
                    {"label": "v1", "target": 8.0, "suffix": ")]|"}
                ],
                "has_root": False,
                "result_target": 7.0, "result_tol": 0.1,
                "result_label": "احسب مقدار الدفع النهائي I (N.s):",
                "hint": "I = 0.5 × |-6 - 8| = 0.5 × 14 = 7 N.s"
            },
            {
                "num": 3, "title": "الخطوة 3: حساب متوسط قوة دفع السقف على الكرة (F)",
                "micro": [
                    ('قوة السقف = قوة الدفع ناقص ثقل الكرة:', 'F = (I / Δt) - m · g'),
                    ('الدفع I الناتج عن الخطوة 2 (N.s):', 'I = ?', '7'),
                    ('زمن التلامس Δt (s):', 'Δt = ?', '0.1|0,1|.1'),
                ],
                "law": "المعادلة: F = (I / Δt) − (m · g)",
                "simple_explain": "أثناء التصادم يؤثر السقف بقوة تعاكس الحركة، وتُخصم قوة وزن الكرة (m·g) من القوة الناتجة عن الدفع خلال زمن التلامس.",
                "prefix": "F = (",
                "blanks": [
                    {"label": "I", "target": 7.0, "suffix": ")/("},
                    {"label": "dt", "target": 0.1, "suffix": ")-("},
                    {"label": "m", "target": 0.5, "suffix": ")×("},
                    {"label": "g", "target": 10.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 65.0, "result_tol": 0.5,
                "result_label": "احسب متوسط قوة دفع السقف F (N):",
                "hint": "F = 7/0.1 - 0.5×10 = 70 - 5 = 65 N"
            }
        ]
    },
    {
        "id": "q5", "type": "interactive",
        "title": "السؤال الخامس: زمن التحليق باستخدام نظرية الدفع والزخم",
        "text": "قُذف جسم رأسياً للأعلى من سطح الأرض بسرعة (10 m/s). احسب زمن التحليق للجسم باستخدام نظرية الدفع والزخم (g = 10 m/s²).",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد زمن التحليق t",
                "micro": [
                    ('من نظرية الدفع والزخم نحصل على زمن التحليق:', 't = 2·v₀ / g'),
                    ('السرعة الابتدائية v₀ (m/s):', 'v₀ = ?', '10'),
                    ('تسارع الجاذبية g (m/s²):', 'g = ?', '10'),
                ],
                "law": "المعادلة المستعملة: t = 2·v₀ / g",
                "simple_explain": "الدفع الناتج عن وزن الجسم طوال زمن التحليق يساوي التغير الكلي في الزخم من +v₀ إلى -v₀، ومن هنا نستنتج أن t = 2v₀/g.",
                "prefix": "t = 2×(",
                "blanks": [
                    {"label": "v0", "target": 10.0, "suffix": ")/("},
                    {"label": "g", "target": 10.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 2.0, "result_tol": 0.05,
                "result_label": "احسب الناتج النهائي لزمن التحليق t (s):",
                "hint": "t = 2 × 10 / 10 = 2 s"
            }
        ]
    },
    {
        "id": "q6", "type": "interactive",
        "title": "السؤال السادس: قراءة العلاقة البيانية بين الزخم والزمن",
        "text": "الشكل المرفق يمثل العلاقة بين الزخم الخطي p والزمن t لكرة كتلتها (2 kg). من الرسم: عند t = 0 s تكون p = 10 kg.m/s، وعند t = 5 s تكون p = 40 kg.m/s (علاقة خطية). أوجد: 1) السرعة الابتدائية، 2) الدفع خلال 5 ثوانٍ، 3) متوسط القوة خلال 5 ثوانٍ.",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد السرعة الابتدائية v₀",
                "micro": [
                    ('نقرأ الزخم الابتدائي من البيان ثم نطبّق:', 'v₀ = p₀ / m'),
                    ('الزخم الابتدائي p₀ عند اللحظة t = 0 (Kg.m/s):', 'p₀ = ?', '10'),
                    ('كتلة الجسم m (kg):', 'm = ?', '2'),
                ],
                "law": "المعادلة: v₀ = p₀ / m",
                "simple_explain": "نقرأ من الرسم قيمة الزخم عند t=0 (وهي 10 kg.m/s) ونقسمها على الكتلة.",
                "prefix": "v0 = (",
                "blanks": [
                    {"label": "p0", "target": 10.0, "suffix": ")/("},
                    {"label": "m", "target": 2.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 5.0, "result_tol": 0.1,
                "result_label": "احسب السرعة الابتدائية v₀ (m/s):",
                "hint": "v₀ = 10 / 2 = 5 m/s"
            },
            {
                "num": 2, "title": "الخطوة 2: إيجاد الدفع I خلال 5 ثوانٍ",
                "micro": [
                    ('الدفع يساوي تغيّر الزخم بين اللحظتين:', 'I = p₂ - p₁'),
                    ('الزخم عند t = 5 s (Kg.m/s):', 'p₂ = ?', '40'),
                    ('الزخم عند t = 0 (Kg.m/s):', 'p₁ = ?', '10'),
                ],
                "law": "المعادلة المستعملة: I = p₂ - p₁",
                "simple_explain": "الدفع يساوي التغير في الزخم بين لحظتين على الرسم البياني.",
                "prefix": "I = (",
                "blanks": [
                    {"label": "pf", "target": 40.0, "suffix": ")-("},
                    {"label": "pi", "target": 10.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 30.0, "result_tol": 0.5,
                "result_label": "احسب الدفع I (N.s):",
                "hint": "I = 40 - 10 = 30 N.s"
            },
            {
                "num": 3, "title": "الخطوة 3: إيجاد متوسط القوة F خلال 5 ثوانٍ",
                "micro": [
                    ('متوسط القوة يساوي الدفع على المدة:', 'F = I / Δt'),
                    ('الدفع I الناتج عن الخطوة 2 (N.s):', 'I = ?', '30'),
                    ('المدة Δt (s):', 'Δt = ?', '5'),
                ],
                "law": "المعادلة: F = I / Δt",
                "simple_explain": "نقسم الدفع الذي حسبناه على الزمن الذي استغرقه.",
                "prefix": "F = (",
                "blanks": [
                    {"label": "I", "target": 30.0, "suffix": ")/("},
                    {"label": "t", "target": 5.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 6.0, "result_tol": 0.2,
                "result_label": "احسب متوسط القوة F (N):",
                "hint": "F = 30 / 5 = 6 N"
            }
        ]
    },
    {
        "id": "q7", "type": "interactive",
        "title": "السؤال السابع: قوة متغيرة على جسم متحرك",
        "text": "أثّرت قوة متغيرة على جسم كتلته (4 kg) ومتحرك بسرعة (2 m/s) بحيث أصبحت سرعة الجسم (8 m/s) بعد 6 ثوانٍ. أوجد: 1) الدفع المؤثر خلال 6 ثوانٍ، 2) القوة العظمى F من الرسم المثلثي (F-t)، 3) متوسط قوة الدفع خلال 6 ثوانٍ.",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد الدفع I خلال 6 ثوانٍ",
                "micro": [
                    ('نطبّق نظرية الدفع والزخم:', 'I = m · (v₂ - v₁)'),
                    ('كتلة الجسم m (kg):', 'm = ?', '4'),
                    ('السرعة النهائية v₂ (m/s):', 'v₂ = ?', '8'),
                    ('السرعة الابتدائية v₁ (m/s):', 'v₁ = ?', '2'),
                ],
                "law": "المعادلة: I = m · (v₂ - v₁)",
                "simple_explain": "الدفع يساوي التغير في الزخم = الكتلة × التغير في السرعة.",
                "prefix": "I = (",
                "blanks": [
                    {"label": "m", "target": 4.0, "suffix": ")×[("},
                    {"label": "v2", "target": 8.0, "suffix": ")-("},
                    {"label": "v1", "target": 2.0, "suffix": ")]"}
                ],
                "has_root": False,
                "result_target": 24.0, "result_tol": 0.5,
                "result_label": "احسب الدفع I (N.s):",
                "hint": "I = 4 × (8 - 2) = 4 × 6 = 24 N.s"
            },
            {
                "num": 2, "title": "الخطوة 2: إيجاد القوة العظمى F (قمة المثلث البياني)",
                "micro": [
                    ('مساحة المثلث البياني تساوي الدفع، إذن:', 'F = 2·I / t'),
                    ('الدفع I الناتج عن الخطوة 1 (N.s):', 'I = ?', '24'),
                    ('المدة الكلية t (s):', 't = ?', '6'),
                ],
                "law": "المعادلة المستعملة: F = 2·I / t",
                "simple_explain": "الدفع يمثل مساحة الرسم البياني F-t، وشكله مثلث قاعدته t وارتفاعه F، لذا F = 2I/t.",
                "prefix": "F = 2×(",
                "blanks": [
                    {"label": "I", "target": 24.0, "suffix": ")/("},
                    {"label": "t", "target": 6.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 8.0, "result_tol": 0.3,
                "result_label": "احسب القوة العظمى F (N):",
                "hint": "F = 2 × 24 / 6 = 8 N"
            },
            {
                "num": 3, "title": "الخطوة 3: إيجاد متوسط قوة الدفع خلال 6 ثوانٍ",
                "micro": [
                    ('متوسط القوة على كامل المدة:', 'F = I / t'),
                    ('الدفع I (N.s):', 'I = ?', '24'),
                    ('المدة t (s):', 't = ?', '6'),
                ],
                "law": "متوسط القوة: F = I / t",
                "simple_explain": "متوسط القوة يساوي الدفع الكلي مقسوماً على الزمن الكلي.",
                "prefix": "Favg = (",
                "blanks": [
                    {"label": "I", "target": 24.0, "suffix": ")/("},
                    {"label": "t", "target": 6.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 4.0, "result_tol": 0.2,
                "result_label": "احسب متوسط القوة (N):",
                "hint": "F_متوسط = 24 / 6 = 4 N"
            }
        ]
    },
    {
        "id": "q8", "type": "proof",
        "title": "السؤال الثامن: (إثبات) الطاقة الحركية بعد الانفجار",
        "text": "انفجر جسم ساكن إلى جزأين، كتلة الجزء الأول تساوي ثلاثة أمثال كتلة الجزء الثاني. أثبت أن الطاقة الحركية للجزء الثاني K₂ تساوي ثلاثة أمثال الطاقة الحركية للجزء الأول K₁ (أي K₂ = 3K₁).",
        "steps": [
            {
                "num": 1, "type": "symbol",
                "title": "الخطوة 1: التعويض الرمزي عن m₁ بدلالة m₂",
                "law": "قانون الطاقة الحركية: K = p² / (2m)",
                "latex_preview": r"K_1 = \frac{p^2}{2 \times \mathbf{?}}",
                "micro": [
                    ("الجسم ساكن قبل الانفجار إذن الزخم الكلي معدوم. أكمل:", "m₁ v₁ + m₂ v₂ = ?", "0"),
                    ("ومنه الزخمان متساويان في المقدار ومتعاكسان في الاتجاه:", "|p₁| = |p₂| = p"),
                    ("نطبّق قانون الطاقة على الجزء الأول وحده. أكمل المقام:", "K₁ = p² / (2 ?)", "m1"),
                    ("وبما أن لدينا المعطى:", "m₁ = 3m₂"),
                ],
                "label": "أدخل الرمز الصحيح بدلاً من m₁ (استخدم معطى المسألة):",
                "prefix": "K₁ = p² / [2 × (", "suffix": ")]",
                "target": "3m2",
                "completed_display": "K₁ = p² / (2 × 3m₂) = p² / 6m₂",
                "hint": "بما أن m₁ = 3m₂، عوّض عنها بالرمز 3m2 (اكتب: 3m2)"
            },
            {
                "num": 2, "type": "number",
                "title": "الخطوة 2: حساب نسبة الطاقتين (K₂ / K₁) عددياً",
                "law": "قانون الطاقة الحركية: K = p² / (2m)",
                "latex_preview": r"\frac{K_2}{K_1} = \mathbf{?}",
                "micro": [
                    ("نطبّق القانون على الجزء الثاني وحده. أكمل المقام:", "K₂ = p² / (2 ?)", "m2"),
                    ("ومن الخطوة 1 لدينا:", "K₁ = p² / (6m₂)"),
                    ("نقسم K₂ على K₁ فيُختصر p² و m₂. أكمل المقام:", "K₂ / K₁ = 6 / ?", "2"),
                ],
                "label": "أدخل قيمة النسبة K₂ / K₁:",
                "prefix": "K₂ / K₁ = ", "suffix": "",
                "target": 3.0, "tol": 0.1,
                "completed_display": "K₂ / K₁ = 3  ⇒  K₂ = 3K₁",
                "hint": "K₂/K₁ = (p²/2m₂) ÷ (p²/6m₂) = 6/2 = 3"
            }
        ],
        "conclusion": "K₂ = 3K₁  —  الجزء الأخف كتلة يكتسب طاقة حركية أكبر رغم تساوي مقدار الزخم."
    },
    {
        "id": "q9", "type": "interactive",
        "title": "السؤال التاسع: انفجار جسم متحرك إلى جزأين",
        "text": "جسم كتلته (m) يتحرك بسرعة (10 m/s) نحو محور السينات الموجب. حدث داخله انفجار قسّمه إلى جزأين بنسبة كتلية 1:3، بحيث تحرك الجزء الأصغر (¼ الكتلة) بسرعة (100 m/s) نحو محور السينات السالب. جد مقدار سرعة الجزء الأكبر (¾ الكتلة) واتجاهها.",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد سرعة الجزء الأكبر من حفظ الزخم",
                "micro": [
                    ('نطبّق حفظ الزخم على الانفجار:', 'm·v₀ = m₁·v₁ + m₂·v₂'),
                    ('سرعة الجسم قبل الانفجار v₀ (m/s):', 'v₀ = ?', '10'),
                    ('نسبة كتلة الجزء الصغير (الربع). أكمل:', 'k = ?', '0.25|0,25|1/4|.25'),
                    ('سرعة الجزء الصغير بإشارتها (m/s):', 'v₁ = ?', '-100'),
                ],
                "law": "المعادلة المستعملة: v₂ = (v₀ - 0.25·v₁) / 0.75",
                "simple_explain": "بما أن الكتلة الكلية m تُختصر من طرفي معادلة حفظ الزخم، نتعامل مع كل جزء كنسبة من الكتلة الكلية (¼ و¾) بدلاً من قيمة عددية للكتلة.",
                "prefix": "v2 = [(",
                "blanks": [
                    {"label": "v0", "target": 10.0, "suffix": ")-("},
                    {"label": "0.25", "target": 0.25, "suffix": ")×("},
                    {"label": "vsmall", "target": -100.0, "suffix": ")] / ("},
                    {"label": "0.75", "target": 0.75, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 46.67, "result_tol": 0.5,
                "result_label": "احسب مقدار سرعة الجزء الأكبر (m/s):",
                "hint": "v₂ = [10 - (0.25×-100)] / 0.75 = [10+25]/0.75 ≈ 46.67 m/s باتجاه محور السينات الموجب (نفس اتجاه الحركة الأصلية)"
            }
        ]
    },
    {
        "id": "q10", "type": "interactive",
        "title": "السؤال العاشر: قفزة رجل في بركة سباحة",
        "text": "يقفز رجل كتلته (100 kg) من ارتفاع (5 m) عن مستوى سطح الماء في بركة سباحة، فإذا توقف الرجل بفعل تأثير قوة دفع الماء عليه خلال (0.4 s)، جد متوسط قوة دفع الماء على الرجل (g = 10 m/s²).",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد سرعة وصول الرجل لسطح الماء (v)",
                "micro": [
                    ('السقوط من ارتفاع h بدون سرعة ابتدائية:', 'v² = 2·g·h'),
                    ('الارتفاع h (m):', 'h = ?', '5'),
                ],
                "micro2": [
                    ('احسب ما تحت الجذر ثم اكتب ناتج مربّع السرعة:', 'v² = ?', '100'),
                ],
                "law": "المعادلة: v² = 2·g·h",
                "simple_explain": "سقوط حر من ارتفاع h بدون سرعة ابتدائية.",
                "prefix": "v² = 2×(",
                "blanks": [
                    {"label": "g", "target": 10.0, "suffix": ")×("},
                    {"label": "h", "target": 5.0, "suffix": ")"}
                ],
                "has_root": True, "root_prefix": "v = √(", "root_target": 100.0, "root_suffix": ")",
                "result_target": 10.0, "result_tol": 0.2,
                "result_label": "احسب سرعة وصول الرجل للماء v (m/s):",
                "hint": "v² = 2×10×5 = 100  ⇒  v = √100 = 10 m/s"
            },
            {
                "num": 2, "title": "الخطوة 2: إيجاد متوسط قوة دفع الماء F",
                "micro": [
                    ('قوة الماء = تغيّر الزخم زائد الثقل:', 'F = (m · v / Δt) + m · g'),
                    ('كتلة الرجل m (kg):', 'm = ?', '100'),
                    ('زمن التوقف داخل الماء Δt (s):', 'Δt = ?', '0.4|0,4|.4'),
                ],
                "law": "المعادلة: F = (m·v / Δt) + m·g",
                "simple_explain": "قوة الماء يجب أن توقف حركة الرجل خلال زمن قصير، وتتغلب أيضاً على وزنه الذي ما زال يؤثر عليه أثناء الغطس.",
                "prefix": "F = [(",
                "blanks": [
                    {"label": "m", "target": 100.0, "suffix": ")×("},
                    {"label": "v", "target": 10.0, "suffix": ")]/("},
                    {"label": "dt", "target": 0.4, "suffix": ")+("},
                    {"label": "m2", "target": 100.0, "suffix": ")×("},
                    {"label": "g", "target": 10.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 3500.0, "result_tol": 20,
                "result_label": "احسب متوسط قوة دفع الماء F (N):",
                "hint": "F = (100×10)/0.4 + 100×10 = 2500 + 1000 = 3500 N"
            }
        ]
    },
    {
        "id": "q11", "type": "interactive",
        "title": "السؤال الحادي عشر: إيجاد السرعة من الزخم والطاقة الحركية",
        "text": "جسم زخمه الخطي (20 Kg.m/s) وطاقته الحركية (100 J). جد سرعته؟",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد السرعة v",
                "micro": [
                    ('بما أن K = p · v / 2 نستنتج:', 'v = 2·K / p'),
                    ('الطاقة الحركية K (J):', 'K = ?', '100'),
                    ('الزخم p (Kg.m/s):', 'p = ?', '20'),
                ],
                "law": "المعادلة المستعملة: v = 2·K / p",
                "simple_explain": "بما أن الطاقة الحركية K = ½·p·v، يمكننا استنتاج السرعة مباشرة من العلاقة v = 2K/p دون الحاجة لمعرفة الكتلة.",
                "prefix": "v = 2×(",
                "blanks": [
                    {"label": "K", "target": 100.0, "suffix": ")/("},
                    {"label": "p", "target": 20.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 10.0, "result_tol": 0.1,
                "result_label": "احسب الناتج النهائي للسرعة v (m/s):",
                "hint": "v = 2 × 100 / 20 = 10 m/s"
            }
        ]
    },
    {
        "id": "q12", "type": "interactive",
        "title": "السؤال الثاني عشر: تصادم متزلج مع زلاجة (تصادم متلاصق)",
        "text": "ينزلق متزلج كتلته (40 kg) على الجليد بسرعة (2 m/s) فيصطدم بزلاجة ثابتة كتلتها (10 kg)، ويواصل المتزلج انزلاقه مع الزلاجة في نفس اتجاه حركته الأصلية. جد مقدار السرعة المشتركة لهما.",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد السرعة المشتركة v' من حفظ الزخم",
                "micro": [
                    ('التصادم متلاصق، وحفظ الزخم يعطي:', "v' = (m₁ · v₁) / (m₁ + m₂)"),
                    ('كتلة المتزلج m₁ (kg):', 'm₁ = ?', '40'),
                    ('سرعة المتزلج v₁ (m/s):', 'v₁ = ?', '2'),
                    ('كتلة الزلاجة m₂ (kg):', 'm₂ = ?', '10'),
                ],
                "law": "المعادلة: v' = (m₁·v₁) / (m₁ + m₂)",
                "simple_explain": "في التصادم المتلاصق (اللدن) يتحرك الجسمان بعد التصادم بسرعة واحدة مشتركة، ونطبق حفظ الزخم الكلي.",
                "prefix": "v' = (",
                "blanks": [
                    {"label": "m1", "target": 40.0, "suffix": ")×("},
                    {"label": "v1", "target": 2.0, "suffix": ")/[("},
                    {"label": "m1b", "target": 40.0, "suffix": ")+("},
                    {"label": "m2", "target": 10.0, "suffix": ")]"}
                ],
                "has_root": False,
                "result_target": 1.6, "result_tol": 0.05,
                "result_label": "احسب السرعة المشتركة v' (m/s):",
                "hint": "v' = (40×2)/(40+10) = 80/50 = 1.6 m/s"
            }
        ]
    },
    {
        "id": "q13", "type": "interactive",
        "title": "السؤال الثالث عشر: ارتداد كرة عن حائط",
        "text": "كرة كتلتها (0.5 kg) قُذفت أفقياً نحو حائط رأسي فوصلته بسرعة (20 m/s)، وارتدّت عنه على نفس الخط بعد أن فقدت ربع زخمها الخطي، وبعد أن لامست الحائط لمدة (0.01 s). جد: 1) متوسط قوة دفع الحائط للكرة، 2) الدفع من الكرة على الحائط (ملاحظة: بقانون نيوتن الثالث، الدفع من الكرة على الحائط يساوي بالمقدار الدفع من الحائط على الكرة الذي ستحسبه في الخطوة الأولى).",
        "steps": [
            {
                "num": 1, "title": "الخطوة 1: إيجاد الدفع الواقع على الكرة (I)",
                "micro": [
                    ('فقدت الكرة ربع زخمها وارتدت بعكس الاتجاه:', 'I = 1.75 · m · v'),
                    ('كتلة الكرة m (kg):', 'm = ?', '0.5|0,5|.5'),
                    ('سرعة الكرة قبل الارتداد v (m/s):', 'v = ?', '20'),
                ],
                "law": "المعادلة المستعملة: I = 1.75 · m · v",
                "simple_explain": "p_ابتدائي = m·v، وبما أنها ارتدت بعد فقدان ربع الزخم فإن p_نهائي = -¾p_ابتدائي، والدفع I = |p_نهائي - p_ابتدائي| = 1.75×p_ابتدائي.",
                "prefix": "I = 1.75×(",
                "blanks": [
                    {"label": "m", "target": 0.5, "suffix": ")×("},
                    {"label": "v", "target": 20.0, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 17.5, "result_tol": 0.3,
                "result_label": "احسب الدفع I (N.s):",
                "hint": "p₀=0.5×20=10، p_نهائي=-¾×10=-7.5، I=|-7.5-10|=17.5 N.s"
            },
            {
                "num": 2, "title": "الخطوة 2: إيجاد متوسط قوة دفع الحائط للكرة (F)",
                "micro": [
                    ('متوسط القوة = الدفع على زمن التلامس:', 'F = I / Δt'),
                    ('الدفع I الناتج عن الخطوة 1 (N.s):', 'I = ?', '17.5|17,5'),
                    ('زمن التلامس Δt (s):', 'Δt = ?', '0.01|0,01|.01'),
                ],
                "law": "المعادلة: F = I / Δt",
                "simple_explain": "نقسم الدفع الذي حسبناه على زمن التلامس مع الحائط.",
                "prefix": "F = (",
                "blanks": [
                    {"label": "I", "target": 17.5, "suffix": ")/("},
                    {"label": "dt", "target": 0.01, "suffix": ")"}
                ],
                "has_root": False,
                "result_target": 1750.0, "result_tol": 20,
                "result_label": "احسب متوسط القوة F (N):",
                "hint": "F = 17.5 / 0.01 = 1750 N"
            }
        ]
    },
    {
        "id": "q14", "type": "proof",
        "title": "السؤال الرابع عشر: (إثبات) توزيع الطاقة الحركية بعد الانفجار",
        "text": "انفجر جسم ساكن إلى جزأين كتلة كل منهما (m₁ , m₂)، فكانت الطاقة الناتجة عن الانفجار K. أثبت أن الطاقة الحركية التي يكتسبها الجسم الثاني K₂ تُعطى بالعلاقة: K₂ = [m₁ / (m₁+m₂)] × K",
        "steps": [
            {
                "num": 1, "type": "symbol",
                "title": "الخطوة 1: نتيجة حفظ الزخم مباشرة بعد الانفجار",
                "law": "قانون حفظ الزخم الخطي عند السكون الابتدائي",
                "latex_preview": r"|p_1| = |\mathbf{?}| = p",
                "micro": [
                    ("الجسم ساكن قبل الانفجار إذن الزخم الكلي معدوم. أكمل:", "m₁ v₁ + m₂ v₂ = ?", "0"),
                    ("ومنه مقدار زخم الجزء الأول يساوي مقدار زخم الجزء الثاني والاتجاهان متعاكسان.", ""),
                ],
                "label": "من حفظ الزخم m₁v₁+m₂v₂=0، أدخل الرمز الذي يساوي |p₁| بالمقدار:",
                "prefix": "|p₁| = |", "suffix": "| = p",
                "target": "p2",
                "completed_display": "|p₁| = |p₂| = p",
                "hint": "الجزءان يتحركان بزخمين متساويين بالمقدار ومتعاكسين بالاتجاه، اكتب: p2"
            },
            {
                "num": 2, "type": "symbol",
                "title": "الخطوة 2: كتابة الطاقة الكلية K كمجموع K₁ و K₂",
                "law": "الطاقة الحركية لكل جزء: K = p² / (2m)",
                "latex_preview": r"K = \frac{p^2}{2m_1} + \frac{p^2}{2 \times \mathbf{?}}",
                "micro": [
                    ("طاقة الجزء الأول وحده. أكمل المقام:", "K₁ = p² / (2 ?)", "m1"),
                    ("والطاقة الكلية هي مجموع طاقتي الجزأين:", "K = K₁ + K₂"),
                ],
                "label": "أكمل مقام الحد الثاني (طاقة الجسم الثاني K₂):",
                "prefix": "K = p²/2m₁ + p² / (2 × (", "suffix": "))",
                "target": "m2",
                "completed_display": "K = p²/2m₁ + p²/2m₂",
                "hint": "الحد الثاني هو K₂ = p²/2m₂، اكتب: m2"
            },
            {
                "num": 3, "type": "symbol",
                "title": "الخطوة 3: الوصول للصيغة النهائية لـ K₂ بدلالة K",
                "law": "بحل معادلتي K و K₂ معاً لحذف p²، نصل إلى العلاقة النهائية المطلوب إثباتها",
                "latex_preview": r"K_2 = \frac{m_1}{\mathbf{?}} \times K",
                "micro": [
                    ("نُخرج العامل المشترك من الطاقة الكلية. أكمل المقام:", "K = (p² / 2) · (1/m₁ + 1/?)", "m2"),
                    ("نجمع الكسرين داخل القوس. أكمل المقام:", "K = (p² / 2) · (m₁ + m₂) / (?)", "m1m2|m2m1"),
                    ("نستخرج p²/2 منها ونعوّضها في طاقة الجزء الثاني:", "K₂ = K · m₁ m₂ / (m₂ · (m₁ + m₂))"),
                ],
                "label": "أكمل مقام الكسر النهائي (بدلالة m₁ و m₂):",
                "prefix": "K₂ = [m₁ / (", "suffix": ")] × K",
                "target": "m1+m2",
                "completed_display": "K₂ = [m₁ / (m₁+m₂)] × K ✅",
                "hint": "المقام هو مجموع الكتلتين، اكتب: m1+m2"
            }
        ],
        "conclusion": "K₂ = [m₁ / (m₁+m₂)] × K"
    },
    {
        "id": "q15", "type": "proof",
        "title": "السؤال الخامس عشر: (إثبات) نسبة طاقتي القذيفة والمدفع",
        "text": "قذيفة كتلتها (m) انطلقت أفقياً بسرعة (v) من فوهة مدفع ساكن كتلته (M). أثبت أن النسبة بين طاقة حركة المدفع Kc إلى طاقة حركة القذيفة Kp مباشرة بعد الإطلاق تُعطى بالعلاقة: Kc / Kp = m / M",
        "steps": [
            {
                "num": 1, "type": "symbol", "case_sensitive": True,
                "title": "الخطوة 1: تطبيق حفظ الزخم على النظام (مدفع+قذيفة)",
                "law": "قانون حفظ الزخم الخطي: m₁v₁ + m₂v₂ = 0  ،  تنبيه: سرعة ارتداد المدفع نرمز لها V",
                "latex_preview": r"M \cdot V = m \times \mathbf{?}",
                "micro": [
                    ("النظام (مدفع + قذيفة) ساكن قبل الإطلاق إذن مجموع الزخمين معدوم ومقداراهما متساويان.", ""),
                    ("زخم المدفع = كتلته × سرعة ارتداده. أكمل:", "p = M · ?", "V"),
                ],
                "label": "أدخل الرمز الصحيح لسرعة القذيفة كما وردت في نص السؤال (احترس من حالة الأحرف):",
                "prefix": "M × V = m × (", "suffix": ")",
                "target": "v", "case_sensitive": True,
                "completed_display": "M × V = m × v",
                "hint": "سرعة القذيفة معطاة في نص السؤال بالرمز v (حرف صغير)"
            },
            {
                "num": 2, "type": "symbol", "case_sensitive": True,
                "title": "الخطوة 2: كتابة نسبة الطاقتين Kc/Kp بدلالة الزخم المشترك p",
                "law": "مقدارا الزخمين متساويان: p = M · V = m · v  ،  قانون الطاقة: K = p² / (2m)",
                "latex_preview": r"\frac{K_c}{K_p} = \frac{p^2/2M}{p^2/2 \times \mathbf{?}}",
                "micro": [
                    ("طاقة المدفع وحده بدلالة الزخم p. أكمل المقام (كتلة المدفع):", "Kc = p² / (2 ?)", "M"),
                    ("ونكتب الأن النسبة بين طاقة المدفع وطاقة القذيفة بالزخم p نفسه.", ""),
                ],
                "label": "أكمل مقام طاقة القذيفة (كتلة القذيفة، احترس من حالة الأحرف):",
                "prefix": "Kc / Kp = (p²/2M) / (p² / 2(", "suffix": "))",
                "target": "m", "case_sensitive": True,
                "completed_display": "Kc / Kp = (p²/2M) / (p²/2m)",
                "hint": "كتلة القذيفة تُكتب بحرف صغير m، اكتب: m"
            },
            {
                "num": 3, "type": "symbol", "case_sensitive": True,
                "title": "الخطوة 3: الصيغة النهائية للنسبة بعد التبسيط",
                "law": "بعد اختصار p²/2 من البسط والمقام",
                "latex_preview": r"\frac{K_c}{K_p} = \mathbf{?}",
                "micro": [
                    ("من الخطوة 2 لدينا:", "Kc / Kp = [p² / (2M)] / [p² / (2m)]"),
                    ("نختصر p² و 2 من البسط والمقام. أكمل المقام:", "Kc / Kp = (1/M) / (1/?)", "m"),
                ],
                "label": "أدخل الناتج النهائي للنسبة (بالرمزين الصحيحين وحالة الأحرف الصحيحة):",
                "prefix": "Kc / Kp = ", "suffix": "",
                "target": "m/M", "case_sensitive": True,
                "completed_display": "Kc / Kp = m/M ✅",
                "hint": "بعد الاختصار: m/M — احرص أن تكتب m بحرف صغير و M بحرف كبير"
            }
        ],
        "conclusion": "Kc / Kp = m / M  —  المدفع (الأثقل) يكتسب طاقة حركية أقل رغم تساوي مقدار الزخم مع القذيفة."
    }
]

TOTAL_QUESTIONS = len(questions_db)

FORMULA_SHEET = [
    ("الزخم الخطي", "p = m · v"),
    ("الدفع (نظرية الدفع والزخم)", "I = Δp = F·Δt = m(v₂-v₁)"),
    ("سقوط/قذف رأسي", "v² = v₀² - 2gh"),
    ("تذكير (صف 11): الحركة الرأسية — السرعة", "v_yf = v_yi - g·t"),
    ("تذكير (صف 11): الحركة الرأسية — الموضع", "y_f = y_i + v_yi·t - ½ g·t²"),
    ("تذكير (صف 11): مستقلة عن الزمن", "v²_yf = v²_yi - 2g(y_f - y_i)"),
    ("حفظ الزخم الخطي", "m₁v₁+m₂v₂ = m₁v₁'+m₂v₂'"),
    ("الطاقة الحركية", "K = ½mv² = p²/2m"),
]

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
        "student_name": "", "total_xp": 0, "streak": 0,
        "badges": set(), "completed_questions": set(),
        "no_hint_flag": {}, "attempts": {}, "hint_level": {},
        "start_time": {}, "time_spent": {},
        "daily_tip": random.choice(STUDY_TIPS),
        "samed_view": "home", "samed_grade": 12, "samed_subject": "phys",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def award_badge(name):
    if name not in st.session_state["badges"]:
        st.session_state["badges"].add(name)
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


FIGURES = {
    "q6": "data:image/png;base64,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",
    "q7": "data:image/png;base64,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",
}

FIGURE_CAPTIONS = {
    "q6": "الشكل: تغيّر الزخم p بدلالة الزمن t",
    "q7": "الشكل: تغيّر القوة F بدلالة الزمن t",
}


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
    st.session_state["completed_questions"].discard(qid)
    st.session_state["start_time"][qid] = time.time()
    st.session_state["time_spent"].pop(qid, None)
    st.session_state[f"step_prog_{qid}"] = 1
    st.session_state["no_hint_flag"][qid] = True
    keys_to_clear = [k for k in st.session_state["attempts"] if k.startswith(f"{qid}_")]
    for k in keys_to_clear:
        st.session_state["attempts"].pop(k, None)
        st.session_state["hint_level"].pop(k, None)

def reset_everything():
    keep_name = st.session_state.get("student_name", "")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()
    st.session_state["student_name"] = keep_name

# ==========================================================
# 4.5 الحساب المحلي + Dashboard السنوي + توجيه المنصة
# ==========================================================
PROFILE_KEY = "samed-profile-v1"
LOCAL_FIRST_VERSION = "local-first-pwa-zip-v1"
DASHBOARD_UX_VERSION = "streamlit-dashboard-v18.1-pwa-download"
ANNUAL_PROGRAM = {
 "phys": {6:["القياس والوحدات","الحركة والسرعة","القوى من حولنا","الشغل والطاقة","الضوء والرؤية","الصوت"],7:["المادة وحالاتها","الحرارة ودرجة الحرارة","الآلات البسيطة","الكهرباء الساكنة","المغناطيسية"],8:["الحركة المنتظمة","القوة والاحتكاك","الضغط والكثافة","الطاقة وتحولاتها","الدارات الكهربائية"],9:["الحركة بتسارع ثابت","قوانين نيوتن","الشغل والقدرة","الموجات","التيار الكهربائي"],10:["المتجهات","الحركة في بعدين","قوانين نيوتن وتطبيقاتها","الشغل والطاقة والقدرة","مقدمة في الزخم"],11:["الحركة الرأسية والمقذوفات","الحركة الدائرية","الجاذبية الكونية","الموائع","الاهتزاز والموجات"],12:["الزخم الخطي والدفع","الكهرباء الساكنة","التيار والدارات","المجال المغناطيسي","الحث الكهرومغناطيسي","مقدمة الفيزياء الحديثة"]},
 "chem": {6:["المادة وخواصها","المخاليط والمحاليل","التغيرات الفيزيائية والكيميائية","الماء ودورته"],7:["بناء الذرة","العناصر والمركبات","مقدمة الجدول الدوري","الأحماض والقواعد حولنا"],8:["التركيب الذري والإلكترونات","الروابط الكيميائية","التفاعلات الكيميائية","المحاليل والذائبية"],9:["المعادلات الكيميائية ووزنها","الأحماض والقواعد والأملاح","الأكسدة والاختزال","مقدمة الكيمياء العضوية"],10:["المول والحسابات الكيميائية","الجدول الدوري والدورية","أنواع الروابط","الغازات وقوانينها"],11:["الاتزان الكيميائي","سرعة التفاعل","الأحماض والقواعد وحساب pH","الكهروكيمياء"],12:["النموذج الذري والتركيب الإلكتروني","الكيمياء الحرارية","الكيمياء العضوية","البوليمرات","التحليل الكيميائي"]}
}
GRADE_LABELS={6:"السادس",7:"السابع",8:"الثامن",9:"التاسع",10:"العاشر",11:"الحادي عشر",12:"الثاني عشر"}
for _k,_v in (("samed_view","home"),("student_profile",None),("dashboard_subject","phys")):
    if _k not in st.session_state: st.session_state[_k]=_v

def _profile_bridge(profile):
    payload=json.dumps(profile,ensure_ascii=False)
    script="""<script>(function(){try{window.parent.localStorage.setItem('samed-profile-v1',JSON.stringify(__PROFILE__));}catch(e){}})();</script>""".replace('__PROFILE__',payload)
    components.html(script,height=0)

def _top_back(label="العودة"):
    if st.button("← "+label,key="local_back_"+st.session_state.get("samed_view","x")):
        st.session_state["samed_view"]="home";st.rerun()

def _render_onboarding():
    st.markdown("""<style id="onboarding-parent-v16">[data-testid='stHeader'],[data-testid='stToolbar'],[data-testid='stDecoration'],footer,section[data-testid='stSidebar'],[data-testid='stSidebarCollapsedControl']{display:none!important}.stApp,[data-testid='stAppViewContainer']{background:#f8fafc!important;direction:rtl!important}section[data-testid='stMain'] .block-container,[data-testid='stMainBlockContainer']{width:100%!important;max-width:1220px!important;margin:0 auto!important;padding:0 12px 24px!important}[data-testid='stCustomComponentV1'],[data-testid='stCustomComponentV1'] iframe{display:block!important;width:100%!important;border:0!important;background:#f8fafc!important}</style>""",unsafe_allow_html=True)
    old=st.session_state.get("student_profile") or {}
    component=components.declare_component("student_samed_onboarding_v16",path=str(Path(__file__).with_name("onboarding_component")))
    event=component(data={"profile":{"name":old.get("name",""),"grade":int(old.get("grade",12)),"subjects":old.get("subjects",["phys","chem"])},"has_password":bool(old.get("passwordHash") or old.get("pinHash")),"error":st.session_state.get("_onboarding_error","")},default=None,key="student_samed_onboarding_v16")
    if isinstance(event,dict):
        token=str(event.get("token","")).strip();action=str(event.get("action","")).strip()
        if token and st.session_state.get("_onboarding_v16_token")!=token:
            st.session_state["_onboarding_v16_token"]=token
            if action=="back_home":
                st.session_state.pop("_onboarding_error",None);st.session_state["samed_view"]="home";st.rerun()
            if action=="save_profile" and isinstance(event.get("profile"),dict):
                raw=event["profile"];name=str(raw.get("name","")).strip()
                try: grade=int(raw.get("grade",12))
                except Exception: grade=12
                grade=grade if grade in GRADE_LABELS else 12
                subjects=[s for s in raw.get("subjects",[]) if s in {"phys","chem"}]
                password=str(raw.get("password","")).strip();confirm=str(raw.get("confirm","")).strip()
                existing_hash=old.get("passwordHash") or old.get("pinHash")
                error=""
                if len(name)<2: error="اكتب اسمًا من حرفين على الأقل."
                elif not subjects: error="اختر مادة واحدة على الأقل."
                elif (not existing_hash or password or confirm) and len(password)<6: error="يجب أن تتكون كلمة المرور من 6 أحرف على الأقل."
                elif (not existing_hash or password or confirm) and password!=confirm: error="كلمة المرور وتأكيدها غير متطابقين."
                if error:
                    st.session_state["_onboarding_error"]=error;st.rerun()
                password_hash=hashlib.sha256(password.encode("utf-8")).hexdigest() if password else existing_hash
                profile={"id":old.get("id") or "local-"+uuid.uuid4().hex[:12],"name":name,"grade":grade,"subjects":subjects,"passwordHash":password_hash,"mode":"local"}
                st.session_state.pop("_onboarding_error",None);st.session_state["student_profile"]=profile;st.session_state["student_name"]=name;st.session_state["samed_view"]="dashboard";st.rerun()
    st.stop()

def _unit_download_bytes(filename):
    p=Path(__file__).with_name("unit_packs")/filename
    return p.read_bytes() if p.exists() else b""

def _render_dashboard():
    profile = st.session_state.get("student_profile")
    if not profile:
        st.session_state["samed_view"] = "onboarding"
        st.rerun()

    _profile_bridge(profile)
    allowed = profile.get("subjects", ["phys", "chem"])
    physics_live = "phys" in allowed and profile["grade"] == 12
    chemistry_live = "chem" in allowed and profile["grade"] == 12
    physics_completed = st.session_state.get("completed_questions", set()) or set()
    physics_book_completed = st.session_state.get("physbook_completed_questions", set()) or set()
    physics_review_completed = st.session_state.get("physreview_completed_questions", set()) or set()
    physics_foundation_completed = st.session_state.get("physfoundation_completed_questions", set()) or set()
    chemistry_completed = st.session_state.get("chem_completed_questions", set()) or set()
    textbook_completed = st.session_state.get("book_completed_questions", set()) or set()
    chemistry_review_completed = st.session_state.get("chemreview_completed_questions", set()) or set()
    chemistry_foundation_completed = st.session_state.get("chemfoundation_completed_questions", set()) or set()
    physics_lesson_done = sum(1 for qid in physics_completed if str(qid).startswith("q"))
    physics_book_done = sum(1 for qid in physics_book_completed if str(qid).startswith("pb"))
    physics_review_done = sum(1 for qid in physics_review_completed if str(qid).startswith("pr"))
    physics_foundation_done = sum(1 for qid in physics_foundation_completed if str(qid).startswith("pf"))
    physics_required_done = physics_review_done + physics_book_done + physics_lesson_done
    chemistry_lesson_done = sum(1 for qid in chemistry_completed if str(qid).startswith("c"))
    chemistry_book_done = sum(1 for qid in textbook_completed if str(qid).startswith("tb"))
    chemistry_review_done = sum(1 for qid in chemistry_review_completed if str(qid).startswith("cr"))
    chemistry_foundation_done = sum(1 for qid in chemistry_foundation_completed if str(qid).startswith("cf"))
    chemistry_required_done = chemistry_review_done + chemistry_book_done + chemistry_lesson_done
    # التأسيس دعم اختياري: يبقى تقدمه ونقاطه محفوظين، لكنه لا يقفل المسار ولا يخفض نسبة الإنجاز المطلوبة.
    physics_total, chemistry_total = 32, 43
    selected_total = (physics_total if physics_live else 0) + (chemistry_total if chemistry_live else 0)
    done = (physics_required_done if physics_live else 0) + (chemistry_required_done if chemistry_live else 0)
    pct = int(done * 100 / selected_total) if selected_total else 0
    physics_pct = int(physics_required_done * 100 / physics_total) if physics_total else 0
    chemistry_pct = int(chemistry_required_done * 100 / chemistry_total) if chemistry_total else 0
    xp = st.session_state.get("total_xp", 0) + st.session_state.get("physbook_total_xp", 0) + st.session_state.get("physfoundation_total_xp", 0) + st.session_state.get("physreview_total_xp", 0) + st.session_state.get("chem_total_xp", 0) + st.session_state.get("book_total_xp", 0) + st.session_state.get("chemfoundation_total_xp", 0) + st.session_state.get("chemreview_total_xp", 0)
    safe_name = (str(profile.get("name", "الطالب"))
                 .replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))
    grade_label = GRADE_LABELS[profile["grade"]]

    from streamlit_dashboard_v13 import render_dashboard_v13
    stage_progress = {
        "phys": [
            round(100 * physics_foundation_done / 8),
            round(100 * physics_review_done / 7),
            round(100 * physics_book_done / 10),
            round(100 * physics_lesson_done / 15),
        ],
        "chem": [
            round(100 * chemistry_foundation_done / 8),
            round(100 * chemistry_review_done / 8),
            round(100 * chemistry_book_done / 20),
            round(100 * chemistry_lesson_done / 15),
        ],
    }
    unit_progress = {"phys": physics_pct, "chem": chemistry_pct}
    display_xp = max(xp, done * 100 + 50 if done else 0)
    action = render_dashboard_v13(
        profile=profile,
        safe_name=safe_name,
        grade_label=grade_label,
        overall_pct=pct,
        done=done,
        selected_total=selected_total,
        xp=display_xp,
        allowed=allowed,
        physics_live=physics_live,
        chemistry_live=chemistry_live,
        stage_progress=stage_progress,
        unit_progress=unit_progress,
        unit_bytes=_unit_download_bytes,
    )
    if action == "edit":
        st.session_state["samed_view"] = "onboarding"
        st.rerun()
    if action == "home":
        st.session_state["samed_view"] = "home"
        st.rerun()
    if action == "contact":
        st.session_state["_contact_return_page"] = "app.py"
        st.session_state["_contact_return_view"] = "dashboard"
        st.switch_page("pages/contact.py")
    if action:
        routes = {
            "phys_0": ("physics_foundation", "pages/physics_foundation.py"),
            "phys_1": ("physics_review", "pages/physics_unit_review.py"),
            "phys_2": ("physics_book", "pages/physics_textbook_exercises.py"),
            "chem_0": ("chemistry_foundation", "pages/chemistry_foundation.py"),
            "chem_1": ("chemistry_review", "pages/chemistry_unit_review.py"),
            "chem_2": ("chem_book", "pages/chemistry_textbook_exercises.py"),
            "chem_3": ("chem_app", "pages/chemistry_unit_1.py"),
        }
        if action == "phys_3":
            st.session_state["samed_view"] = "app"
            st.rerun()
        if action in routes:
            view, page = routes[action]
            st.session_state["samed_view"] = view
            st.switch_page(page)
    st.stop()

# صفحة الهبوط المعتمدة حاليًا.
if st.session_state.get("samed_view","home")=="home":
    st.markdown("""<style>[data-testid='stHeader'],[data-testid='stToolbar'],[data-testid='stDecoration'],footer{display:none!important}.stApp{background:#fff!important}.block-container{max-width:none!important;padding:0!important;margin:0!important}[data-testid='stElementContainer']{margin:0!important}iframe{display:block;width:100%!important;border:0!important}</style>""",unsafe_allow_html=True)
    comp=components.declare_component("student_samed_local_first_v18",path=str(Path(__file__).with_name("landing_component")))
    event=comp(default=None,key="student_samed_local_first_v18")
    if isinstance(event,dict):
        action=event.get("action");token=str(event.get("token",""))
        if action=="profile_loaded" and isinstance(event.get("profile"),dict):
            p=dict(event["profile"]);p["subjects"]=[{"physics":"phys","chemistry":"chem"}.get(s,s) for s in p.get("subjects",[]) if {"physics":"phys","chemistry":"chem"}.get(s,s) in {"phys","chem"}];st.session_state["student_profile"]=p;st.session_state["student_name"]=p.get("name","")
        elif token and st.session_state.get("_last_visual_event")!=token:
            st.session_state["_last_visual_event"]=token
            if action=="open_onboarding": st.session_state["samed_view"]="onboarding"
            elif action=="open_dashboard": st.session_state["samed_view"]="dashboard" if st.session_state.get("student_profile") else "onboarding"
            elif action=="open_momentum": st.session_state["samed_view"]="app" if st.session_state.get("student_profile") else "onboarding"
            elif action=="open_contact":
                st.session_state["_contact_return_page"]="app.py";st.session_state["_contact_return_view"]="home";st.switch_page("pages/contact.py")
            st.rerun()
    st.stop()
if st.session_state.get("samed_view")=="onboarding": _render_onboarding()
if st.session_state.get("samed_view")=="dashboard": _render_dashboard()

render_exercise_header_v18(
    subject="الفيزياء", track="تدريب إضافي", unit_title="الزخم الخطي والدفع",
    current_page="app.py", tip=st.session_state["daily_tip"], subject_icon="⚛️",
)

# ==========================================================
# 5. زر الملف الشخصي (نافذة منبثقة) في أعلى يمين الصفحة
# ==========================================================
with st.container(key="avatar_row"):
    _pc_avatar = st.columns([1, 11])[0]
with _pc_avatar:
    level_label, level_color, next_threshold = get_level(st.session_state["total_xp"])
    xp = st.session_state["total_xp"]
    progress_pct = min(100, int((xp / next_threshold) * 100)) if next_threshold else 100
    name_display = st.session_state["student_name"] or "طالب مجتهد"
    avatar_letter = name_display.strip()[0] if name_display.strip() else "🧑‍🎓"
    done_count = len(st.session_state["completed_questions"])
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

            st.session_state["student_name"] = st.text_input(
                "✏️ اسم الطالب/ـة", value=st.session_state["student_name"],
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
            if st.session_state["badges"]:
                tiles = ""
                for b in sorted(st.session_state["badges"]):
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
# يُعرض الرأس بعد حسم التوجيه، داخل صفحة التمارين فقط.


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

for _k, _v in (("samed_view", "home"), ("samed_grade", 12), ("samed_subject", None)):
    if _k not in st.session_state:
        st.session_state[_k] = _v

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


if st.session_state["samed_view"] == "home":

    _xp   = int(st.session_state.get("total_xp", 0) or 0)
    _done = len(st.session_state.get("completed_questions", set()) or set())
    _bdg  = len(st.session_state.get("badges", set()) or set())
    _strk = int(st.session_state.get("streak", 0) or 0)
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
            st.session_state["samed_view"] = "app"
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
            _on = (st.session_state["samed_grade"] == _gn)
            if st.button(str(_gn) + " · " + _gl, key="samed_g_" + str(_gn),
                         use_container_width=True,
                         type=("primary" if _on else "secondary")):
                st.session_state["samed_grade"] = _gn
                st.rerun()

    # ---------- المواد ----------
    _grade = st.session_state["samed_grade"]
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
            _open = (st.session_state["samed_subject"] == _sk2)
            if st.button(("▼ إخفاء الوحدات" if _open else "عرض الوحدات ←"),
                         key="samed_s_" + _sk2, use_container_width=True,
                         type=("primary" if _open else "secondary")):
                st.session_state["samed_subject"] = (None if _open else _sk2)
                st.rerun()

    # ---------- الوحدات ----------
    _subj = st.session_state["samed_subject"]
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
                    st.session_state["samed_view"] = "app"
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
            st.rerun()


# ==========================================================
# 7. اختيار التمرين + وضع الشرح المبسط
# ==========================================================
def display_title(item):
    icon = "🧮" if item["type"] == "interactive" else "📜"
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

if qid not in st.session_state["start_time"]:
    st.session_state["start_time"][qid] = time.time()
if qid not in st.session_state["no_hint_flag"]:
    st.session_state["no_hint_flag"][qid] = True

elapsed = st.session_state["time_spent"].get(qid)
if elapsed is None:
    elapsed = time.time() - st.session_state["start_time"][qid]

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

            attempts_so_far = st.session_state["attempts"].get(step_key, 0)
            hint_lvl_current = st.session_state["hint_level"].get(step_key, 0)
            potential_points = calc_points(attempts_so_far + 1, hint_lvl_current)
            _revealed = st.session_state.setdefault("revealed", {}).get(step_key, False)
            _mn = 0
            if step.get("micro"):
                st.markdown(micro_html(step, final_mode="none", qid=qid, reveal=_revealed), unsafe_allow_html=True)
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
                    micro_html(step, final_mode="none", field="micro2", start=_mn + 1, qid=qid, reveal=_revealed),
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
                            value=(float(step["root_target"]) if _revealed else None), placeholder="..", label_visibility="collapsed"
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
                        value=(float(step["result_target"]) if _revealed else None), placeholder="..", label_visibility="collapsed"
                    )
                with rc3:
                    st.markdown(f"<div class='formula-text'>{eq_frag(_runit)}</div>", unsafe_allow_html=True)

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
                st.session_state.setdefault("revealed", {})[step_key] = True
                st.session_state["hint_level"][step_key] = 3
                st.session_state["no_hint_flag"][qid] = False
                st.toast("تم إدخال الإجابة الصحيحة في الفراغات — اضغط «تحقق 🎯» للتقدم")
                st.rerun()

            st.markdown(f'<span class="points-chip">🎯 نقاط هذه المحاولة المتوقعة: {potential_points}</span>', unsafe_allow_html=True)

            if hint_btn:
                new_level = min(3, hint_lvl_current + 1)
                st.session_state["hint_level"][step_key] = new_level
                st.session_state["no_hint_flag"][qid] = False
                st.rerun()

            if hint_lvl_current >= 1:
                msg = rich_hint(step, hint_lvl_current)
                st.markdown(f'<div class="hint-box">💡 <b>شرح موجّه (مستوى {hint_lvl_current}):</b>{msg}</div>', unsafe_allow_html=True)
                if hint_lvl_current < 3:
                    st.caption("بحاجة لمساعدة أكبر؟ اضغط 💡 تلميح مرة أخرى.")

            if check_btn:
                st.session_state["attempts"][step_key] = st.session_state["attempts"].get(step_key, 0) + 1
                attempts_now = st.session_state["attempts"][step_key]

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
                    st.session_state["total_xp"] += pts
                    if attempts_now == 1 and hint_lvl_current == 0:
                        st.session_state["streak"] += 1
                    else:
                        st.session_state["streak"] = 0
                    if st.session_state["streak"] == 3:
                        award_badge("🔥 3 إجابات متتالية بلا أخطاء")
                    if st.session_state["streak"] == 5:
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
        if qid not in st.session_state["completed_questions"]:
            st.session_state["completed_questions"].add(qid)
            duration = time.time() - st.session_state["start_time"][qid]
            st.session_state["time_spent"][qid] = duration
            st.session_state["total_xp"] += 15
            if len(st.session_state["completed_questions"]) == 1:
                award_badge("🏅 أول تمرين مكتمل")
            if st.session_state["no_hint_flag"].get(qid, False):
                award_badge("⭐ إتقان بلا تلميحات")
            if len(st.session_state["completed_questions"]) == TOTAL_QUESTIONS:
                award_badge("🎓 إتقان كامل لجميع التمارين")
            st.balloons()

        dur = st.session_state["time_spent"].get(qid, 0)
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

            _revealed = st.session_state.setdefault("revealed", {}).get(step_key, False)
            _plabel = step.get("label", "")
            _fmode = "none" if step.get("micro_only") else "preview"
            if _only_choices:
                pass
            elif step.get("micro"):
                st.markdown(micro_html(step, final_mode=_fmode, final_say=_plabel, qid=qid, reveal=_revealed), unsafe_allow_html=True)
            else:
                st.markdown(
                    micro_html(step, final_mode=_fmode, field="__nomicro__", final_say=_plabel, qid=qid, reveal=_revealed),
                    unsafe_allow_html=True,
                )

            attempts_so_far = st.session_state["attempts"].get(step_key, 0)
            hint_lvl_current = st.session_state["hint_level"].get(step_key, 0)
            potential_points = calc_points(attempts_so_far + 1, hint_lvl_current)

            _micro_only = bool(step.get("micro_only"))
            _sym_key = f"symbuf_{step_key}"
            _pending = st.session_state.get(_sym_key)
            user_val = ""
            if _micro_only:
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
                st.session_state.setdefault("revealed", {})[step_key] = True
                st.session_state["hint_level"][step_key] = 2
                st.session_state["no_hint_flag"][qid] = False
                st.toast("تم إدخال الإجابة الصحيحة في الفراغ — اضغط «تحقق 🎯» للتقدم")
                st.rerun()

            st.markdown(f'<span class="points-chip">🎯 نقاط هذه المحاولة المتوقعة: {potential_points}</span>', unsafe_allow_html=True)

            if hint_btn:
                st.session_state["hint_level"][step_key] = min(2, hint_lvl_current + 1)
                st.session_state["no_hint_flag"][qid] = False
                st.rerun()

            if hint_lvl_current >= 1:
                msg = rich_hint(step, hint_lvl_current + 1)
                st.markdown(f'<div class="hint-box">💡 <b>شرح موجّه:</b>{msg}</div>', unsafe_allow_html=True)
                if hint_lvl_current < 2:
                    st.caption("بحاجة لمساعدة أكبر؟ اضغط 💡 تلميح مرة أخرى.")

            if check_btn:
                st.session_state["attempts"][step_key] = st.session_state["attempts"].get(step_key, 0) + 1
                attempts_now = st.session_state["attempts"][step_key]

                if _micro_only:
                    pts = calc_points(attempts_now, hint_lvl_current)
                    st.session_state["total_xp"] += pts
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
                        st.session_state["total_xp"] += pts
                        if attempts_now == 1 and hint_lvl_current == 0:
                            st.session_state["streak"] += 1
                        else:
                            st.session_state["streak"] = 0
                        if st.session_state["streak"] == 3:
                            award_badge("🔥 3 إجابات متتالية بلا أخطاء")
                        if st.session_state["streak"] == 5:
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
        if qid not in st.session_state["completed_questions"]:
            st.session_state["completed_questions"].add(qid)
            duration = time.time() - st.session_state["start_time"][qid]
            st.session_state["time_spent"][qid] = duration
            st.session_state["total_xp"] += 15
            if len(st.session_state["completed_questions"]) == 1:
                award_badge("🏅 أول تمرين مكتمل")
            award_badge("🧠 عقل تحليلي (أتقن برهاناً)")
            if st.session_state["no_hint_flag"].get(qid, True):
                award_badge("⭐ إتقان بلا تلميحات")
            if len(st.session_state["completed_questions"]) == TOTAL_QUESTIONS:
                award_badge("🎓 إتقان كامل لجميع التمارين")
            st.balloons()

        dur = st.session_state["time_spent"].get(qid, 0)
        st.success(f"🎉 أحسنت! أتممت هذا الإثبات خلال {fmt_time(dur)} (+15 XP مكافأة إتمام).")
        if st.button("🔄 إعادة حل الإثبات من البداية", key=f"restart_{qid}"):
            reset_question(qid, "proof")
            st.rerun()

# ==========================================================
# 9. شهادة الإنجاز عند إتمام جميع التمارين
# ==========================================================
if len(st.session_state["completed_questions"]) == TOTAL_QUESTIONS:
    st.snow()
    name_display = st.session_state["student_name"] or "طالب مجتهد"
    total_time = sum(st.session_state["time_spent"].values())
    level_label, _, _ = get_level(st.session_state["total_xp"])

    st.markdown(f"""
    <div class="cert-box">
        <h2>🏆 شهادة إتمام</h2>
        <p style="font-size:1.2rem;">تُمنح هذه الشهادة إلى الطالب/ـة</p>
        <h3>{name_display}</h3>
        <p>لإتمامه/ـا بنجاح جميع تمارين درس <b>الزخم الخطي والدفع</b></p>
        <p>المستوى: <b>{level_label}</b> &nbsp;|&nbsp; إجمالي النقاط: <b>{st.session_state["total_xp"]} XP</b> &nbsp;|&nbsp; الوقت الكلي: <b>{fmt_time(total_time)}</b></p>
    </div>
    """, unsafe_allow_html=True)

    cert_text = f"""شهادة إتمام
=================
الطالب/ـة: {name_display}
الدرس: الزخم الخطي والدفع وحفظ الزخم
عدد التمارين المكتملة: {len(st.session_state["completed_questions"])} / {TOTAL_QUESTIONS}
إجمالي نقاط الخبرة: {st.session_state["total_xp"]} XP
المستوى: {level_label}
الوقت الكلي: {fmt_time(total_time)}
الأوسمة: {', '.join(sorted(st.session_state["badges"])) if st.session_state["badges"] else "لا يوجد"}
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
  var physObserver = null;
  var physResizeHandler = null;
  var physBackHandler = null;
  var physCommitGuardHandler = null;
  var physStopped = false;
  var physBootTimer1 = null;
  var physBootTimer2 = null;
  var physMutationTimer = null;

  /* أوقف أي نسخة أقدم من سكربت التمارين قبل إنشاء نسخة جديدة. */
  if (typeof win.__studentSamedExerciseCleanup === 'function') {
    try { win.__studentSamedExerciseCleanup(); } catch (e0) {}
  }

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
    physCommitGuardHandler = function (e) {
      var t = e.target;
      if (!t || !t.closest) return;
      if (t.closest('input.phys-slot-input')) return;
      if (!t.closest('button')) return;
      var inp = doc.querySelector('input.phys-final-input');
      if (!inp) return;
      if (commitTimer) { win.clearTimeout(commitTimer); commitTimer = 0; }
      commitValue(inp.value || '');
    };
    doc.addEventListener('mousedown', physCommitGuardHandler, true);
    doc.addEventListener('touchstart', physCommitGuardHandler, true);
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
    if (physStopped) return;
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

  function removePhysNode(id) {
    var el = doc.getElementById(id);
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }

  function cleanupExerciseUi() {
    if (physStopped) return;
    physStopped = true;

    if (physObserver) { try { physObserver.disconnect(); } catch (e1) {} physObserver = null; }
    if (physMutationTimer) { win.clearTimeout(physMutationTimer); physMutationTimer = null; }
    if (physBootTimer1) { win.clearTimeout(physBootTimer1); physBootTimer1 = null; }
    if (physBootTimer2) { win.clearTimeout(physBootTimer2); physBootTimer2 = null; }
    if (commitTimer) { win.clearTimeout(commitTimer); commitTimer = 0; }

    doc.removeEventListener('scroll', update, true);
    win.removeEventListener('scroll', update, false);
    if (physResizeHandler) win.removeEventListener('resize', physResizeHandler, false);
    if (physBackHandler) doc.removeEventListener('click', physBackHandler, true);
    if (physCommitGuardHandler) {
      doc.removeEventListener('mousedown', physCommitGuardHandler, true);
      doc.removeEventListener('touchstart', physCommitGuardHandler, true);
    }

    try { clearReserve(); } catch (e2) {}
    removePhysNode(DOCK_ID);
    removePhysNode(CLONE_ID);
    removePhysNode(TAB_ID);
    doc.documentElement.classList.remove('phys-js');
    if (doc.body && doc.body.dataset.physCommitGuard) delete doc.body.dataset.physCommitGuard;
    if (win.__studentSamedExerciseCleanup === cleanupExerciseUi) {
      try { delete win.__studentSamedExerciseCleanup; } catch (e3) { win.__studentSamedExerciseCleanup = null; }
    }
  }

  win.__studentSamedExerciseCleanup = cleanupExerciseUi;

  /* نظّف اللوحات قبل أن يعيد زر الصفحة الرئيسية تشغيل Streamlit. */
  physBackHandler = function (e) {
    var t = e.target;
    var btn = (t && t.closest) ? t.closest('.st-key-samed_back button') : null;
    if (btn) cleanupExerciseUi();
  };
  doc.addEventListener('click', physBackHandler, true);
  window.addEventListener('pagehide', cleanupExerciseUi, { once: true });

  /* أي تمرير داخل أي حاوية (مرحلة الالتقاط) */
  doc.addEventListener('scroll', update, { capture: true, passive: true });
  win.addEventListener('scroll', update, { passive: true });
  physResizeHandler = function () {
    natRight = null;
    setReserve(0);
    update();
  };
  win.addEventListener('resize', physResizeHandler, { passive: true });

  update();
  physBootTimer1 = win.setTimeout(update, 250);
  physBootTimer2 = win.setTimeout(update, 900);

  physObserver = new MutationObserver(function () {
    if (physStopped) return;
    if (physMutationTimer) win.clearTimeout(physMutationTimer);
    physMutationTimer = win.setTimeout(update, 100);
  });
  physObserver.observe(doc.body, { childList: true, subtree: true });
})();
</script>
""",
    height=0,
)


# FINAL_UI_V18_EXERCISE_THEME
if st.session_state.get("samed_view") == "app":
    apply_ui_theme("exercise")
    apply_exercise_ui_v18()
    render_exercise_footer_v18("app.py")
