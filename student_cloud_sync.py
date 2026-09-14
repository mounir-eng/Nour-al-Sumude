"""Google Sheets sync for students and contact messages."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import streamlit as st

HEADERS = [
    "id",
    "name",
    "grade",
    "subjects",
    "xp",
    "progress",
    "badges",
    "found",
    "review",
    "book",
    "extra",
    "last_seen",
    "teacher_id",
    "password_hash",
]
MESSAGE_HEADERS = [
    "id",
    "created_at",
    "name",
    "email",
    "institution",
    "subject",
    "message",
    "status",
]

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def is_configured() -> bool:
    try:
        gsheets = st.secrets.get("gsheets", {})
        sa = st.secrets.get("gcp_service_account", {})
        return bool(gsheets.get("spreadsheet") and sa.get("client_email") and sa.get("private_key"))
    except Exception:
        return False


def _client():
    import gspread
    from google.oauth2.service_account import Credentials

    sa = dict(st.secrets["gcp_service_account"])
    key = str(sa.get("private_key") or "")
    sa["private_key"] = key.replace(chr(92) + "n", "\n")
    creds = Credentials.from_service_account_info(sa, scopes=_SCOPES)
    return gspread.authorize(creds)


def open_worksheet(kind: str = "students"):
    if not is_configured():
        return None
    gsheets = st.secrets["gsheets"]
    spreadsheet = str(gsheets.get("spreadsheet") or "").strip()
    if kind == "messages":
        title = str(gsheets.get("messages_worksheet") or "messages").strip() or "messages"
        headers = MESSAGE_HEADERS
    else:
        title = str(gsheets.get("worksheet") or "students").strip() or "students"
        headers = HEADERS
    gc = _client()
    sh = gc.open(spreadsheet) if not spreadsheet.startswith("http") else gc.open_by_url(spreadsheet)
    try:
        ws = sh.worksheet(title)
    except Exception:
        ws = sh.add_worksheet(title=title, rows=2000, cols=max(16, len(headers)))
        ws.update("A1", [headers])
        return ws
    values = ws.get_all_values()
    if not values:
        ws.update("A1", [headers])
    elif [c.strip() for c in values[0]] != headers:
        # Keep existing sheet; callers map by header name when possible.
        pass
    return ws


def _row_dict(headers: list[str], row: list[str]) -> dict[str, str]:
    out = {}
    for i, key in enumerate(headers):
        out[key] = row[i].strip() if i < len(row) else ""
    return out


def list_students(*, include_secrets: bool = False) -> list[dict[str, Any]]:
    ws = open_worksheet("students")
    if ws is None:
        return []
    rows = ws.get_all_values()
    if not rows:
        return []
    headers = [c.strip() or HEADERS[i] if i < len(HEADERS) else c.strip() for i, c in enumerate(rows[0])]
    out = []
    for row in rows[1:]:
        if not any(cell.strip() for cell in row):
            continue
        item = _row_dict(headers if headers else HEADERS, row)
        if not include_secrets:
            item.pop("password_hash", None)
        out.append(item)
    return out


def find_student_by_name(name: str) -> dict[str, Any] | None:
    needle = (name or "").strip().casefold()
    if not needle:
        return None
    for row in list_students(include_secrets=True):
        if str(row.get("name") or "").strip().casefold() == needle:
            return row
    return None


def upsert_student(profile: dict[str, Any], stats: dict[str, Any] | None = None) -> dict[str, Any]:
    ws = open_worksheet("students")
    if ws is None:
        return {"ok": False, "error": "sheets_not_configured"}
    stats = stats or {}
    sid = str(profile.get("id") or "").strip()
    name = str(profile.get("name") or "").strip()
    grades = profile.get("grades") or [profile.get("grade")]
    grade_s = ",".join(str(int(g)) for g in grades if str(g).strip())
    subjects = profile.get("subjects") or []
    if isinstance(subjects, list):
        subjects_s = ",".join(str(s) for s in subjects)
    else:
        subjects_s = str(subjects)
    values = {
        "id": sid,
        "name": name,
        "grade": grade_s,
        "subjects": subjects_s,
        "xp": str(stats.get("xp", profile.get("xp", 0) or 0)),
        "progress": str(stats.get("progress", profile.get("progress", 0) or 0)),
        "badges": str(stats.get("badges", profile.get("badges", "") or "")),
        "found": str(stats.get("found", 0) or 0),
        "review": str(stats.get("review", 0) or 0),
        "book": str(stats.get("book", 0) or 0),
        "extra": str(stats.get("extra", 0) or 0),
        "last_seen": _now(),
        "teacher_id": str(profile.get("teacher_id") or ""),
        "password_hash": str(profile.get("passwordHash") or profile.get("password_hash") or ""),
    }
    rows = ws.get_all_values()
    headers = HEADERS
    if rows:
        headers = [c.strip() or HEADERS[i] if i < len(HEADERS) else c.strip() for i, c in enumerate(rows[0])]
        if not any(headers):
            headers = HEADERS
    payload = [values.get(h, "") for h in headers]
    match_row = None
    for i, row in enumerate(rows[1:], start=2):
        rid = row[0].strip() if row else ""
        rname = row[1].strip() if len(row) > 1 else ""
        if (sid and rid == sid) or (name and rname.casefold() == name.casefold()):
            match_row = i
            break
    if match_row:
        ws.update(f"A{match_row}", [payload])
    else:
        ws.append_row(payload, value_input_option="USER_ENTERED")
    return {"ok": True}


def save_contact_message(
    *,
    name: str,
    email: str,
    institution: str,
    subject: str,
    message: str,
    msg_id: str,
) -> dict[str, Any]:
    ws = open_worksheet("messages")
    if ws is None:
        return {"ok": False, "error": "sheets_not_configured"}
    ws.append_row(
        [msg_id, _now(), name, email, institution, subject, message, "new"],
        value_input_option="USER_ENTERED",
    )
    return {"ok": True}


def list_contact_messages() -> list[dict[str, str]]:
    ws = open_worksheet("messages")
    if ws is None:
        return []
    rows = ws.get_all_values()
    if not rows:
        return []
    headers = [c.strip() or MESSAGE_HEADERS[i] if i < len(MESSAGE_HEADERS) else c.strip() for i, c in enumerate(rows[0])]
    out = []
    for row in rows[1:]:
        if not any(cell.strip() for cell in row):
            continue
        item = _row_dict(headers if headers else MESSAGE_HEADERS, row)
        item["status"] = (item.get("status") or "new").strip() or "new"
        out.append(item)
    out.reverse()
    return out


def _find_message_row(ws, msg_id: str) -> int | None:
    rows = ws.get_all_values()
    for i, row in enumerate(rows[1:], start=2):
        if row and row[0].strip() == msg_id:
            return i
    return None


def update_message_status(msg_id: str, status: str) -> bool:
    ws = open_worksheet("messages")
    if ws is None:
        return False
    idx = _find_message_row(ws, msg_id)
    if not idx:
        return False
    headers = [c.strip() for c in (ws.row_values(1) or MESSAGE_HEADERS)]
    col = headers.index("status") + 1 if "status" in headers else len(MESSAGE_HEADERS)
    ws.update_cell(idx, col, status)
    return True


def delete_message(msg_id: str) -> bool:
    ws = open_worksheet("messages")
    if ws is None:
        return False
    idx = _find_message_row(ws, msg_id)
    if not idx:
        return False
    ws.delete_rows(idx)
    return True
