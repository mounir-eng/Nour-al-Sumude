"""Professional lesson-first Streamlit renderer for remedial unit reviews."""
from __future__ import annotations

import html
import math
import re
from typing import Any

import streamlit as st
from ui_theme_v13 import apply_ui_theme


_BASE_CSS = r"""
<style>
[data-testid="stHeader"], footer {display:none!important}
.stApp{background:#f4f7fb;color:#183249}
.block-container{max-width:1180px!important;padding:14px 22px 56px!important}
.rv-topline{display:flex;align-items:center;gap:10px;color:#607486;font-size:11px;margin:2px 0 8px}
.rv-topline b{color:#17364d}
.rv-hero{background:linear-gradient(135deg,var(--rv-deep),var(--rv-accent));color:white;border-radius:25px;padding:25px 27px;display:grid;grid-template-columns:minmax(0,1fr) 185px;gap:22px;align-items:center;box-shadow:0 18px 42px rgba(15,53,79,.17);overflow:hidden;position:relative}
.rv-hero:after{content:"";position:absolute;width:240px;height:240px;border-radius:50%;background:rgba(255,255,255,.07);left:-80px;top:-120px}
.rv-hero-copy,.rv-progress{position:relative;z-index:1}.rv-kicker{display:inline-flex;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.16);border-radius:99px;padding:5px 10px;font-size:10px;font-weight:900}
.rv-hero h1{font-size:29px;margin:9px 0 5px}.rv-hero p{margin:0;color:#e4f3f7;line-height:1.8;font-size:13px}.rv-source{margin-top:12px!important;font-size:10px!important;color:#cce5ec!important}
.rv-progress{text-align:center;border-right:1px solid rgba(255,255,255,.18);padding-right:20px}.rv-ring{width:98px;height:98px;border-radius:50%;display:grid;place-items:center;margin:0 auto 8px;position:relative}.rv-ring:after{content:"";position:absolute;inset:9px;background:var(--rv-deep);border-radius:50%}.rv-ring b{position:relative;z-index:1;font-size:22px}.rv-progress span,.rv-progress small{display:block}.rv-progress span{font-size:11px;font-weight:900}.rv-progress small{font-size:9px;color:#d6ebf1;margin-top:2px}
.rv-route{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0 18px}.rv-route-item{background:#fff;border:1px solid #dde7ee;border-radius:13px;padding:9px 11px;display:flex;gap:8px;align-items:center;color:#657887;font-size:10px;font-weight:800}.rv-route-item b{width:25px;height:25px;border-radius:50%;display:grid;place-items:center;background:#edf3f7;color:#6b7c89}.rv-route-item.active{border-color:var(--rv-accent);color:var(--rv-deep);background:var(--rv-soft)}.rv-route-item.active b{background:var(--rv-accent);color:white}
.rv-map-title{display:flex;justify-content:space-between;align-items:end;margin:20px 2px 8px}.rv-map-title h2{margin:0;font-size:19px}.rv-map-title small{font-size:9px;color:#85949f}.rv-map{display:flex;gap:8px;overflow-x:auto;padding:2px 1px 8px;scrollbar-width:thin}.rv-map-node{min-width:142px;border:1px solid #dde6ec;background:#fff;border-radius:13px;padding:10px 11px;color:#536a7a}.rv-map-node b{display:block;font-size:10px;color:#193c54;margin-bottom:4px}.rv-map-node small{font-size:8px;color:#83919b}.rv-map-node.done{border-color:#9fddcf;background:#effbf8}.rv-map-node.current{border-color:var(--rv-accent);box-shadow:0 0 0 2px var(--rv-soft)}
.rv-lesson-head{background:#fff;border:1px solid #dce6ed;border-right:5px solid var(--rv-accent);border-radius:18px;padding:19px 21px;margin:13px 0 10px;box-shadow:0 8px 24px rgba(26,61,83,.055)}.rv-lesson-head .tag{display:inline-flex;background:var(--rv-soft);color:var(--rv-deep);padding:4px 8px;border-radius:99px;font-size:9px;font-weight:900}.rv-lesson-head h2{margin:8px 0 5px;font-size:24px;color:#18364c}.rv-lesson-head p{margin:0;color:#657986;font-size:12px;line-height:1.75}
.rv-card{background:#fff;border:1px solid #dfe8ee;border-radius:17px;padding:18px 19px;margin-bottom:10px;box-shadow:0 7px 22px rgba(20,56,79,.045)}.rv-card h3{margin:0 0 10px;color:#18384f;font-size:16px}.rv-story{background:linear-gradient(135deg,#fffaf0,#fff);border:1px solid #f1d9a9;border-radius:15px;padding:14px 15px;margin-bottom:10px;color:#684d1e;line-height:1.85;font-size:12px}.rv-story b{color:#9a620d}.rv-paragraph{font-size:13px;line-height:1.95;color:#405969;margin:0 0 9px}.rv-points{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:10px}.rv-point{background:#f5f8fa;border-radius:11px;padding:9px;color:#526b7c;font-size:10px;font-weight:750;border:1px solid #e8eef2}
.rv-formula{background:linear-gradient(135deg,var(--rv-deep),#123f5b);border-radius:17px;padding:18px;color:#fff;margin:10px 0}.rv-formula small{display:block;color:#cde3eb;font-size:9px;margin-bottom:8px}.rv-equation{direction:ltr;unicode-bidi:isolate;text-align:center;font-family:Consolas,"Courier New",monospace;font-size:22px;font-weight:900;letter-spacing:.2px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.13);border-radius:11px;padding:11px}.rv-formula p{margin:8px 0 0;color:#d9eaf0;font-size:10px;line-height:1.7}
.rv-symbols{display:grid;gap:6px}.rv-symbol{display:grid;grid-template-columns:52px 1fr;gap:8px;align-items:center;background:#f7f9fb;border:1px solid #e7edf1;border-radius:10px;padding:8px}.rv-symbol code{direction:ltr;unicode-bidi:isolate;text-align:center;color:var(--rv-deep);font-weight:900;font-size:13px}.rv-symbol span{font-size:9px;color:#647986}.rv-symbol small{display:block;color:#96a2aa;font-size:8px;margin-top:2px}
.rv-support{background:#f8f5ff;border:1px solid #e4d9fa;border-radius:13px;padding:12px;color:#5e4b7b;font-size:10px;line-height:1.75}.rv-memory{background:#ecfaf6;border:1px solid #c7eadf;border-radius:13px;padding:12px;color:#176d5d;font-size:10px;line-height:1.75}.rv-mistake{background:#fff4f3;border:1px solid #f2d0cc;border-radius:13px;padding:12px;color:#915049;font-size:10px;line-height:1.75;margin-top:8px}
.rv-example-head{display:flex;justify-content:space-between;gap:10px;align-items:start}.rv-example-head span{background:#eef8ff;color:#306b8f;border-radius:99px;padding:5px 8px;font-size:8px;font-weight:900;white-space:nowrap}.rv-example-head h3{margin:0 0 4px}.rv-example-q{color:#607684;font-size:11px;line-height:1.7;margin:0 0 12px}.rv-givens{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:11px}.rv-givens span{direction:ltr;unicode-bidi:isolate;background:#f1f5f8;border:1px solid #e1e9ef;border-radius:8px;padding:5px 8px;font-family:Consolas,monospace;font-size:9px;color:#294c65}.rv-plan{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:9px 0}.rv-plan div{background:#fafbfc;border:1px solid #e7edf1;border-radius:10px;padding:8px;font-size:9px;color:#617483}.rv-plan b{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--rv-accent);color:#fff;margin-left:4px}.rv-substitution{direction:ltr;unicode-bidi:isolate;text-align:center;background:var(--rv-soft);border:1px dashed var(--rv-accent);border-radius:12px;padding:10px;font-family:Consolas,monospace;font-weight:800;color:var(--rv-deep);margin:9px 0 4px}
.rv-solution{background:#eefaf6;border:1px solid #bde5d9;border-radius:14px;padding:13px;margin-top:10px}.rv-solution b{color:#12715f;font-size:11px}.rv-solution-line{direction:ltr;unicode-bidi:isolate;text-align:center;background:#fff;border-radius:8px;padding:7px;margin-top:5px;font-family:Consolas,monospace;color:#244e63;font-size:11px}.rv-interpret{font-size:9px;color:#55746d;margin-top:8px;line-height:1.7}.rv-complete{background:linear-gradient(135deg,#e8faf5,#fff);border:1px solid #b7e4d8;border-radius:15px;padding:13px;color:#176e5f;text-align:center;font-size:11px;font-weight:850;margin:10px 0}
.rv-viz{min-height:165px;border-radius:16px;background:linear-gradient(145deg,#f7fbfd,#eef5f8);border:1px solid #dce9ef;display:grid;place-items:center;overflow:hidden;padding:14px;margin:10px 0}.viz-row{display:flex;align-items:center;justify-content:center;gap:16px;width:100%;direction:ltr}.viz-big{font-size:42px}.viz-arrow{font-family:Consolas,monospace;color:var(--rv-accent);font-size:25px;font-weight:900}.viz-label{font-family:Consolas,monospace;color:#244c65;font-size:12px;font-weight:800;direction:ltr}.viz-stack{display:grid;gap:8px;width:min(92%,460px);direction:ltr}.viz-level{height:3px;background:#7fa7bb;position:relative}.viz-level span{position:absolute;right:0;top:-17px;color:#42647a;font:10px Consolas}.viz-level.hot{background:#e7902f}.viz-boxes{display:flex;gap:8px;direction:ltr}.viz-box{width:46px;height:42px;border:2px solid #7597aa;border-radius:5px;display:grid;place-items:center;color:#174e6c;font:20px Consolas;background:white}.viz-wave{font-size:34px;color:var(--rv-accent);letter-spacing:3px;direction:ltr}.viz-graph{width:300px;height:130px;border-left:3px solid #385c72;border-bottom:3px solid #385c72;position:relative}.viz-graph:after{content:"";position:absolute;left:20px;bottom:0;border-left:120px solid transparent;border-right:120px solid transparent;border-bottom:105px solid rgba(20,151,135,.24);transform:rotate(0deg);transform-origin:bottom}.viz-caption{font-size:9px;color:#607986;text-align:center;margin-top:8px}
@media(max-width:780px){.block-container{padding:9px 10px 42px!important}.rv-hero{grid-template-columns:1fr;padding:21px 17px}.rv-hero h1{font-size:24px}.rv-progress{border-right:0;border-top:1px solid rgba(255,255,255,.16);padding:14px 0 0;display:flex;align-items:center;justify-content:center;gap:12px}.rv-ring{width:70px;height:70px;margin:0}.rv-route,.rv-points,.rv-plan{grid-template-columns:1fr}.rv-map-node{min-width:126px}.rv-lesson-head h2{font-size:20px}}

/* RTL_TYPOGRAPHY_V10 */
.stApp,[data-testid="stAppViewContainer"],.block-container{direction:rtl!important;text-align:right!important;font-family:"Noto Sans Arabic",Tahoma,Arial,sans-serif!important}
[data-testid="stMarkdownContainer"],.rv-hero-copy,.rv-card,.rv-story,.rv-lesson-head,.rv-route-item,.rv-map-node,.rv-support,.rv-memory,.rv-mistake{direction:rtl!important;text-align:right!important}
.rv-paragraph,.rv-point,.rv-example-q,.rv-plan div,.rv-formula p,.rv-interpret,.rv-symbol span,.rv-story,.rv-support,.rv-memory,.rv-mistake{unicode-bidi:plaintext!important}
.rv-ltr{direction:ltr!important;unicode-bidi:isolate!important;display:inline-block!important;white-space:nowrap!important;font-family:Consolas,"Courier New",monospace!important}
.rv-equation,.rv-substitution{direction:ltr!important;unicode-bidi:isolate!important;text-align:center!important}
.rv-givens span,.rv-solution-line{direction:rtl!important;unicode-bidi:plaintext!important;text-align:center!important}
.rv-symbol code,.rv-symbol small{direction:ltr!important;unicode-bidi:isolate!important}
.viz-label,.viz-caption{direction:rtl!important;unicode-bidi:plaintext!important;text-align:center!important}
.rv-topline{font-size:14px!important}.rv-kicker{font-size:13px!important}.rv-hero h1{font-size:36px!important}.rv-hero p{font-size:16px!important}.rv-source{font-size:13px!important}.rv-progress b{font-size:28px!important}.rv-progress span{font-size:14px!important}.rv-progress small{font-size:12px!important}
.rv-route-item{font-size:14px!important}.rv-route-item small{font-size:12px!important}.rv-map-title h2{font-size:24px!important}.rv-map-title small{font-size:12px!important}.rv-map-node{min-width:178px!important}.rv-map-node b{font-size:13px!important;line-height:1.65!important}.rv-map-node small{font-size:11px!important}
.rv-lesson-head .tag{font-size:12px!important}.rv-lesson-head h2{font-size:30px!important}.rv-lesson-head p{font-size:16px!important}.rv-card h3{font-size:21px!important}.rv-story{font-size:16px!important}.rv-paragraph{font-size:17px!important;line-height:2!important}.rv-point{font-size:14px!important;line-height:1.75!important}
.rv-formula small{font-size:13px!important}.rv-equation{font-size:28px!important}.rv-formula p{font-size:14px!important}.rv-example-head h3{font-size:21px!important}.rv-example-head span{font-size:11px!important}.rv-example-q{font-size:15px!important;line-height:1.9!important}.rv-givens span{font-size:13px!important}.rv-plan div{font-size:13px!important;line-height:1.7!important}.rv-substitution{font-size:18px!important}
.rv-symbol code{font-size:18px!important}.rv-symbol span{font-size:14px!important}.rv-symbol small{font-size:12px!important}.rv-support,.rv-memory,.rv-mistake{font-size:14px!important}.rv-solution b{font-size:15px!important}.rv-solution-line{font-size:16px!important}.rv-interpret{font-size:14px!important}.rv-complete{font-size:15px!important}.viz-label{font-size:16px!important}.viz-caption{font-size:13px!important}
.stTextInput label p,.stSelectbox label p{font-size:14px!important;direction:rtl!important;text-align:right!important;unicode-bidi:plaintext!important}.stTextInput input{font-size:16px!important;direction:ltr!important;text-align:left!important;unicode-bidi:isolate!important}.stButton button,.stFormSubmitButton button{font-size:15px!important}.stSelectbox div[data-baseweb="select"]>div{font-size:15px!important;direction:rtl!important;text-align:right!important}
@media(max-width:780px){.rv-hero h1{font-size:29px!important}.rv-hero p{font-size:15px!important}.rv-lesson-head h2{font-size:25px!important}.rv-paragraph{font-size:16px!important}.rv-story{font-size:15px!important}.rv-card h3,.rv-example-head h3{font-size:19px!important}.rv-map-node{min-width:160px!important}.rv-equation{font-size:23px!important}.rv-substitution{font-size:16px!important}}

</style>
"""




