import csv,io,hmac
import streamlit as st
from supabase_service import admin_rows

st.set_page_config(page_title="لوحة مزامنة الطلاب",page_icon="📊",layout="wide")
st.markdown("<style>html,body,[class*=css]{direction:rtl;text-align:right;font-family:Tahoma,Arial,sans-serif}</style>",unsafe_allow_html=True)
if not st.session_state.get("sync_admin_ok"):
    st.title("دخول إدارة المنصة")
    with st.form("admin_login"):
        password=st.text_input("كلمة مرور لوحة الإدارة",type="password")
        go=st.form_submit_button("دخول")
    expected=str(st.secrets.get("app",{}).get("admin_dashboard_password",""))
    if go:
        if expected and hmac.compare_digest(password,expected): st.session_state["sync_admin_ok"]=True;st.rerun()
        else: st.error("كلمة المرور غير صحيحة.")
    st.stop()

st.title("📊 نتائج تطبيق الطالب الصامد")
st.caption("تعرض أحدث نسخة وصلت من كل جهاز، وتبقى النتائج غير المتصلة محفوظة حتى تعود الشبكة.")
try:
    profiles=admin_rows("student_profiles");snapshots=admin_rows("progress_snapshots")
except Exception as e:
    st.error(str(e));st.stop()
by_id={p["id"]:p for p in profiles};latest={}
for r in snapshots:
    key=(r.get("student_id"),r.get("unit_id"));stamp=r.get("client_updated_at") or r.get("server_updated_at") or ""
    if key not in latest or stamp>(latest[key].get("client_updated_at") or latest[key].get("server_updated_at") or ""):latest[key]=r
rows=[]
for r in latest.values():
    p=by_id.get(r.get("student_id"),{})
    rows.append({"الطالب":p.get("full_name","—"),"الصف":p.get("grade","—"),"المحافظة":p.get("governorate","—"),"الوحدة":r.get("unit_id","—"),"التقدم %":r.get("percent",0),"المكتمل":r.get("completed",0),"الإجمالي":r.get("total",0),"آخر مزامنة":r.get("server_updated_at","—"),"معرف الطالب":r.get("student_id","")})
rows.sort(key=lambda x:(str(x["الطالب"]),str(x["الوحدة"])))
c1,c2,c3,c4=st.columns(4)
c1.metric("الطلاب المسجلون",len(profiles));c2.metric("طلاب لديهم نتائج",len({r.get('student_id') for r in snapshots}));c3.metric("الوحدات المتزامنة",len(rows));c4.metric("متوسط التقدم",f"{round(sum(int(r['التقدم %']) for r in rows)/len(rows)) if rows else 0}%")
if rows:
    st.dataframe(rows,use_container_width=True,hide_index=True)
    out=io.StringIO();w=csv.DictWriter(out,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
    st.download_button("تنزيل النتائج CSV",out.getvalue().encode("utf-8-sig"),"student-results.csv","text/csv")
else:st.info("لم تصل نتائج من التطبيق بعد.")
