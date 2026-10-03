from __future__ import annotations
import json
from urllib import request, error, parse
import streamlit as st


def cfg():
    c=st.secrets["supabase"]
    public=c.get("publishable_key",c.get("anon_key","")); secret=c.get("secret_key",c.get("service_role_key",""))
    return str(c["url"]).rstrip("/"),str(public),str(secret)


def _call(method,path,body=None,*,admin=False,token=None,query=""):
    base,anon,service=cfg(); key=service if admin else anon
    data=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
    headers={"apikey":key,"Content-Type":"application/json"}
    # Legacy service_role is a JWT and may be used as Bearer. New sb_secret keys
    # are API keys, not JWTs, and must only be sent in the apikey header.
    if admin and not service.startswith("sb_secret_"): headers["Authorization"]="Bearer "+service
    elif (not admin) and token: headers["Authorization"]="Bearer "+token
    req=request.Request(base+path+query,data=data,headers=headers,method=method)
    try:
        with request.urlopen(req,timeout=20) as r:
            raw=r.read().decode("utf-8"); return r.status,json.loads(raw) if raw else None
    except error.HTTPError as e:
        raw=e.read().decode("utf-8")
        try: detail=json.loads(raw)
        except Exception: detail={"message":raw}
        return e.code,detail


def register_student(email,password,profile):
    status,user=_call("POST","/auth/v1/admin/users",{"email":email,"password":password,"email_confirm":True,"user_metadata":{"full_name":profile["full_name"]}},admin=True)
    if status not in range(200,300): return False,(user or {}).get("msg") or (user or {}).get("message") or "تعذر إنشاء الحساب"
    uid=user["id"]
    row={"id":uid,**profile}
    status,result=_call("POST","/rest/v1/student_profiles",row,admin=True)
    if status not in range(200,300):
        _call("DELETE",f"/auth/v1/admin/users/{uid}",admin=True)
        return False,(result or {}).get("message","تعذر حفظ ملف الطالب")
    return True,uid


def sign_in(email,password):
    status,result=_call("POST","/auth/v1/token",{"email":email,"password":password},query="?grant_type=password")
    return (status in range(200,300),result)


def admin_rows(table,select="*"):
    query="?select="+parse.quote(select,safe="*,().:")
    status,result=_call("GET",f"/rest/v1/{table}",admin=True,query=query)
    if status not in range(200,300): raise RuntimeError((result or {}).get("message","تعذر تحميل البيانات"))
    return result or []