# FOUNDATION_LARGE_TYPE_V11
_EXTRA_LARGE_CSS = r"""
<style>
.rv-paragraph{font-size:20px!important;line-height:2.08!important}.rv-story{font-size:19px!important;line-height:2!important}.rv-card h3,.rv-example-head h3{font-size:24px!important}.rv-lesson-head h2{font-size:33px!important}.rv-lesson-head p{font-size:19px!important;line-height:1.9!important}.rv-hero h1{font-size:39px!important}.rv-hero p{font-size:19px!important;line-height:1.95!important}.rv-source{font-size:15px!important}.rv-point{font-size:17px!important;line-height:1.9!important}.rv-example-q{font-size:18px!important;line-height:2!important}.rv-plan div{font-size:16px!important;line-height:1.9!important}.rv-givens span{font-size:15px!important}.rv-formula p{font-size:17px!important;line-height:1.9!important}.rv-equation{font-size:31px!important}.rv-substitution{font-size:21px!important}.rv-field label{font-size:16px!important;line-height:1.8!important}.rv-field input{font-size:18px!important}.rv-option{font-size:17px!important;line-height:1.85!important}.rv-action,.rv-nav button{font-size:17px!important}.rv-support,.rv-memory,.rv-mistake{font-size:17px!important;line-height:1.95!important}.rv-symbol span{font-size:16px!important}.rv-symbol small{font-size:14px!important}.rv-symbol code{font-size:20px!important}.rv-solution>b{font-size:18px!important}.rv-solution-line{font-size:19px!important}.rv-interpret{font-size:17px!important;line-height:1.9!important}.rv-map button b{font-size:15px!important;line-height:1.8!important}.rv-map button small{font-size:13px!important}.rv-map-head small{font-size:14px!important}.rv-kicker,.rv-route>div{font-size:15px!important}.rv-route small{font-size:13px!important}.rv-lesson-head .tag{font-size:14px!important}.viz-caption{font-size:16px!important}.viz-label{font-size:18px!important}div[data-testid="stTextInput"] label p,div[data-testid="stSelectbox"] label p{font-size:17px!important;line-height:1.8!important}div[data-baseweb="input"] input,div[data-baseweb="select"]{font-size:18px!important}
@media(max-width:820px){.rv-paragraph{font-size:19px!important}.rv-story{font-size:18px!important}.rv-card h3,.rv-example-head h3{font-size:22px!important}.rv-lesson-head h2{font-size:28px!important}.rv-lesson-head p{font-size:18px!important}.rv-hero h1{font-size:32px!important}.rv-hero p{font-size:18px!important}.rv-equation{font-size:26px!important}.rv-substitution{font-size:19px!important}.rv-field label{font-size:16px!important}}
</style>
"""


