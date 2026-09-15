"""Google Sheets sync for students and contact messages."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

_LAST_ERROR = ""
_CREATED_URL = ""
_LAST_UPSERT = ""

HEADERS = [
    "id", "name", "grade", "subjects", "xp", "progress", "badges",
    "found", "review", "book", "extra", "last_seen", "teacher_id", "password_hash",
]
MESSAGE_HEADERS = [
    "id", "created_at", "name", "email", "institution", "subject", "message", "status",
]


def _secrets():
    try:
        import streamlit as st
        return st.secrets
    except Exception:
        return {}


def sheets_configured() -> bool:
    try:
        g = _secrets().get("gsheets", {})
        gcp = _secrets().get("gcp_service_account", {})
        return bool(
            (g.get("spreadsheet") or g.get("spreadsheet_id") or g.get("url"))
            and gcp.get("client_email")
            and gcp.get("private_key")
        )
    except Exception:
        return False


def last_sheets_error() -> str:
    return _LAST_ERROR


def last_upsert_name() -> str:
    return _LAST_UPSERT


def last_created_url() -> str:
    return _CREATED_URL


def _service_email() -> str:
    try:
        return str(_secrets().get("gcp_service_account", {}).get("client_email") or "").strip()
    except Exception:
        return ""


def _clean_ref(raw: str) -> str:
    text = str(raw or "").strip().strip('"').strip("'")
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip()


def spreadsheet_key() -> str:
    g = _secrets().get("gsheets", {})
    raw = _clean_ref(g.get("spreadsheet") or g.get("spreadsheet_id") or g.get("url") or "")
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", raw)
    if match:
        return match.group(1)
    if re.fullmatch(r"[a-zA-Z0-9-_]{30,}", raw):
        return raw
    return raw


def _friendly_error(exc: Exception) -> str:
    email = _service_email()
    share = f" شارك الجدول مع {email} بصلاحية محرر." if email else " شارك الجدول مع إيميل الحساب الخدمي بصلاحية محرر."
    name = type(exc).__name__
    text = str(exc).lower()
    if "SpreadsheetNotFound" in name or "not found" in text:
        return "الحساب الخدمي لا يرى هذا الجدول. افتح الجدول → مشاركة → أضف الإيميل كمحرر." + share
    if "APIError" in name or "403" in str(exc) or "permission" in text:
        return "لا توجد صلاحية لفتح الجدول. فعّل Google Sheets API و Google Drive API." + share
    return "تعذر الاتصال بـ Google Sheets. تحقق من Secrets ومشاركة الجدول."


def _set_error(exc: Exception | None = None, message: str = "") -> None:
    global _LAST_ERROR
    _LAST_ERROR = message or (_friendly_error(exc) if exc else "")


def _sa_info() -> dict[str, Any]:
    gcp = dict(_secrets().get("gcp_service_account", {}))
    key = str(gcp.get("private_key") or "")
    gcp["private_key"] = key.replace("\\n", "\n")
    return gcp


def _client():
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(_sa_info(), scopes=scopes)
    return gspread.authorize(creds)


def _open_spreadsheet(gc):
    raw = spreadsheet_key()
    if not raw:
        raise ValueError("empty spreadsheet")
    if re.fullmatch(r"[a-zA-Z0-9-_]{30,}", raw):
        return gc.open_by_key(raw)
    if raw.startswith("http://") or raw.startswith("https://"):
        return gc.open_by_url(raw)
    return gc.open(raw)


def _ensure_headers(ws, headers: list[str]) -> None:
    values = ws.get_all_values()
    if not values:
        ws.append_row(headers)
        return
    current = [str(c).strip() for c in values[0]]
    if current != headers:
        ws.update("A1", [headers])


def _open_ws(kind: str = "students"):
    g = _secrets().get("gsheets", {})
    if kind == "messages":
        ws_name = str(g.get("messages_worksheet") or "messages").strip() or "messages"
        headers = MESSAGE_HEADERS
    else:
        ws_name = str(g.get("worksheet") or "students").strip() or "students"
        headers = HEADERS
    sh = _open_spreadsheet(_client())
    try:
        ws = sh.worksheet(ws_name)
    except Exception:
        ws = sh.add_worksheet(title=ws_name, rows=2000, cols=max(16, len(headers)))
    _ensure_headers(ws, headers)
    return ws


def create_managed_spreadsheet(share_with: str = "") -> dict[str, str]:
    global _CREATED_URL, _LAST_ERROR
    gc = _client()
    sh = gc.create("nour-al-sumude-students")
    email = _service_email()
    if email:
        try:
            sh.share(email, perm_type="user", role="writer")
        except Exception:
            pass
    share_with = str(share_with or "").strip()
    if share_with and "@" in share_with:
        try:
            sh.share(share_with, perm_type="user", role="writer")
        except Exception:
            pass
    students = sh.sheet1
    students.update_title("students")
    _ensure_headers(students, HEADERS)
    try:
        messages = sh.add_worksheet(title="messages", rows=2000, cols=len(MESSAGE_HEADERS))
    except Exception:
        messages = students
    _ensure_headers(messages, MESSAGE_HEADERS)
    url = "https://docs.google.com/spreadsheets/d/" + str(sh.id) + "/edit"
    _CREATED_URL = url
    _LAST_ERROR = ""
    return {"id": sh.id, "url": url}


def _row_to_student(row: dict[str, Any]) -> dict[str, Any]:
    grade_raw = str(row.get("grade") or "").strip()
    grades = [g.strip() for g in grade_raw.replace(";", ",").split(",") if g.strip()]
    return {
        "id": str(row.get("id") or "").strip(),
        "name": str(row.get("name") or "").strip(),
        "grade": grade_raw,
        "grades": grades,
        "subjects": str(row.get("subjects") or "").strip(),
        "xp": str(row.get("xp") or "0").strip() or "0",
        "progress": str(row.get("progress") or "0").strip() or "0",
        "badges": str(row.get("badges") or "").strip(),
        "found": str(row.get("found") or "").strip(),
        "review": str(row.get("review") or "").strip(),
        "book": str(row.get("book") or "").strip(),
        "extra": str(row.get("extra") or "").strip(),
        "last_seen": str(row.get("last_seen") or "").strip(),
        "teacher_id": str(row.get("teacher_id") or "").strip(),
        "password_hash": str(row.get("password_hash") or "").strip(),
    }


def list_students() -> list[dict[str, Any]]:
    _set_error(message="")
    if not sheets_configured():
        return []
    try:
        rows = _open_ws("students").get_all_records(expected_headers=HEADERS)
        out = []
        for row in rows:
            item = _row_to_student(row)
            if item["id"] or item["name"]:
                out.append(item)
        return out
    except Exception as exc:
        _set_error(exc)
        return []


def find_student_by_name(name: str) -> dict[str, Any] | None:
    target = str(name or "").strip()
    if not target:
        return None
    for row in list_students():
        if str(row.get("name") or "").strip() == target:
            return row
    return None


def upsert_student(profile: dict[str, Any]) -> dict[str, Any]:
    global _LAST_UPSERT
    if not sheets_configured():
        _set_error(message="لم يُضبط Google Sheets في Secrets.")
        return dict(profile)
    try:
        saved = _upsert_student(profile)
        _LAST_UPSERT = str(saved.get("name") or "")
        _set_error(message="")
        return saved
    except Exception as exc:
        _set_error(exc)
        return dict(profile)


def _upsert_student(profile: dict[str, Any]) -> dict[str, Any]:
    ws = _open_ws("students")
    records = ws.get_all_records(expected_headers=HEADERS)
    sid = str(profile.get("id") or "").strip()
    name = str(profile.get("name") or "").strip()
    grades = profile.get("grades") or [profile.get("grade", "")]
    grade_txt = ",".join(str(g).strip() for g in grades if str(g).strip())
    subjects = profile.get("subjects") or []
    if isinstance(subjects, list):
        mapped = []
        for s in subjects:
            mapped.append({"phys": "فيزياء", "chem": "كيمياء", "physics": "فيزياء", "chemistry": "كيمياء"}.get(str(s), str(s)))
        subjects_txt = "، ".join(mapped)
    else:
        subjects_txt = str(subjects)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    payload = {
        "id": sid or ("stu-" + datetime.now(timezone.utc).strftime("%y%m%d%H%M%S")),
        "name": name,
        "grade": grade_txt,
        "subjects": subjects_txt,
        "xp": str(profile.get("xp", 0) or 0),
        "progress": str(profile.get("progress", 0) or 0),
        "badges": str(profile.get("badges") or ""),
        "found": str(profile.get("found") or ""),
        "review": str(profile.get("review") or ""),
        "book": str(profile.get("book") or ""),
        "extra": str(profile.get("extra") or ""),
        "last_seen": now,
        "teacher_id": str(profile.get("teacher_id") or ""),
        "password_hash": str(profile.get("passwordHash") or profile.get("password_hash") or ""),
    }
    row_i = None
    for i, rec in enumerate(records, start=2):
        rid = str(rec.get("id") or "").strip()
        rname = str(rec.get("name") or "").strip()
        if (sid and rid == sid) or (not sid and rname == name):
            row_i = i
            if rid:
                payload["id"] = rid
            if not payload["xp"] or payload["xp"] == "0":
                payload["xp"] = str(rec.get("xp") or 0)
            if not payload["progress"] or payload["progress"] == "0":
                payload["progress"] = str(rec.get("progress") or 0)
            if not payload["badges"]:
                payload["badges"] = str(rec.get("badges") or "")
            break
    values = [payload[h] for h in HEADERS]
    if row_i:
        ws.update("A" + str(row_i) + ":N" + str(row_i), [values])
    else:
        ws.append_row(values)
    return payload


def list_messages(status: str | None = None) -> list[dict[str, Any]]:
    if not sheets_configured():
        return []
    try:
        rows = _open_ws("messages").get_all_records(expected_headers=MESSAGE_HEADERS)
        out = []
        for row in rows:
            item = {h: str(row.get(h) or "").strip() for h in MESSAGE_HEADERS}
            if not item["id"] and not item["message"]:
                continue
            if status and item.get("status") != status:
                continue
            out.append(item)
        return out
    except Exception as exc:
        _set_error(exc)
        return []


def save_contact_message(data: dict[str, Any]) -> dict[str, Any]:
    if not sheets_configured():
        return dict(data)
    try:
        ws = _open_ws("messages")
        payload = {
            "id": str(data.get("id") or ("msg-" + datetime.now(timezone.utc).strftime("%y%m%d%H%M%S"))),
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "name": str(data.get("name") or "").strip(),
            "email": str(data.get("email") or "").strip(),
            "institution": str(data.get("institution") or "").strip(),
            "subject": str(data.get("subject") or "").strip(),
            "message": str(data.get("message") or "").strip(),
            "status": "new",
        }
        ws.append_row([payload[h] for h in MESSAGE_HEADERS])
        return payload
    except Exception as exc:
        _set_error(exc)
        return dict(data)


def update_message_status(msg_id: str, status: str) -> None:
    if not sheets_configured() or not msg_id:
        return
    try:
        ws = _open_ws("messages")
        rows = ws.get_all_records(expected_headers=MESSAGE_HEADERS)
        for i, rec in enumerate(rows, start=2):
            if str(rec.get("id") or "").strip() == str(msg_id):
                ws.update_cell(i, MESSAGE_HEADERS.index("status") + 1, status)
                return
    except Exception as exc:
        _set_error(exc)


def delete_message(msg_id: str) -> None:
    if not sheets_configured() or not msg_id:
        return
    try:
        ws = _open_ws("messages")
        rows = ws.get_all_records(expected_headers=MESSAGE_HEADERS)
        for i, rec in enumerate(rows, start=2):
            if str(rec.get("id") or "").strip() == str(msg_id):
                ws.delete_rows(i)
                return
    except Exception as exc:
        _set_error(exc)
