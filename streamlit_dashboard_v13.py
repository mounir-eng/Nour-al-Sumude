"""Isolated, production-safe Streamlit dashboard for the student platform."""
from __future__ import annotations

import base64
import html
from collections.abc import Callable
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

DASHBOARD_UI_VERSION = "streamlit-dashboard-v18.1-pwa-download"

_COMPONENT = components.declare_component(
    "student_samed_dashboard_v18_1",
    path=str(Path(__file__).with_name("dashboard_component")),
)

_PARENT_CSS = r"""
<style id="streamlit-dashboard-v18-1-parent">
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f8fafc!important;direction:rtl!important}
section[data-testid="stMain"]{width:100%!important;max-width:100%!important}
section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{
  width:100%!important;max-width:1240px!important;margin:0 auto!important;
  padding:0 14px 28px!important;direction:rtl!important
}
[data-testid="stCustomComponentV1"]{width:100%!important;border:0!important;background:#f8fafc!important}
[data-testid="stCustomComponentV1"] iframe{display:block!important;width:100%!important;border:0!important;background:#f8fafc!important}
[data-testid="stElementContainer"]:has([data-testid="stCustomComponentV1"]){margin:0!important;width:100%!important}
@media(max-width:700px){section[data-testid="stMain"] .block-container,[data-testid="stMainBlockContainer"]{padding:0!important}}
</style>
"""


def _pct(value: int | float) -> int:
    return max(0, min(100, int(round(value))))


def _zip_b64(unit_bytes: Callable[[str], bytes], filename: str) -> str:
    try:
        data = unit_bytes(filename) or b""
    except Exception:
        data = b""
    return base64.b64encode(data).decode("ascii") if data else ""


def render_dashboard_v13(
    *,
    profile: dict[str, Any],
    safe_name: str,
    grade_label: str,
    overall_pct: int,
    done: int,
    selected_total: int,
    xp: int,
    allowed: list[str],
    physics_live: bool,
    chemistry_live: bool,
    stage_progress: dict[str, list[int]],
    unit_progress: dict[str, int],
    unit_bytes: Callable[[str], bytes],
) -> str | None:
    """Render the dashboard in an isolated local component and return an action."""
    st.markdown(_PARENT_CSS, unsafe_allow_html=True)

    raw_name = str(profile.get("name") or html.unescape(safe_name) or "الطالب")[:80]
    payload = {
        "name": raw_name,
        "grade": int(profile.get("grade", 12)),
        "grade_label": str(grade_label),
        "overall_pct": _pct(overall_pct),
        "done": max(0, int(done)),
        "selected_total": max(0, int(selected_total)),
        "xp": max(0, int(xp)),
        "allowed": [value for value in allowed if value in {"phys", "chem"}],
        "physics_live": bool(physics_live),
        "chemistry_live": bool(chemistry_live),
        "stage_progress": {
            "phys": [_pct(value) for value in stage_progress.get("phys", [0, 0, 0, 0])[:4]],
            "chem": [_pct(value) for value in stage_progress.get("chem", [0, 0, 0, 0])[:4]],
        },
        "unit_progress": {
            "phys": _pct(unit_progress.get("phys", 0)),
            "chem": _pct(unit_progress.get("chem", 0)),
        },
    }

    event = _COMPONENT(
        data=payload,
        physics_zip=_zip_b64(unit_bytes, "physics12_unit1_complete_offline.zip") if physics_live else "",
        chemistry_zip=_zip_b64(unit_bytes, "chemistry12_unit1_complete_offline.zip") if chemistry_live else "",
        pwa_zip=_zip_b64(unit_bytes, "student_samed_pwa_offline.zip"),
        default=None,
        key="student_samed_dashboard_v18_1",
    )
    if not isinstance(event, dict):
        return None
    token = str(event.get("token", ""))
    action = str(event.get("action", ""))
    if not token or not action:
        return None
    if st.session_state.get("_dashboard_v18_1_event_token") == token:
        return None
    st.session_state["_dashboard_v18_1_event_token"] = token
    return action