# FOUNDATION_SIMPLE_INLINE_V12
_FOUNDATION_SIMPLE_CSS_V12 = r"""
<style>
.rv-simple-sentence{background:#eef9ff;border:2px solid #a9d8ee;border-radius:17px;padding:16px 18px;margin:0 0 10px;color:#173f59;font-size:22px!important;line-height:2!important;font-weight:850;direction:rtl;text-align:right;unicode-bidi:plaintext}
.rv-simple-sentence b{color:var(--rv-accent);font-size:18px}
.rv-vector-note{direction:ltr!important;unicode-bidi:isolate!important;text-align:center!important;background:#fff;border:2px solid var(--rv-accent);border-radius:15px;padding:13px 15px;margin:8px 0 12px;font:900 23px/1.8 Consolas,"Noto Sans Arabic",monospace;color:var(--rv-deep)}
.rv-symbolic-copy{background:#f7fafc;border:1px solid #dce7ed;border-radius:14px;padding:12px;margin-top:10px}.rv-symbolic-copy>small{display:block;font-size:16px;color:#617887;font-weight:850;margin-bottom:5px}
.rv-inline-guide{direction:rtl;text-align:right;background:#fff7e8;border:1px solid #f0d29a;border-radius:13px;padding:12px 14px;margin-bottom:10px;font-size:18px;line-height:1.9;color:#76551e}.rv-inline-guide b{display:block;color:#8f5e08;font-size:20px}
.rv-inline-next{direction:rtl;text-align:right;font-size:18px;font-weight:850;color:#425f72;margin:13px 2px 6px}
.rv-inline-token{direction:ltr!important;unicode-bidi:isolate!important;display:flex;align-items:center;justify-content:center;min-height:54px;white-space:nowrap;font:900 25px Consolas,"Courier New",monospace;color:var(--rv-deep)}
div[data-testid="stForm"]:has(.rv-inline-guide){background:#f8fbfd;border:2px solid #d5e4ec;border-radius:17px;padding:14px!important}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stHorizontalBlock"]{direction:ltr!important;align-items:center!important;gap:.35rem!important;overflow-x:auto;padding:3px 2px 7px}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"]{min-width:74px!important}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"] input{direction:ltr!important;text-align:center!important;font:900 22px Consolas,"Courier New",monospace!important;color:var(--rv-deep)!important;background:#fff!important;border:0!important;border-bottom:3px solid var(--rv-accent)!important;border-radius:8px 8px 3px 3px!important;padding:8px 5px!important;min-width:72px!important}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"] input:focus{box-shadow:0 0 0 3px var(--rv-soft)!important}
@media(max-width:820px){.rv-simple-sentence{font-size:20px!important}.rv-vector-note{font-size:19px!important}.rv-inline-guide,.rv-inline-next{font-size:17px!important}.rv-inline-token{font-size:21px!important;min-height:49px}div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"]{min-width:64px!important}div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"] input{font-size:20px!important;min-width:62px!important}}
</style>
"""


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


