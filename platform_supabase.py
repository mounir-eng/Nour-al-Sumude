"""Integration for the existing student route and existing admin dashboard."""
from __future__ import annotations
import uuid
from datetime import datetime,timezone
from urllib.parse import quote
import streamlit as st
from supabase_service import _call, register_student, sign_in, admin_rows


def configured():
    try:
        c=st.secrets.get('supabase',{})
        return bool(c.get('url') and (c.get('publishable_key') or c.get('anon_key')) and (c.get('secret_key') or c.get('service_role_key')))
    except Exception:return False


def valid_email(email):
    import re
    return bool(re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',str(email)))


def safe_error(result):
    code=str((result or {}).get('code') or (result or {}).get('error_code') or '')
    if code in {'email_exists','user_already_exists'}:return 'هذا البريد مسجل بالفعل. استخدم تسجيل الدخول.'
    return 'تعذر حفظ الحساب في Supabase. تحقق من إعدادات Secrets والجداول، ثم حاول مجددًا.'


def authenticate(email,password):
    ok,result=sign_in(email,password)
    if not ok:raise ValueError('تعذر الدخول: تحقق من البريد وكلمة المرور وتفعيل الحساب.')
    token=result['access_token'];uid=result['user']['id']
    status,rows=_call('GET','/rest/v1/student_profiles',token=token,query='?id=eq.'+quote(uid)+'&select=*')
    if status not in range(200,300) or not rows:raise ValueError('الحساب موجود لكن ملف الطالب غير موجود؛ راجع إدارة المنصة.')
    row=rows[0]
    st.session_state['_supabase_session']=result
    return {'id':uid,'name':row['full_name'],'email':email,'grade':row['grade'],'grades':row.get('grades') or [row['grade']],
            'subjects':row.get('subjects') or ['phys','chem'],'mode':'supabase','firstFeedbackDone':False,'feedbackStages':[],'feedbackBonus':0}


def save_account(old,raw):
    email=str(raw.get('email','')).strip().lower();password=str(raw.get('password',''))
    if not valid_email(email):raise ValueError('أدخل بريدًا إلكترونيًا صحيحًا؛ ستستخدمه لدخول التطبيق.')
    grades=[int(g) for g in (raw.get('grades') or [raw['grade']]) if int(g) in range(6,13)]
    row={'full_name':raw['name'],'grade':grades[0],'grades':grades,'subjects':raw['subjects'],'email':email}
    session=st.session_state.get('_supabase_session') or {}
    if old.get('mode')=='supabase' and session.get('user',{}).get('id')==old.get('id'):
        if email!=old.get('email'):raise ValueError('لا تغيّر البريد من تعديل الملف؛ أبقه كما هو حاليًا.')
        status,result=_call('PATCH','/rest/v1/student_profiles',row,admin=True,query='?id=eq.'+quote(old['id']))
        if status not in range(200,300):raise ValueError(safe_error(result))
        if password:
            status,result=_call('PUT','/auth/v1/admin/users/'+old['id'],{'password':password},admin=True)
            if status not in range(200,300):raise ValueError('تم تحديث البيانات لكن تعذر تغيير كلمة المرور.')
        return {**old,'name':row['full_name'],'grade':row['grade'],'grades':grades,'subjects':row['subjects']}
    if len(password)<8:raise ValueError('استخدم كلمة مرور من 8 أحرف على الأقل.')
    ok,result=register_student(email,password,row)
    if not ok:raise ValueError('تعذر التسجيل. قد يكون البريد مستخدمًا؛ جرّب تسجيل الدخول. وإلا راجع إعدادات Supabase.')
    return authenticate(email,password)


def save_web_progress(profile,percent,completed,total,stages):
    if profile.get('mode')!='supabase':return
    session=st.session_state.get('_supabase_session') or {}
    if session.get('user',{}).get('id')!=profile.get('id'):return
    signature=(int(percent),int(completed),int(total),str(stages))
    if st.session_state.get('_web_sync_signature')==signature:return
    device=st.session_state.setdefault('_web_device',str(uuid.uuid4()))
    now=datetime.now(timezone.utc).isoformat()
    body={'student_id':profile['id'],'device_id':device,'unit_id':'website_overall','percent':percent,'completed':completed,'total':total,
          'client_updated_at':now,'payload':{'source':'website','stages':stages}}
    # authenticated session identity above is required; server key never reaches HTML.
    from supabase_service import cfg
    base,public,secret=cfg()
    import json
    from urllib.request import Request,urlopen
    headers={'apikey':secret,'Content-Type':'application/json','Prefer':'resolution=merge-duplicates,return=minimal'}
    if not secret.startswith('sb_secret_'):headers['Authorization']='Bearer '+secret
    req=Request(base+'/rest/v1/progress_snapshots?on_conflict=student_id,device_id,unit_id',data=json.dumps(body).encode(),headers=headers,method='POST')
    with urlopen(req,timeout=15):pass
    st.session_state['_web_sync_signature']=signature


def render_admin_results():
    st.subheader('حسابات Supabase ونتائج التطبيق')
    if not configured():st.warning('أضف قسم [supabase] إلى Streamlit Secrets.');return
    try:
        profiles=admin_rows('student_profiles');results=admin_rows('progress_snapshots')
    except Exception:
        st.error('تعذر قراءة Supabase. تحقق من Project URL وSecret key والجداول.');return
    st.caption('النتائج هنا من Supabase؛ جدول Google Sheets القديم يظهر أدناه مستقلاً.')
    if not profiles:st.info('لا توجد حسابات Supabase بعد. سجّل طالبًا من نموذج المنصة المحدث.');return
    latest={}
    for r in results:
        key=(r['student_id'],r['unit_id'])
        if key not in latest or r.get('server_updated_at','')>latest[key].get('server_updated_at',''):latest[key]=r
    rows=[]
    for p in profiles:
        matches=[r for (sid,unit),r in latest.items() if sid==p['id']]
        for r in matches or [{}]:
            rows.append({'الطالب':p['full_name'],'البريد':p.get('email',''),'الصفوف':', '.join(map(str,p.get('grades') or [p['grade']])),'الوحدة':r.get('unit_id','لم تصل نتائج بعد'),'التقدم %':r.get('percent',0),'المكتمل':r.get('completed',0),'الإجمالي':r.get('total',0),'آخر مزامنة':r.get('server_updated_at','—')})
    st.dataframe(rows,hide_index=True,use_container_width=True)
