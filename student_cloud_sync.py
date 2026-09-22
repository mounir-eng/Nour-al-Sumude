"""Google Sheets sync for students, messages, and student feedback."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

HEADERS = ["id","name","grade","subjects","xp","progress","badges","found","review","book","extra","last_seen","teacher_id","password_hash"]
MESSAGE_HEADERS = ["id","created_at","name","email","institution","subject","message","status"]
FEEDBACK_HEADERS = ["id","created_at","student_id","student_name","grade","subject","feedback_type","stage_id","stage_title","rating","difficulty","stars","confidence","likes","issues","improvements","lesson","note","status"]
_LAST_ERROR = ""
_LAST_UPSERT = ""


def _secrets():
    try:
        import streamlit as st
        return st.secrets
    except Exception:
        return {}


def sheets_configured() -> bool:
    try:
        g, sa = _secrets().get("gsheets", {}), _secrets().get("gcp_service_account", {})
        return bool((g.get("spreadsheet") or g.get("spreadsheet_id") or g.get("url")) and sa.get("client_email") and sa.get("private_key"))
    except Exception:
        return False


def last_sheets_error() -> str: return _LAST_ERROR
def last_upsert_name() -> str: return _LAST_UPSERT


def _set_error(message=""):
    global _LAST_ERROR
    _LAST_ERROR = str(message or "")


def _friendly(exc: Exception) -> str:
    email = str(_secrets().get("gcp_service_account", {}).get("client_email") or "").strip()
    suffix = (" شارك الجدول مع " + email + " بصلاحية محرر.") if email else ""
    name, text = type(exc).__name__, str(exc).lower()
    if "SpreadsheetNotFound" in name or "not found" in text:
        return "الحساب الخدمي لا يرى جدول Google Sheets." + suffix
    if "403" in str(exc) or "permission" in text:
        return "لا توجد صلاحية للوصول إلى الجدول. فعّل Sheets API وDrive API." + suffix
    return "تعذر الاتصال بـ Google Sheets. تحقق من Secrets ومشاركة الجدول."


def _clean_ref(raw: Any) -> str:
    text = str(raw or "").strip().strip('"').strip("'")
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip()


def spreadsheet_key() -> str:
    g = _secrets().get("gsheets", {})
    raw = _clean_ref(g.get("spreadsheet") or g.get("spreadsheet_id") or g.get("url") or "")
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", raw)
    return match.group(1) if match else raw


def _client():
    import gspread
    from google.oauth2.service_account import Credentials
    info = dict(_secrets().get("gcp_service_account", {}))
    info["private_key"] = str(info.get("private_key") or "").replace("\\n", "\n")
    creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
    return gspread.authorize(creds)


def _open_sheet():
    gc, ref = _client(), spreadsheet_key()
    if not ref: raise ValueError("empty spreadsheet")
    if re.fullmatch(r"[a-zA-Z0-9-_]{30,}", ref): return gc.open_by_key(ref)
    if ref.startswith("http://") or ref.startswith("https://"): return gc.open_by_url(ref)
    return gc.open(ref)


def _config(kind: str):
    g = _secrets().get("gsheets", {})
    if kind == "messages": return str(g.get("messages_worksheet") or "messages"), MESSAGE_HEADERS
    if kind == "feedback": return str(g.get("feedback_worksheet") or "feedback"), FEEDBACK_HEADERS
    return str(g.get("worksheet") or "students"), HEADERS


def _open_ws(kind="students"):
    name, headers = _config(kind)
    sh = _open_sheet()
    try: ws = sh.worksheet(name)
    except Exception: ws = sh.add_worksheet(title=name, rows=2000, cols=max(20, len(headers)))
    values = ws.get_all_values()
    if not values: ws.append_row(headers)
    elif [str(x).strip() for x in values[0]] != headers: ws.update("A1", [headers])
    return ws


def _records(kind):
    _, headers = _config(kind)
    return _open_ws(kind).get_all_records(expected_headers=headers)


def list_students() -> list[dict[str, Any]]:
    if not sheets_configured(): return []
    try:
        rows = _records("students"); _set_error(); return [dict(r) for r in rows if r.get("id") or r.get("name")]
    except Exception as exc:
        _set_error(_friendly(exc)); return []


def find_student_by_name(name: str):
    target = str(name or "").strip()
    return next((r for r in list_students() if str(r.get("name") or "").strip() == target), None)


def upsert_student(profile: dict[str, Any]) -> dict[str, Any]:
    global _LAST_UPSERT
    if not sheets_configured():
        _set_error("لم يُضبط Google Sheets في Secrets."); return dict(profile)
    try:
        ws, records = _open_ws("students"), _records("students")
        sid, name = str(profile.get("id") or "").strip(), str(profile.get("name") or "").strip()
        grades = profile.get("grades") or [profile.get("grade", "")]
        grade = ",".join(str(x).strip() for x in grades if str(x).strip())
        subjects = profile.get("subjects") or []
        if isinstance(subjects, list): subjects = "، ".join({"phys":"فيزياء","chem":"كيمياء","physics":"فيزياء","chemistry":"كيمياء"}.get(str(x),str(x)) for x in subjects)
        payload = {
            "id": sid or "stu-" + datetime.now(timezone.utc).strftime("%y%m%d%H%M%S"), "name": name,
            "grade": grade, "subjects": str(subjects), "xp": profile.get("xp",0) or 0,
            "progress": profile.get("progress",0) or 0, "badges": profile.get("badges","") or "",
            "found": profile.get("found","") or "", "review": profile.get("review","") or "",
            "book": profile.get("book","") or "", "extra": profile.get("extra","") or "",
            "last_seen": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
            "teacher_id": profile.get("teacher_id","") or "",
            "password_hash": profile.get("passwordHash") or profile.get("password_hash") or "",
        }
        row_i = None
        for i, row in enumerate(records, start=2):
            if (sid and str(row.get("id") or "").strip()==sid) or (not sid and str(row.get("name") or "").strip()==name):
                row_i=i; payload["id"]=str(row.get("id") or payload["id"]); break
        vals=[payload[h] for h in HEADERS]
        if row_i: ws.update("A"+str(row_i)+":N"+str(row_i), [vals])
        else: ws.append_row(vals)
        _LAST_UPSERT=name; _set_error(); return payload
    except Exception as exc:
        _set_error(_friendly(exc)); return dict(profile)


def _list_simple(kind: str, status: str | None = None):
    if not sheets_configured(): return []
    try:
        rows=[dict(r) for r in _records(kind)]
        if status is not None: rows=[r for r in rows if str(r.get("status") or "").strip()==status]
        _set_error(); return rows
    except Exception as exc:
        _set_error(_friendly(exc)); return []


def list_messages(status=None): return _list_simple("messages", status)
def list_feedback(status=None): return _list_simple("feedback", status)


def _append(kind: str, payload: dict[str, Any]):
    _, headers = _config(kind)
    _open_ws(kind).append_row([payload.get(h, "") for h in headers])


def save_contact_message(data: dict[str, Any]):
    payload={"id":data.get("id") or "msg-"+datetime.now(timezone.utc).strftime("%y%m%d%H%M%S%f"),"created_at":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),"name":str(data.get("name") or "").strip(),"email":str(data.get("email") or "").strip(),"institution":str(data.get("institution") or "").strip(),"subject":str(data.get("subject") or "").strip(),"message":str(data.get("message") or "").strip(),"status":"new"}
    try: _append("messages",payload); _set_error()
    except Exception as exc: _set_error(_friendly(exc))
    return payload


def save_feedback(data: dict[str, Any]):
    now=datetime.now(timezone.utc)
    payload={h:"" for h in FEEDBACK_HEADERS}
    payload.update({"id":"fb-"+now.strftime("%y%m%d%H%M%S%f"),"created_at":now.strftime("%Y-%m-%d %H:%M:%S"),"status":"new"})
    for h in FEEDBACK_HEADERS:
        if h in data:
            value=data[h]
            payload[h]="، ".join(str(x) for x in value) if isinstance(value,list) else str(value or "")
    try: _append("feedback",payload); _set_error()
    except Exception as exc: _set_error(_friendly(exc))
    return payload


def _update_status(kind: str, item_id: str, status: str):
    _, headers=_config(kind); ws=_open_ws(kind)
    for i,row in enumerate(_records(kind),start=2):
        if str(row.get("id") or "").strip()==str(item_id): ws.update_cell(i,headers.index("status")+1,status); return


def _delete(kind: str, item_id: str):
    ws=_open_ws(kind)
    for i,row in enumerate(_records(kind),start=2):
        if str(row.get("id") or "").strip()==str(item_id): ws.delete_rows(i); return


def update_message_status(item_id,status):
    try: _update_status("messages",item_id,status)
    except Exception as exc: _set_error(_friendly(exc))
def delete_message(item_id):
    try: _delete("messages",item_id)
    except Exception as exc: _set_error(_friendly(exc))
def update_feedback_status(item_id,status):
    try: _update_status("feedback",item_id,status)
    except Exception as exc: _set_error(_friendly(exc))
def delete_feedback(item_id):
    try: _delete("feedback",item_id)
    except Exception as exc: _set_error(_friendly(exc))