_ARABIC_PART_RE = re.compile(r"([\u0600-\u06FF]+)")
_TECH_PART_RE = re.compile(r"[A-Za-z0-9\u0370-\u03FF\u2070-\u209F↑↓∞]")
_EDGE_PART_RE = re.compile(r"^(\s*)(.*?)([\s.,;:!?]*)$", re.S)


def _mixed(value: Any) -> str:
    """Safe HTML for an RTL sentence with isolated LTR scientific fragments."""
    out: list[str] = []
    for part in _ARABIC_PART_RE.split(str(value)):
        if not part:
            continue
        if _ARABIC_PART_RE.search(part) or not _TECH_PART_RE.search(part):
            out.append(_esc(part))
            continue
        match = _EDGE_PART_RE.match(part)
        if not match:
            out.append(_esc(part))
            continue
        lead, core, tail = match.groups()
        out.append(_esc(lead))
        if core:
            out.append(f'<bdi class="rv-ltr" dir="ltr">{_esc(core)}</bdi>')
        out.append(_esc(tail))
    return "".join(out)


def _plain_mixed(value: Any) -> str:
    """Plain text equivalent for native Streamlit labels and notices."""
    out: list[str] = []
    for part in _ARABIC_PART_RE.split(str(value)):
        if not part:
            continue
        if _ARABIC_PART_RE.search(part) or not _TECH_PART_RE.search(part):
            out.append(part)
            continue
        match = _EDGE_PART_RE.match(part)
        if not match:
            out.append(part)
            continue
        lead, core, tail = match.groups()
        out.append(lead + (f"\u2066{core}\u2069" if core else "") + tail)
    return "".join(out)


def _parse_number(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    digits = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
    text = text.translate(digits).replace("−", "-").replace("٫", ".").replace("،", ".").replace(",", ".")
    text = text.replace("×", "*").replace("·", "*").replace(" ", "")
    m = re.fullmatch(r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))\*?10\^?([+-]?\d+)", text, flags=re.I)
    if m:
        try:
            return float(m.group(1)) * (10 ** int(m.group(2)))
        except Exception:
            return None
    try:
        return float(text)
    except Exception:
        return None


def _near(actual: float | None, expected: float, tol: float | None = None) -> bool:
    if actual is None or not math.isfinite(actual):
        return False
    if tol is None:
        tol = max(abs(expected) * 0.005, 1e-40 if expected else 1e-9)
    return abs(actual - expected) <= tol


