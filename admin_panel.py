"""Professional admin dashboard for الطالب الصامد."""
from __future__ import annotations
import html
from typing import Any
import streamlit as st
from student_cloud_sync import (delete_feedback,delete_message,last_sheets_error,list_feedback,list_messages,list_students,sheets_configured,spreadsheet_key,update_feedback_status,update_message_status)

UI="samed-admin-ui-v8-feedback"
def e(v:Any)->str:return html.escape(str(v or ""))
def n(v:Any)->int:
    try:return max(0,min(100,int(float(str(v).replace('%','') or 0))))
    except:return 0

def css():
 st.markdown(f'''<style>@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;800&display=swap');html,body,.stApp{{font-family:Cairo,'Noto Sans Arabic',Tahoma,sans-serif!important;direction:rtl;text-align:right}}.stApp{{background:#f3f6f5}}[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stSidebar"]{{display:none!important}}.block-container{{max-width:1180px!important;padding-top:1rem!important}}.{UI} .hero{{background:linear-gradient(135deg,#173f44,#245e65 58%,#2f7a72);color:#fff;border-radius:24px;padding:24px;box-shadow:0 16px 38px rgba(23,63,68,.2);margin-bottom:14px}}.{UI} .hero small{{color:#f5c65a;font-weight:800}}.{UI} .hero h2{{margin:7px 0}}.{UI} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin-top:15px}}.{UI} .kpi{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.13);padding:13px;border-radius:15px}}.{UI} .kpi span{{display:block;font-size:12px;color:#dce9e6}}.{UI} .kpi b{{display:block;font-size:26px;color:#f5c65a}}.{UI} .nav{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0}}.{UI} .navcard{{background:#fff;border:1px solid #d7e4e1;border-radius:18px;padding:15px;text-align:center;box-shadow:0 8px 20px rgba(23,63,68,.06)}}.{UI} .navcard i{{font-style:normal;font-size:28px;display:block}}.{UI} .navcard b{{display:block;margin-top:5px}}.{UI} table{{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border-radius:18px;overflow:hidden}}.{UI} th{{background:#173f44;color:#f5c65a;padding:11px;font-size:12px}}.{UI} td{{padding:11px;border-bottom:1px solid #e7eeec;font-size:13px}}.{UI} .bar{{height:7px;background:#e7efed;border-radius:99px;overflow:hidden;min-width:80px}}.{UI} .bar i{{display:block;height:100%;background:linear-gradient(90deg,#245e65,#f5c65a)}}.{UI} .item{{background:#fff;border:1px solid #d7e4e1;border-radius:17px;padding:15px;margin:9px 0;box-shadow:0 7px 18px rgba(23,63,68,.05)}}.{UI} .tags span{{display:inline-block;background:#eef7f4;color:#245e65;border-radius:999px;padding:3px 8px;margin:3px;font-size:11px}}@media(max-width:800px){{.{UI} .grid{{grid-template-columns:1fr 1fr}}.{UI} .nav{{grid-template-columns:1fr}}}}</style>''',unsafe_allow_html=True)

def login():
 if st.session_state.get('admin_ok'):return True
 try:expected=str(st.secrets.get('admin',{}).get('password') or '')
 except:expected=''
 st.markdown(f'<div class="{UI}"><div class="hero"><small>لوحة الإدارة</small><h2>دخول المشرف</h2><p>متابعة الطلبة والرسائل وآراء تجربة التعلم.</p></div></div>',unsafe_allow_html=True)
 if not expected:st.warning('أضف كلمة مرور الأدمن في Streamlit Cloud عبر Settings → Secrets.');return False
 with st.form('admin_login_v8'):
  pwd=st.text_input('كلمة المرور',type='password');ok=st.form_submit_button('دخول',use_container_width=True)
 if ok and pwd==expected:st.session_state['admin_ok']=True;st.rerun()
 if ok:st.error('كلمة المرور غير صحيحة.')
 return False

def feedback_page(status):
 title='آراء الطلبة الجديدة' if status=='new' else 'آراء تمت معالجتها'
 st.markdown(f'<div class="{UI}"><div class="hero"><small>تحسين المنصة</small><h2>{title}</h2><p>التجربة الأولى وتقييمات نهاية المراحل في مكان واحد.</p></div></div>',unsafe_allow_html=True)
 if st.button('← العودة إلى الرئيسية',key='back_feedback_'+status):st.session_state.admin_view='home';st.rerun()
 rows=list_feedback(status)
 if not rows:st.info('لا توجد تقييمات هنا حاليًا.');return
 for r in reversed(rows):
  typ='التجربة الأولى' if r.get('feedback_type')=='first_use' else ('نهاية مرحلة · '+str(r.get('stage_title') or ''))
  stars=('★'*int(float(r.get('stars') or 0))) if str(r.get('stars') or '').replace('.','',1).isdigit() else ''
  tags=''.join(f'<span>{e(x)}</span>' for x in [r.get('rating'),r.get('difficulty'),stars,r.get('confidence')] if x)
  details=' · '.join(str(r.get(x) or '') for x in ['likes','issues','improvements','lesson'] if r.get(x))
  st.markdown(f'<div class="{UI}"><div class="item"><b>{e(r.get("student_name"))}</b> · {e(typ)}<br><small>{e(r.get("created_at"))} · الصف {e(r.get("grade"))}</small><div class="tags">{tags}</div><p>{e(details)}</p><p>{e(r.get("note"))}</p></div></div>',unsafe_allow_html=True)
  c1,c2=st.columns(2);fid=str(r.get('id') or '')
  if status=='new' and c1.button('تمت المعالجة',key='fb_done_'+fid):update_feedback_status(fid,'processed');st.rerun()
  if c2.button('حذف',key='fb_del_'+status+'_'+fid):delete_feedback(fid);st.rerun()

