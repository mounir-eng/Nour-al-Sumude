"""مزامنة تسجيل الطلبة وتقدمهم إلى Google Sheets — دون حفظ كلمات المرور في اللوحات."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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

PHYS_KEYS = {
    "found": "physics12-foundation-momentum",
    "review": "physics12-review-momentum",
    "book": "physics12-textbook-momentum",
    "extra": "physics12-momentum",
}
CHEM_KEYS = {
    "found": "chemistry12-foundation-atom",
    "review": "chemistry12-review-unit1",
    "book": "chemistry12-textbook-unit1",
    "extra": "chemistry12-atomic-structure",
}


def is_configured() -> bool:
    try:
        import streamlit as st

        gsheets = st.secrets.get("gsheets", {})
        return bool(gsheets.get("spreadsheet")) and "gcp_service_account" in st.secrets
    except Exception:
        return False


def normalize_subjects(subjects: Any) -> list[str]:
    if isinstance(subjects, str):
        subjects = subjects.replace("،", ",").split(",")
    out: list[str] = []
    for item in subjects or []:
        value = str(item).strip().lower()
        if value in {"phys", "physics"} and "physics" not in out:
            out.append("physics")
        elif value in {"chem", "chemistry"} and "chemistry" not in out:
            out.append("chemistry")
    return out


def initials_from_name(name: str) -> str:
    parts = [part for part in str(name).split() if part]
    if not parts:
        return "؟"
    if len(parts) == 1:
        return parts[0][:2]
    return parts[0][0] + parts[-1][0]


def derive_badges(progress: int, xp: int, stages: dict) -> list[str]:
    badges: list[str] = []
    if progress > 0 or xp > 0 or any(int(value or 0) > 0 for value in (stages or {}).values()):
        badges.append("first")
    review = int((stages or {}).get("review") or 0)
    book = int((stages or {}).get("book") or 0)
    extra = int((stages or {}).get("extra") or 0)
    if review >= 60:
        badges.append("streak3")
    if book >= 70:
        badges.append("nohint")
    if extra >= 80:
        badges.append("streak5")
    if extra >= 90:
        badges.append("proof")
    if progress >= 100 or (review >= 100 and book >= 100 and extra >= 100):
        badges.append("all")
    return badges


def format_last(iso: str) -> str:
    if not iso:
        return "الآن"
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        minutes = int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds() // 60)
        if minutes < 5:
            return "الآن"
        if minutes < 60:
            return f"منذ {minutes} د"
        hours = minutes // 60
        if hours < 24:
            return "اليوم"
        days = hours // 24
        if days == 1:
            return "أمس"
        if days < 8:
            return f"منذ {days} أيام"
        return f"منذ {days} يومًا"
    except Exception:
        return str(iso)


def progress_from_offline(progress: dict, subjects: list[str]) -> dict:
    progress = progress or {}
    use_phys = "physics" in subjects if subjects else True
    use_chem = "chemistry" in subjects if subjects else True
    stages = {"found": 0, "review": 0, "book": 0, "extra": 0}
    xp = 0
    done = 0
    total = 0
    for keys, enabled in ((PHYS_KEYS, use_phys), (CHEM_KEYS, use_chem)):
        if not enabled:
            continue
        for stage, unit_id in keys.items():
            item = progress.get(unit_id) or {}
            pct = max(0, min(100, int(item.get("percent") or 0)))
            stages[stage] = max(stages[stage], pct)
            n = int(item.get("done") or 0)
            t = int(item.get("total") or 0)
            xp += n * 10
            if stage != "found":
                done += n
                total += t
    overall = int(done * 100 / total) if total else int(sum(stages[k] for k in ("review", "book", "extra")) / 3)
    return {"stages": stages, "xp": xp, "progress": max(0, min(100, overall))}


def combine_stages(stage_progress: dict, physics_live: bool, chemistry_live: bool) -> dict:
    phys = list(stage_progress.get("phys") or [0, 0, 0, 0])
    chem = list(stage_progress.get("chem") or [0, 0, 0, 0])
    out = {}
    for i, key in enumerate(("found", "review", "book", "extra")):
        values = []
        if physics_live:
            values.append(int(phys[i]) if i < len(phys) else 0)
        if chemistry_live:
            values.append(int(chem[i]) if i < len(chem) else 0)
        out[key] = int(round(sum(values) / len(values))) if values else 0
    return out


def record_from_profile(profile: dict, xp: int = 0, progress: int = 0, stages: dict | None = None) -> dict:
    stages = stages or {"found": 0, "review": 0, "book": 0, "extra": 0}
    return {
        "id": (profile or {}).get("id"),
        "name": (profile or {}).get("name"),
        "grade": (profile or {}).get("grade"),
        "subjects": (profile or {}).get("subjects"),
        "xp": xp,
        "progress": progress,
        "stages": stages,
        "badges": derive_badges(int(progress or 0), int(xp or 0), stages),
        "teacher_id": (profile or {}).get("teacher_id") or "",
    }


def merge_offline(record: dict, offline: dict) -> dict:
    record = dict(record or {})
    profile = offline.get("profile") if isinstance(offline, dict) else None
    progress = offline.get("progress") if isinstance(offline, dict) else None
    if isinstance(profile, dict):
        if not record.get("name") and profile.get("name"):
            record["name"] = profile.get("name")
        if profile.get("grade"):
            try:
                record["grade"] = int(profile.get("grade"))
            except Exception:
                pass
        if profile.get("subjects"):
            record["subjects"] = normalize_subjects(profile.get("subjects"))
        if profile.get("id") and not record.get("id"):
            record["id"] = profile.get("id")
        if profile.get("teacher_id") and not record.get("teacher_id"):
            record["teacher_id"] = profile.get("teacher_id")
    if isinstance(progress, dict) and progress:
        parsed = progress_from_offline(progress, normalize_subjects(record.get("subjects")))
        record["xp"] = max(int(record.get("xp") or 0), int(parsed["xp"]))
        record["progress"] = max(int(record.get("progress") or 0), int(parsed["progress"]))
        stages = dict(record.get("stages") or {})
        for key, value in parsed["stages"].items():
            stages[key] = max(int(stages.get(key) or 0), int(value))
        record["stages"] = stages
        record["badges"] = derive_badges(int(record["progress"]), int(record["xp"]), stages)
    return record


def open_spreadsheet():
    import gspread
    from google.oauth2.service_account import Credentials
    import streamlit as st

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    info = dict(st.secrets["gcp_service_account"])
    if isinstance(info.get("private_key"), str):
        info["private_key"] = info["private_key"].replace("\\n", "\n")
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)
    ident = str(st.secrets["gsheets"]["spreadsheet"]).strip()
    return client.open_by_url(ident) if ident.startswith("http") else client.open_by_key(ident)


def open_worksheet(tab: str, headers: list[str]):
    sheet = open_spreadsheet()
    try:
        ws = sheet.worksheet(tab)
    except Exception as exc:
        name = exc.__class__.__name__
        if "not found" in str(exc).lower() or name.endswith("WorksheetNotFound"):
            ws = sheet.add_worksheet(title=tab, rows=2000, cols=max(len(headers), 12))
            ws.append_row(headers, value_input_option="USER_ENTERED")
            return ws
        raise
    existing = [str(cell).strip() for cell in ws.row_values(1)]
    if existing != headers:
        ws.update("A1", [headers], value_input_option="USER_ENTERED")
    return ws


def _open_ws():
    import streamlit as st

    tab = str(st.secrets.get("gsheets", {}).get("worksheet", "students") or "students").strip()
    return open_worksheet(tab, HEADERS)


def upsert_student(record: dict, merge: bool = True) -> None:
    if not is_configured():
        return
    record = dict(record or {})
    for banned in ("password", "passwordHash", "pinHash", "confirm"):
        record.pop(banned, None)
    rec_id = str(record.get("id") or "").strip()
    if not rec_id:
        return
    ws = _open_ws()
    rows = ws.get_all_records()
    stages = record.get("stages") or {}
    badges = record.get("badges") or derive_badges(int(record.get("progress") or 0), int(record.get("xp") or 0), stages)
    new_row = {
        "id": rec_id,
        "name": str(record.get("name") or "").strip(),
        "grade": int(record.get("grade") or 12),
        "subjects": ",".join(normalize_subjects(record.get("subjects"))),
        "xp": int(record.get("xp") or 0),
        "progress": int(record.get("progress") or 0),
        "badges": ",".join(badges),
        "found": int(stages.get("found") or 0),
        "review": int(stages.get("review") or 0),
        "book": int(stages.get("book") or 0),
        "extra": int(stages.get("extra") or 0),
        "last_seen": record.get("last_seen") or datetime.now(timezone.utc).isoformat(),
        "teacher_id": str(record.get("teacher_id") or "").strip(),
        "password_hash": str(record.get("password_hash") or "").strip(),
    }
    idx = None
    old = None
    for i, row in enumerate(rows):
        if str(row.get("id") or "").strip() == rec_id:
            idx = i
            old = row
            break
    if merge and old:
        if not new_row["name"]:
            new_row["name"] = str(old.get("name") or "")
        if not new_row["subjects"]:
            new_row["subjects"] = str(old.get("subjects") or "")
        try:
            old_progress = int(old.get("progress") or 0)
            if new_row["progress"] == 0 and old_progress > 0:
                new_row["progress"] = old_progress
                new_row["xp"] = max(new_row["xp"], int(old.get("xp") or 0))
                for key in ("found", "review", "book", "extra"):
                    new_row[key] = max(new_row[key], int(old.get(key) or 0))
                if not new_row["badges"]:
                    new_row["badges"] = str(old.get("badges") or "")
        except Exception:
            pass
        if not new_row["teacher_id"]:
            new_row["teacher_id"] = str(old.get("teacher_id") or "")
        if not new_row["password_hash"]:
            new_row["password_hash"] = str(old.get("password_hash") or "")
    values = [new_row[h] for h in HEADERS]
    if idx is None:
        ws.append_row(values, value_input_option="USER_ENTERED")
    else:
        ws.update(f"A{idx + 2}:N{idx + 2}", [values], value_input_option="USER_ENTERED")


def list_students(teacher_id: str | None = None, include_secrets: bool = False) -> list[dict]:
    if not is_configured():
        return []
    rows = _open_ws().get_all_records()
    teacher_id = str(teacher_id or "").strip()
    out = []
    for i, row in enumerate(rows, start=1):
        name = str(row.get("name") or "").strip()
        rec_id = str(row.get("id") or "").strip() or f"row-{i}"
        if not name and rec_id.startswith("row-"):
            continue
        row_teacher = str(row.get("teacher_id") or "").strip()
        if teacher_id and row_teacher != teacher_id:
            continue
        try:
            grade = int(row.get("grade") or 12)
        except Exception:
            grade = 12
        try:
            xp = int(row.get("xp") or 0)
        except Exception:
            xp = 0
        try:
            progress = int(row.get("progress") or 0)
        except Exception:
            progress = 0
        subjects = normalize_subjects(row.get("subjects"))
        badges = [item.strip() for item in str(row.get("badges") or "").split(",") if item.strip()]
        stages = {}
        for key in ("found", "review", "book", "extra"):
            try:
                stages[key] = int(row.get(key) or 0)
            except Exception:
                stages[key] = 0
        if not badges:
            badges = derive_badges(progress, xp, stages)
        item = {
            "id": rec_id,
            "name": name or rec_id,
            "initials": initials_from_name(name or rec_id),
            "grade": grade,
            "subjects": subjects or ["physics"],
            "xp": xp,
            "progress": max(0, min(100, progress)),
            "last": format_last(str(row.get("last_seen") or "")),
            "stages": stages,
            "badges": badges,
            "teacher_id": row_teacher,
        }
        if include_secrets:
            item["password_hash"] = str(row.get("password_hash") or "")
        out.append(item)
    return out


def safe_upsert(record: dict, merge: bool = True) -> bool:
    try:
        upsert_student(record, merge=merge)
        return True
    except Exception:
        return False