def _visual(kind: str) -> str:
    foundation_visuals = {
        'foundation_units': '<div class="viz-row"><span class="viz-box">km/h</span><span class="viz-arrow">÷3.6 →</span><span class="viz-box">m/s</span></div><div class="viz-caption">وحّد الوحدات قبل الحساب</div>',
        'foundation_vectors': '<div class="viz-row"><span class="viz-arrow">◀ 11 N</span><span class="viz-big">📦</span><span class="viz-arrow">18 N ▶</span></div><div class="viz-caption">اجمع المتجهات بالإشارات</div>',
        'foundation_motion': '<div class="viz-row"><span class="viz-box">−5 m</span><span class="viz-arrow">────▶</span><span class="viz-box">+13 m</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">Δx=x_f−x_i</bdi></div>',
        'foundation_acceleration': '<div class="viz-row"><span class="viz-box">4 m/s</span><span class="viz-arrow">3 s →</span><span class="viz-box">16 m/s</span></div><div class="viz-caption">تغير السرعة في كل ثانية</div>',
        'foundation_newton2': '<div class="viz-row"><span class="viz-arrow">◀ 8 N</span><span class="viz-big">🛒</span><span class="viz-arrow">24 N ▶</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">ΣF=ma</bdi></div>',
        'foundation_newton3': '<div class="viz-row"><span class="viz-big">✋</span><span class="viz-arrow">45 N ▶</span><span class="viz-big">🧱</span><span class="viz-arrow">◀ 45 N</span></div><div class="viz-caption">قوتان على جسمين مختلفين</div>',
        'foundation_energy': '<div class="viz-row"><span class="viz-label">v ×2</span><span class="viz-arrow">→</span><span class="viz-label">K ×4</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">K=½mv²</bdi></div>',
        'foundation_bridge': '<div class="viz-row"><span class="viz-box">FΔt</span><span class="viz-arrow">⇄</span><span class="viz-box">mΔv</span></div><div class="viz-caption">الجسر إلى الدفع والزخم</div>',
        'foundation_matter': '<div class="viz-row"><span class="viz-box">H</span><span class="viz-arrow">—</span><span class="viz-box">O</span><span class="viz-arrow">—</span><span class="viz-box">H</span></div><div class="viz-caption">رموز الذرات في الجزيء</div>',
        'foundation_particles': '<div class="viz-row"><span class="viz-box">p⁺</span><span class="viz-box">n⁰</span><span class="viz-arrow">نواة</span><span class="viz-box">e⁻</span></div><div class="viz-caption">الموقع والشحنة</div>',
        'foundation_nuclear': '<div class="viz-row"><span class="viz-big"><bdi class="rv-ltr" dir="ltr">²⁷₁₃Al</bdi></span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">A</bdi> أعلى و<bdi class="rv-ltr" dir="ltr">Z</bdi> أسفل</div>',
        'foundation_isotopes': '<div class="viz-row"><span class="viz-box">³⁵Cl</span><span class="viz-arrow">نفس Z</span><span class="viz-box">³⁷Cl</span></div><div class="viz-caption">نظائر العنصر نفسه</div>',
        'foundation_models': '<div class="viz-row"><span class="viz-label">دالتون</span><span class="viz-arrow">→</span><span class="viz-label">طومسون</span><span class="viz-arrow">→</span><span class="viz-label">رذرفورد</span></div><div class="viz-caption">الدليل يطوّر النموذج</div>',
        'foundation_ions': '<div class="viz-row"><span class="viz-box">Cl</span><span class="viz-arrow">+e⁻ →</span><span class="viz-box">Cl⁻</span></div><div class="viz-caption">اكتساب الإلكترون يعطي أيونًا سالبًا</div>',
        'foundation_shells': '<div class="viz-row"><span class="viz-big">◎</span><span class="viz-label"><bdi class="rv-ltr" dir="ltr">2n²</bdi></span></div><div class="viz-caption">سعة مستويات الطاقة</div>',
        'foundation_valence': '<div class="viz-row"><span class="viz-box">2</span><span class="viz-box">8</span><span class="viz-box">2</span></div><div class="viz-caption">العدد الأخير إلكترونات التكافؤ</div>',
    }
    if kind in foundation_visuals:
        return '<div class="rv-viz">' + foundation_visuals[kind] + '</div>'
    visuals = {
        "momentum": '<div><div class="viz-row"><span class="viz-big">🚚</span><span class="viz-arrow">────▶</span></div><div class="viz-row"><span class="viz-label"><bdi class="rv-ltr" dir="ltr">m</bdi> كبير</span><span class="viz-label">v</span><span class="viz-label">P = mv</span></div><div class="viz-caption">الكتلة والسرعة معًا تحددان الزخم</div></div>',
        "delta": '<div><div class="viz-row"><span class="viz-arrow">vᵢ  ────▶</span><span class="viz-big">⚽</span><span class="viz-arrow">◀──  v_f</span></div><div class="viz-caption">ارسم الاتجاهين قبل كتابة <bdi class="rv-ltr" dir="ltr">v_f − v_i</bdi></div></div>',
        "impulse": '<div><div class="viz-row"><span class="viz-big">🦶</span><span class="viz-arrow">F × Δt ───▶</span><span class="viz-big">⚽</span></div><div class="viz-caption">القوة والزمن يصنعان الدفع معًا</div></div>',
        "graph": '<div><div class="viz-graph"></div><div class="viz-caption">المساحة تحت منحنى <bdi class="rv-ltr" dir="ltr">F–t</bdi> هي الدفع</div></div>',
        "safety": '<div><div class="viz-row"><span class="viz-label"><bdi class="rv-ltr" dir="ltr">Δt</bdi> صغير → <bdi class="rv-ltr" dir="ltr">|F|</bdi> كبير</span><span class="viz-big">💥</span></div><div class="viz-row"><span class="viz-label"><bdi class="rv-ltr" dir="ltr">Δt</bdi> أكبر → <bdi class="rv-ltr" dir="ltr">|F|</bdi> أصغر</span><span class="viz-big">🛡️</span></div></div>',
        "conservation": '<div><div class="viz-row"><span class="viz-big">🛶</span><span class="viz-arrow">◀── P₂</span><span class="viz-arrow">P₁ ──▶</span><span class="viz-big">📦</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">P₁ + P₂ = 0</bdi> عندما بدأ النظام ساكنًا</div></div>',
        "energy": '<div><div class="viz-row"><span class="viz-label"><bdi class="rv-ltr" dir="ltr">P = mv</bdi> (متجه)</span><span class="viz-big">≠</span><span class="viz-label"><bdi class="rv-ltr" dir="ltr">K = ½mv²</bdi> (قياسي)</span></div><div class="viz-caption">قد يحفظ الزخم بينما تتحول الطاقة الحركية</div></div>',
        "wave": '<div><div class="viz-wave">∿∿∿∿∿</div><div class="viz-row"><span class="viz-label"><bdi class="rv-ltr" dir="ltr">λ</bdi> كبير</span><span class="viz-label"><bdi class="rv-ltr" dir="ltr">ν</bdi> صغير</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">c = λν</bdi> ثابتة في الفراغ</div></div>',
        "photon": '<div><div class="viz-row"><span class="viz-big">✨</span><span class="viz-arrow">E = hν</span><span class="viz-big">✨✨✨</span></div><div class="viz-caption">تردد أعلى يعني فوتونًا أعلى طاقة</div></div>',
        "levels": '<div class="viz-stack"><div class="viz-level hot"><span>n = 4</span></div><div class="viz-level"><span>n = 3</span></div><div class="viz-level"><span>n = 2</span></div><div class="viz-level"><span>n = 1</span></div><div class="viz-caption">طاقات مسموحة منفصلة مثل درجات السلم</div></div>',
        "transition": '<div class="viz-stack"><div class="viz-level hot"><span>n = 3</span></div><div class="viz-row"><span class="viz-arrow">↓ photon</span></div><div class="viz-level"><span>n = 2</span></div><div class="viz-caption">فرق الطاقة يخرج في فوتون محدد</div></div>',
        "orbitals": '<div><div class="viz-boxes"><span class="viz-box">−2</span><span class="viz-box">−1</span><span class="viz-box">0</span><span class="viz-box">+1</span><span class="viz-box">+2</span></div><div class="viz-caption">لـ <bdi class="rv-ltr" dir="ltr">d</bdi> حيث <bdi class="rv-ltr" dir="ltr">l = 2</bdi> توجد خمس قيم لـ <bdi class="rv-ltr" dir="ltr">m_l</bdi></div></div>',
        "shells": '<div><div class="viz-row"><span class="viz-big">◎</span><span class="viz-label"><bdi class="rv-ltr" dir="ltr">n²</bdi> أفلاك</span><span class="viz-label"><bdi class="rv-ltr" dir="ltr">2n²</bdi> إلكترونات</span></div><div class="viz-caption">كل فلك يسع إلكترونين كحد أقصى</div></div>',
        "configuration": '<div><div class="viz-boxes"><span class="viz-box">↑↓</span><span class="viz-box">↑</span><span class="viz-box">↑</span><span class="viz-box">↑</span></div><div class="viz-caption">أوفباو يرتب، باولي يزاوج، هوند يوزع فرادى</div></div>',
        "magnetism": '<div><div class="viz-boxes"><span class="viz-box">↑↓</span><span class="viz-box">↑</span><span class="viz-box">↑</span><span class="viz-box">↑</span><span class="viz-box">↑</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">d⁶</bdi>: أربعة أسهم مفردة → بارامغناطيسية</div></div>',
    }
    return '<div class="rv-viz">' + visuals.get(kind, '<div class="viz-caption">نموذج المفهوم</div>') + '</div>'


