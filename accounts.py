"""حسابات الأساتذة والطلبة — موافقة الأدمن، دون حفظ كلمات المرور كنص."""
from __future__ import annotations

import hashlib
import hmac
import html as html_lib
import re
import smtplib
import ssl
import uuid
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formataddr
from typing import Any

TEACHER_HEADERS = [
    "id",
    "first_name",
    "last_name",
    "email",
    "password_hash",
    "status",
    "created_at",
    "approved_at",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_password(password: str) -> str:
    salt = uuid.uuid4().hex[:16]
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    stored = str(stored or "")
    if not password or not stored:
        return False
    if "$" not in stored:
        digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if len(digest) != len(stored):
            return False
        return hmac.compare_digest(digest, stored)
    salt, digest = stored.split("$", 1)
    check = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    if len(check) != len(digest):
        return False
    return hmac.compare_digest(check, digest)


def _valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", value.strip()))


def teacher_display_name(row: dict) -> str:
    first = str(row.get("first_name") or "").strip()
    last = str(row.get("last_name") or "").strip()
    return (first + " " + last).strip() or str(row.get("email") or "أستاذ")


def _teachers_ws():
    from student_cloud_sync import open_worksheet

    return open_worksheet("teachers", TEACHER_HEADERS)


def _teacher_rows() -> list[dict]:
    try:
        return _teachers_ws().get_all_records()
    except Exception:
        return []


def list_approved_teachers() -> list[dict]:
    out = []
    for row in _teacher_rows():
        if str(row.get("status") or "").strip().lower() != "approved":
            continue
        rec_id = str(row.get("id") or "").strip()
        name = teacher_display_name(row)
        if rec_id and name:
            out.append({"id": rec_id, "name": name})
    out.sort(key=lambda item: item["name"])
    return out


def list_pending_teachers() -> list[dict]:
    out = []
    for row in _teacher_rows():
        if str(row.get("status") or "").strip().lower() != "pending":
            continue
        rec_id = str(row.get("id") or "").strip()
        if not rec_id:
            continue
        out.append(
            {
                "id": rec_id,
                "name": teacher_display_name(row),
                "email": str(row.get("email") or "").strip(),
                "created_at": str(row.get("created_at") or ""),
            }
        )
    return out


def register_teacher(first_name: str, last_name: str, email: str, password: str, confirm: str) -> tuple[bool, str]:
    first_name = str(first_name or "").strip()
    last_name = str(last_name or "").strip()
    email = str(email or "").strip().lower()
    password = str(password or "")
    confirm = str(confirm or "")
    if len(first_name) < 2:
        return False, "اكتب الاسم من حرفين على الأقل."
    if len(last_name) < 2:
        return False, "اكتب اللقب من حرفين على الأقل."
    if not _valid_email(email):
        return False, "اكتب بريدًا إلكترونيًا صحيحًا."
    if len(password) < 6:
        return False, "كلمة المرور من 6 أحرف على الأقل."
    if password != confirm:
        return False, "كلمة المرور وتأكيدها غير متطابقين."
    rows = _teacher_rows()
    for row in rows:
        if str(row.get("email") or "").strip().lower() == email:
            status = str(row.get("status") or "").strip().lower()
            if status == "pending":
                return False, "طلبك قيد المراجعة من الأدمن."
            if status == "approved":
                return False, "هذا البريد مسجّل. سجّل الدخول كأستاذ."
            return False, "هذا البريد غير متاح."
    rec_id = "tch-" + uuid.uuid4().hex[:12]
    ws = _teachers_ws()
    ws.append_row(
        [rec_id, first_name, last_name, email, hash_password(password), "pending", _now(), ""],
        value_input_option="USER_ENTERED",
    )
    try:
        notify_admin_teacher_request(first_name, last_name, email)
    except Exception:
        pass
    return True, "وصل طلبك إلى الأدمن. بعد الموافقة يمكنك تسجيل الدخول كأستاذ."


def login_teacher(email: str, password: str) -> tuple[dict | None, str]:
    email = str(email or "").strip().lower()
    password = str(password or "")
    if not email or not password:
        return None, "اكتب البريد وكلمة المرور."
    for row in _teacher_rows():
        if str(row.get("email") or "").strip().lower() != email:
            continue
        if not verify_password(password, str(row.get("password_hash") or "")):
            return None, "بيانات الدخول غير صحيحة."
        status = str(row.get("status") or "").strip().lower()
        if status == "pending":
            return None, "طلبك ما زال بانتظار موافقة الأدمن."
        if status != "approved":
            return None, "لم يُعتمد هذا الحساب."
        return {
            "id": str(row.get("id") or ""),
            "first_name": str(row.get("first_name") or ""),
            "last_name": str(row.get("last_name") or ""),
            "email": email,
            "name": teacher_display_name(row),
        }, ""
    return None, "بيانات الدخول غير صحيحة."


def _set_teacher_status(teacher_id: str, status: str) -> bool:
    ws = _teachers_ws()
    rows = ws.get_all_records()
    for i, row in enumerate(rows):
        if str(row.get("id") or "").strip() != str(teacher_id):
            continue
        approved_at = _now() if status == "approved" else ""
        ws.update(f"F{i + 2}:H{i + 2}", [[status, str(row.get("created_at") or ""), approved_at]], value_input_option="USER_ENTERED")
        return True
    return False


def approve_teacher(teacher_id: str) -> bool:
    return _set_teacher_status(teacher_id, "approved")


def reject_teacher(teacher_id: str) -> bool:
    return _set_teacher_status(teacher_id, "rejected")


def add_student_for_teacher(teacher_id: str, name: str, grade: int, subjects: list[str], password: str, confirm: str) -> tuple[bool, str]:
    from student_cloud_sync import record_from_profile, safe_upsert

    name = str(name or "").strip()
    password = str(password or "")
    confirm = str(confirm or "")
    teacher_id = str(teacher_id or "").strip()
    if not teacher_id:
        return False, "حساب الأستاذ غير صالح."
    if len(name) < 2:
        return False, "اكتب اسم الطالب من حرفين على الأقل."
    try:
        grade = int(grade)
    except Exception:
        grade = 12
    if grade not in range(6, 13):
        return False, "اختر صفًا من 6 إلى 12."
    if len(password) < 6:
        return False, "عيّن كلمة مرور من 6 أحرف على الأقل."
    if password != confirm:
        return False, "كلمة المرور وتأكيدها غير متطابقين."
    from student_cloud_sync import list_students

    for student in list_students(teacher_id=teacher_id, include_secrets=True):
        if str(student.get("name") or "").strip() == name:
            return False, "يوجد طالب بهذا الاسم في قسمك."
    rec_id = "stu-" + uuid.uuid4().hex[:12]
    record = record_from_profile({"id": rec_id, "name": name, "grade": grade, "subjects": subjects or ["phys"]})
    record["teacher_id"] = teacher_id
    record["password_hash"] = hash_password(password)
    if not safe_upsert(record, merge=False):
        return False, "تعذر حفظ الطالب. تحقق من ربط Google Sheets."
    return True, f"أُضيف {name} إلى قسمك."


def login_student(teacher_id: str, name: str, password: str) -> tuple[dict | None, str]:
    from student_cloud_sync import list_students

    teacher_id = str(teacher_id or "").strip()
    name = str(name or "").strip()
    password = str(password or "")
    if not teacher_id:
        return None, "اختر اسم الأستاذ."
    if len(name) < 2:
        return None, "اكتب اسمك كما سجّله الأستاذ."
    if not password:
        return None, "اكتب كلمة المرور التي أعطاها لك الأستاذ."
    for student in list_students(teacher_id=teacher_id, include_secrets=True):
        if str(student.get("name") or "").strip() != name:
            continue
        if not verify_password(password, str(student.get("password_hash") or "")):
            return None, "كلمة المرور غير صحيحة."
        profile = {
            "id": student.get("id"),
            "name": student.get("name"),
            "grade": student.get("grade"),
            "subjects": ["phys" if s == "physics" else "chem" if s == "chemistry" else s for s in (student.get("subjects") or [])],
            "teacher_id": teacher_id,
            "mode": "class",
        }
        return profile, ""
    return None, "لا يوجد طالب بهذا الاسم عند هذا الأستاذ."


def notify_admin_teacher_request(first_name: str, last_name: str, email: str) -> None:
    try:
        from contact_page import CONTACT_RECIPIENT, _smtp_config
    except Exception:
        return
    config = _smtp_config()
    if not config:
        return
    name = f"{first_name} {last_name}".strip()
    sent_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    plain = (
        "طلب تسجيل أستاذ جديد — الطالب الصامد\n"
        "================================\n\n"
        f"الاسم: {name}\n"
        f"البريد: {email}\n"
        f"الوقت: {sent_at}\n\n"
        "افتح لوحة الأدمن للموافقة:\n"
        "https://your-app.streamlit.app/?admin=1\n"
    )
    rich = f"""
    <div dir="rtl" style="font-family:Arial,Tahoma,sans-serif;line-height:1.8;color:#173b3d">
      <h2 style="color:#245e65">طلب تسجيل أستاذ</h2>
      <p>وصل طلب جديد إلى لوحة الأدمن.</p>
      <table style="border-collapse:collapse;width:100%;max-width:640px">
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>الاسم واللقب</b></td><td style="padding:7px;border:1px solid #dfe7e5">{html_lib.escape(name)}</td></tr>
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>البريد</b></td><td dir="ltr" style="padding:7px;border:1px solid #dfe7e5;text-align:left">{html_lib.escape(email)}</td></tr>
        <tr><td style="padding:7px;border:1px solid #dfe7e5"><b>الوقت</b></td><td dir="ltr" style="padding:7px;border:1px solid #dfe7e5">{sent_at}</td></tr>
      </table>
      <p>افتح لوحة الأدمن ثم وافق على الطلب من قسم طلبات الأساتذة.</p>
    </div>
    """
    mail = EmailMessage()
    mail["Subject"] = f"[الطالب الصامد] طلب تسجيل أستاذ — {name}"
    mail["From"] = formataddr(("منصة الطالب الصامد", str(config["sender"])))
    mail["To"] = CONTACT_RECIPIENT
    mail["Reply-To"] = email
    mail.set_content(plain)
    mail.add_alternative(rich, subtype="html")
    context = ssl.create_default_context()
    if int(config["port"]) == 465:
        with smtplib.SMTP_SSL(str(config["host"]), int(config["port"]), timeout=20, context=context) as smtp:
            smtp.login(str(config["username"]), str(config["password"]))
            smtp.send_message(mail)
    else:
        with smtplib.SMTP(str(config["host"]), int(config["port"]), timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(str(config["username"]), str(config["password"]))
            smtp.send_message(mail)