def messages_page(status):
 title='رسائل التواصل' if status=='new' else 'الرسائل المعالجة'
 st.markdown(f'<div class="{UI}"><div class="hero"><small>لوحة الإدارة</small><h2>{title}</h2></div></div>',unsafe_allow_html=True)
 if st.button('← العودة إلى الرئيسية',key='back_msg_'+status):st.session_state.admin_view='home';st.rerun()
 rows=list_messages(status)
 if not rows:st.info('لا توجد رسائل هنا حاليًا.');return
 for r in reversed(rows):
  st.markdown(f'<div class="{UI}"><div class="item"><b>{e(r.get("name"))}</b> · {e(r.get("subject"))}<br><small>{e(r.get("created_at"))}</small><p>{e(r.get("message"))}</p></div></div>',unsafe_allow_html=True)
  c1,c2=st.columns(2);mid=str(r.get('id') or '')
  if status=='new' and c1.button('تمت المعالجة',key='msg_done_'+mid):update_message_status(mid,'processed');st.rerun()
  if c2.button('حذف',key='msg_del_'+status+'_'+mid):delete_message(mid);st.rerun()

def render_admin_panel():
 css()
 if not login():return
 view=st.session_state.get('admin_view','home')
 if view=='feedback':feedback_page('new');return
 if view=='feedback_done':feedback_page('processed');return
 if view=='messages':messages_page('new');return
 students=list_students() if sheets_configured() else [];feedback=list_feedback('new') if sheets_configured() else [];messages=list_messages('new') if sheets_configured() else []
 avg=round(sum(n(x.get('progress')) for x in students)/len(students)) if students else 0
 st.markdown(f'<div class="{UI}"><div class="hero"><small>لوحة الإدارة · الطالب الصامد</small><h2>متابعة التعلم وتطوير تجربة الطلبة</h2><p>إحصائيات واضحة، تقدم الطلبة، ورسائل التغذية الراجعة.</p><div class="grid"><div class="kpi"><span>الطلبة</span><b>{len(students)}</b></div><div class="kpi"><span>متوسط التقدم</span><b>{avg}%</b></div><div class="kpi"><span>آراء جديدة</span><b>{len(feedback)}</b></div><div class="kpi"><span>رسائل جديدة</span><b>{len(messages)}</b></div></div></div><div class="nav"><div class="navcard"><i>💬</i><b>آراء الطلبة</b><small>تقييم التجربة والمراحل</small></div><div class="navcard"><i>✅</i><b>الآراء المعالجة</b><small>سجل التحسينات</small></div><div class="navcard"><i>✉️</i><b>رسائل التواصل</b><small>طلبات واستفسارات</small></div></div></div>',unsafe_allow_html=True)
 a,b,c=st.columns(3)
 if a.button('فتح آراء الطلبة',use_container_width=True):st.session_state.admin_view='feedback';st.rerun()
 if b.button('فتح الآراء المعالجة',use_container_width=True):st.session_state.admin_view='feedback_done';st.rerun()
 if c.button('فتح رسائل التواصل',use_container_width=True):st.session_state.admin_view='messages';st.rerun()
 if not sheets_configured():st.warning('لم يُضبط Google Sheets بعد. أضف [gsheets] و[gcp_service_account] في Secrets.')
 elif last_sheets_error():st.error(last_sheets_error())
 rows=''
 for s in students:
  pct=n(s.get('progress'));rows+=f'<tr><td><b>{e(s.get("name"))}</b><br><small>{e(s.get("id"))}</small></td><td>{e(s.get("grade"))}</td><td>{e(s.get("subjects"))}</td><td><div class="bar"><i style="width:{pct}%"></i></div>{pct}%</td><td>{e(s.get("xp"))}</td><td>{e(s.get("last_seen"))}</td></tr>'
 table='<p>لا توجد تسجيلات بعد.</p>' if not rows else '<table><thead><tr><th>الطالب</th><th>الصف</th><th>المواد</th><th>التقدم</th><th>XP</th><th>آخر نشاط</th></tr></thead><tbody>'+rows+'</tbody></table>'
 st.markdown(f'<div class="{UI}">{table}</div>',unsafe_allow_html=True)