def _init(course: dict[str, Any]) -> tuple[str, set[str]]:
    prefix = course["prefix"]
    completed_key = f"{prefix}_completed_questions"
    xp_key = f"{prefix}_total_xp"
    current = st.session_state.get(completed_key, set())
    if not isinstance(current, set):
        current = set(current or [])
    st.session_state[completed_key] = current
    st.session_state.setdefault(xp_key, 0)
    return completed_key, current


def _reset_lesson(prefix: str, lesson_id: str, completed_key: str) -> None:
    for suffix in ("example_ok", "checkpoint_ok", "example_msg", "checkpoint_msg", "attempts"):
        st.session_state.pop(f"{prefix}_{lesson_id}_{suffix}", None)
    for key in list(st.session_state.keys()):
        if str(key).startswith(f"{prefix}_{lesson_id}_field_") or str(key) == f"{prefix}_{lesson_id}_result" or str(key) == f"{prefix}_{lesson_id}_choice":
            st.session_state.pop(key, None)
    done = st.session_state.get(completed_key, set())
    if lesson_id in done:
        done.discard(lesson_id)


def _render_videos(course: dict[str, Any], heading: str, note: str) -> None:
    videos = course.get("videos") or []
    if not videos:
        return
    st.markdown(
        '<div class="rv-map-title"><h2>' + heading + '</h2><small>' + note + '</small></div>',
        unsafe_allow_html=True,
    )
    if len(videos) == 1:
        video = videos[0]
        st.markdown('<div class="rv-video-title">' + _mixed(video["title"]) + '</div>', unsafe_allow_html=True)
        st.video(video["url"])
        st.markdown('<a class="rv-video-link" href="' + _esc(video["url"]) + '" target="_blank">فتح على يوتيوب ↗</a>', unsafe_allow_html=True)
        return
    tabs = st.tabs([_plain_mixed(v["title"]) for v in videos])
    for tab, video in zip(tabs, videos):
        with tab:
            st.markdown('<div class="rv-video-title">' + _mixed(video["title"]) + '</div>', unsafe_allow_html=True)
            st.video(video["url"])
            st.markdown('<a class="rv-video-link" href="' + _esc(video["url"]) + '" target="_blank">فتح على يوتيوب ↗</a>', unsafe_allow_html=True)


def render_foundation_course(course: dict[str, Any]) -> None:
    st.set_page_config(page_title=f"تأسيس {course['title']}", page_icon=course["icon"], layout="wide", initial_sidebar_state="collapsed")
    completed_key, completed = _init(course)
    prefix = course["prefix"]
    lessons = course["lessons"]
    accent = "#0d8c80" if course["theme"] == "physics" else "#7751b5"
    deep = "#0a3b59" if course["theme"] == "physics" else "#432b69"
    soft = "#e9faf6" if course["theme"] == "physics" else "#f3edff"
    st.markdown(f"<style>:root{{--rv-accent:{accent};--rv-deep:{deep};--rv-soft:{soft}}}</style>", unsafe_allow_html=True)
    st.markdown(_BASE_CSS, unsafe_allow_html=True)
    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)
    st.markdown(_FOUNDATION_SIMPLE_CSS_V12, unsafe_allow_html=True)
    apply_ui_theme("foundation")
    st.markdown("<style>.rv-route-foundation{grid-template-columns:repeat(4,1fr)!important}@media(max-width:820px){.rv-route-foundation{grid-template-columns:1fr 1fr!important}}</style>", unsafe_allow_html=True)

    back_col, path_col = st.columns([1.1, 5.4])
    with back_col:
        if st.button("← لوحة الطالب", key=f"{prefix}_back", use_container_width=True):
            st.session_state["samed_view"] = "dashboard"
            st.switch_page("app.py")
    with path_col:
        st.markdown('<div class="rv-topline"><b>المدخل التأسيسي</b><span>مهارات الصفين 10 و11</span><span>←</span><span>1 مراجعة الوحدة</span><span>←</span><span>2 تمارين الكتاب</span><span>←</span><span>3 تدريب إضافي</span></div>', unsafe_allow_html=True)

    pct = round(100 * len(completed) / len(lessons)) if lessons else 0
    st.markdown(
        f'''<section class="rv-hero"><div class="rv-hero-copy"><span class="rv-kicker">{_esc(course['icon'])} جسر تأسيسي · من مهارات الصفين 10 و11</span><h1>{_mixed(course['title'])}</h1><p>{_mixed(course['subtitle'])}</p><p class="rv-source">{_mixed(course['source_note'])}</p></div><div class="rv-progress"><div class="rv-ring" style="background:conic-gradient(#45d7bd {pct}%,rgba(255,255,255,.15) 0)"><b>{pct}%</b></div><span>تقدم التأسيس</span><small><bdi class="rv-ltr" dir="ltr">{len(completed)}</bdi> من <bdi class="rv-ltr" dir="ltr">{len(lessons)}</bdi> محاور تأسيسية</small></div></section>''',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="rv-route rv-route-foundation"><div class="rv-route-item active"><b>0</b><span>أعد بناء الأساس<br><small>فكرة + نموذج + مشاركة</small></span></div><div class="rv-route-item"><b>1</b><span>راجع الوحدة</span></div><div class="rv-route-item"><b>2</b><span>حل تمارين الكتاب</span></div><div class="rv-route-item"><b>3</b><span>تدرّب إضافيًا</span></div></div>', unsafe_allow_html=True)

    st.markdown("""<style>.rv-video-title{font-size:17px;font-weight:900;color:#18384f;margin:6px 2px 8px;direction:rtl;text-align:right}.rv-video-link{display:inline-block;margin:6px 2px 14px;font-size:14px;font-weight:800;color:#0d8c80;text-decoration:none}.rv-video-link:hover{text-decoration:underline}</style>""", unsafe_allow_html=True)
    _render_videos(course, "🎥 فيديو تأسيسي", "شاهده قبل البدء في محاور التأسيس")

    labels = [f"{i+1}. {l['title']}" for i, l in enumerate(lessons)]
    picker_key = f"{prefix}_lesson_picker"
    if st.session_state.get(picker_key) not in labels:
        st.session_state[picker_key] = labels[0]
    selected_label = st.selectbox("اختر مهارة تأسيسية", labels, key=picker_key)
    index = labels.index(selected_label)
    lesson = lessons[index]

    nodes = []
    for i, item in enumerate(lessons):
        classes = ["rv-map-node"]
        if item["id"] in completed:
            classes.append("done")
        if i == index:
            classes.append("current")
        status = "مكتمل ✓" if item["id"] in completed else ("تدرسه الآن" if i == index else "لم يبدأ")
        nodes.append(f'<div class="{" ".join(classes)}"><b>{i+1}. {_mixed(item["title"])}</b><small>{status}</small></div>')
    st.markdown(f'<div class="rv-map-title"><h2>خريطة الأساسيات</h2><small>ابدأ من أول فجوة أو انتقل إلى المهارة التي تحتاجها</small></div><div class="rv-map">{"".join(nodes)}</div>', unsafe_allow_html=True)

    st.markdown(f'<section class="rv-lesson-head"><span class="tag">المحور التأسيسي <bdi class="rv-ltr" dir="ltr">{index+1}</bdi> من <bdi class="rv-ltr" dir="ltr">{len(lessons)}</bdi></span><h2>{_mixed(lesson["title"])}</h2><p><b>هدف الدرس:</b> {_mixed(lesson["objective"])}</p></section>', unsafe_allow_html=True)

    main, aside = st.columns([2.25, 1], gap="large")
    with main:
        st.markdown(f'<div class="rv-story"><b>🔎 ابدأ من موقف حقيقي</b><br>{_mixed(lesson["hook"])}</div>', unsafe_allow_html=True)
        if lesson.get("simple_sentence"):
            st.markdown(f'<div class="rv-simple-sentence"><b>الفكرة في جملة واحدة</b><br>{_mixed(lesson["simple_sentence"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="rv-card"><h3>نفهمها كلمة كلمة</h3>' + ''.join(f'<p class="rv-paragraph">{_mixed(p)}</p>' for p in lesson["explanation"]) + '<div class="rv-points">' + ''.join(f'<div class="rv-point">✓ {_mixed(p)}</div>' for p in lesson["key_points"]) + '</div></div>', unsafe_allow_html=True)
        st.markdown(_visual(lesson["visual"]), unsafe_allow_html=True)
        if lesson.get("direction_note"):
            st.markdown(f'<div class="rv-vector-note">{_esc(lesson["direction_note"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rv-formula"><small>العلاقة الرئيسية — معروضة كاملة</small><div class="rv-equation">{_esc(lesson["formula"])}</div><p>{_mixed(lesson.get("formula_note", ""))}</p></div>', unsafe_allow_html=True)

        ex = lesson["example"]
        givens = ''.join(f'<span>{_mixed(g)}</span>' for g in ex["givens"])
        plan = ''.join(f'<div><b>{i+1}</b>{_mixed(step)}</div>' for i, step in enumerate(ex["plan"]))
        st.markdown(f'<div class="rv-card"><div class="rv-example-head"><div><h3>مثال موجّه: {_mixed(ex["title"])}</h3><p class="rv-example-q">{_mixed(ex["question"])}</p></div><span>أنت تضع القيم داخل العلاقة</span></div><div class="rv-givens">{givens}</div><div class="rv-plan">{plan}</div><div class="rv-symbolic-copy"><small>1. العلاقة كاملة بالرموز</small><div class="rv-substitution">{_esc(lesson["formula"])}</div></div></div>', unsafe_allow_html=True)

        ex_ok_key = f"{prefix}_{lesson['id']}_example_ok"
        ex_msg_key = f"{prefix}_{lesson['id']}_example_msg"
        attempts_key = f"{prefix}_{lesson['id']}_attempts"
        with st.form(f"{prefix}_{lesson['id']}_example_form"):
            st.markdown(f'<div class="rv-inline-guide"><b>2. عوّض داخل العلاقة نفسها</b>{_mixed(ex.get("inline_help", "ضع كل عدد مكان رمزه في الفراغ."))}</div>', unsafe_allow_html=True)
            field_values: list[tuple[dict[str, Any], str]] = []
            field_by_key = {field["key"]: field for field in ex["fields"]}
            inline_parts = [part for part in re.split(r"(\[\[[A-Za-z0-9_]+\]\])", ex["inline_template"]) if part]
            inline_weights = [1.15 if part.startswith("[[") else max(0.75, min(3.2, len(part.strip()) / 4 or 0.75)) for part in inline_parts]
            inline_cols = st.columns(inline_weights)
            for i, part in enumerate(inline_parts):
                with inline_cols[i]:
                    match = re.fullmatch(r"\[\[([A-Za-z0-9_]+)\]\]", part)
                    if match:
                        field = field_by_key[match.group(1)]
                        value = st.text_input(
                            _plain_mixed(field["label"]),
                            key=f"{prefix}_{lesson['id']}_field_{field['key']}",
                            placeholder="…",
                            label_visibility="collapsed",
                        )
                        field_values.append((field, value))
                    else:
                        st.markdown(f'<div class="rv-inline-token">{_esc(part)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="rv-inline-next">3. نفّذ العملية ثم اكتب النتيجة في الفراغ الأخير</div>', unsafe_allow_html=True)
            result_value = ""
            result_parts = [part for part in re.split(r"(\[\[[A-Za-z0-9_]+\]\])", ex["result_template"]) if part]
            result_weights = [1.2 if part == "[[__result]]" else max(0.75, min(3.2, len(part.strip()) / 4 or 0.75)) for part in result_parts]
            result_cols = st.columns(result_weights)
            for i, part in enumerate(result_parts):
                with result_cols[i]:
                    if part == "[[__result]]":
                        result_value = st.text_input(
                            _plain_mixed(ex["result"]["label"]),
                            key=f"{prefix}_{lesson['id']}_result",
                            placeholder="…",
                            label_visibility="collapsed",
                        )
                    else:
                        st.markdown(f'<div class="rv-inline-token">{_esc(part)}</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("تحقق من التعويض والحساب", type="primary", use_container_width=True)
        if submitted:
            st.session_state[attempts_key] = int(st.session_state.get(attempts_key, 0)) + 1
            wrong_fields = [_plain_mixed(field["label"]) for field, value in field_values if not _near(_parse_number(value), float(field["answer"]))]
            result_ok = _near(_parse_number(result_value), float(ex["result"]["answer"]), float(ex["result"].get("tol", 0)) or None)
            if not wrong_fields and result_ok:
                st.session_state[ex_ok_key] = True
                st.session_state[ex_msg_key] = "صحيح: وضعت القيم في أماكن رموزها داخل العلاقة، ثم حسبت الناتج."
            else:
                st.session_state[ex_ok_key] = False
                if wrong_fields:
                    st.session_state[ex_msg_key] = "راجع موضع: " + "، ".join(wrong_fields) + ". اقرأ المعطيات ثم طابق كل قيمة مع رمزها."
                else:
                    st.session_state[ex_msg_key] = "التعويض صحيح، لكن الناتج العددي يحتاج مراجعة. نفّذ العملية مرة أخرى."
        if ex_msg_key in st.session_state:
            if st.session_state.get(ex_ok_key):
                st.success(st.session_state[ex_msg_key])
            else:
                st.warning(st.session_state[ex_msg_key])
        if st.session_state.get(ex_ok_key):
            lines = ''.join(f'<div class="rv-solution-line">{_mixed(line)}</div>' for line in ex["solution"])
            st.markdown(f'<div class="rv-solution"><b>الحل المكتمل بعد مشاركتك</b>{lines}<div class="rv-interpret">{_mixed(ex["interpretation"])}</div></div>', unsafe_allow_html=True)
        elif st.session_state.get(attempts_key, 0) >= 2:
            st.info("تلميح: العلاقة مكتوبة كاملة. ارجع إلى بطاقات المعطيات وطابق اسم كل قيمة مع الرمز نفسه قبل الحساب.")

        cp = lesson["checkpoint"]
        cp_ok_key = f"{prefix}_{lesson['id']}_checkpoint_ok"
        cp_msg_key = f"{prefix}_{lesson['id']}_checkpoint_msg"
        cp_options = ["— اختر تفسيرك —"] + list(cp["options"])
        with st.form(f"{prefix}_{lesson['id']}_checkpoint_form"):
            st.markdown("#### توقّف وفكّر")
            st.write(_plain_mixed(cp["question"]))
            choice = st.selectbox("اختر الإجابة الأقرب لفهمك", cp_options, key=f"{prefix}_{lesson['id']}_choice", format_func=_plain_mixed)
            cp_submit = st.form_submit_button("ثبّت الفهم", use_container_width=True)
        if cp_submit:
            if choice == "— اختر تفسيرك —":
                st.session_state[cp_ok_key] = False
                st.session_state[cp_msg_key] = "اختر إجابة أولًا."
            elif choice == cp["options"][cp["answer"]]:
                st.session_state[cp_ok_key] = True
                st.session_state[cp_msg_key] = _plain_mixed(cp["explain"])
            else:
                st.session_state[cp_ok_key] = False
                st.session_state[cp_msg_key] = "ليست الأدق بعد. ارجع إلى الفكرة الرئيسية واقرأ السؤال مرة ثانية."
        if cp_msg_key in st.session_state:
            if st.session_state.get(cp_ok_key):
                st.success("فهم صحيح — " + st.session_state[cp_msg_key])
            else:
                st.warning(st.session_state[cp_msg_key])

        newly_completed = False
        if st.session_state.get(ex_ok_key) and st.session_state.get(cp_ok_key) and lesson["id"] not in completed:
            completed.add(lesson["id"])
            st.session_state[f"{prefix}_total_xp"] += 20
            newly_completed = True
        if lesson["id"] in completed:
            st.markdown('<div class="rv-complete">✓ اكتمل هذا المحور التأسيسي: فهمت الفكرة، ونفذت التطبيق، وثبّت التفسير.</div>', unsafe_allow_html=True)
        if newly_completed:
            st.rerun()

    with aside:
        with st.expander("أحتاج تمهيدًا أبسط", expanded=False):
            st.write(_plain_mixed(lesson["prerequisite"]))
        st.markdown('<div class="rv-card"><h3>قاموس الرموز</h3><div class="rv-symbols">' + ''.join(f'<div class="rv-symbol"><code>{_esc(s["symbol"])}</code><span>{_mixed(s["meaning"])}<small>{_esc(s.get("unit", ""))}</small></span></div>' for s in lesson["symbols"]) + '</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rv-memory"><b>🧠 بطاقة ذاكرة</b><br>{_mixed(lesson["memory"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rv-mistake"><b>⚠️ خطأ شائع</b><br>{_mixed(lesson["mistake"])}</div>', unsafe_allow_html=True)
        st.button(
            "إعادة هذا الدرس",
            key=f"{prefix}_{lesson['id']}_reset_button",
            on_click=_reset_lesson,
            args=(prefix, lesson["id"], completed_key),
            use_container_width=True,
        )

    def move_to(target: int) -> None:
        st.session_state[picker_key] = labels[target]

    prev_col, next_col = st.columns(2)
    with prev_col:
        st.button("→ المحور السابق", disabled=index == 0, on_click=move_to, args=(max(0, index - 1),), key=f"{prefix}_prev", use_container_width=True)
    with next_col:
        st.button("المحور التالي ←", disabled=index == len(lessons) - 1, on_click=move_to, args=(min(len(lessons) - 1, index + 1),), key=f"{prefix}_next", use_container_width=True)

    if len(completed) == len(lessons):
        st.success("أكملت الجسر التأسيسي. أصبحت جاهزًا للمرحلة التالية: مراجعة مفاهيم الوحدة الحالية.", icon="🎉")
        if st.button("الانتقال إلى المرحلة 1: مراجعة الوحدة", type="primary", use_container_width=True, key=f"{prefix}_to_review"):
            st.switch_page(course["next_page"])
