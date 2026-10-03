import streamlit as st
from supabase_service import register_student,sign_in

st.set_page_config(page_title="التسجيل وتحميل التطبيق",page_icon="🛡️",layout="centered")
st.markdown("""<style>html,body,[class*=css]{direction:rtl;text-align:right;font-family:Tahoma,Arial,sans-serif}.stButton button,.stLinkButton a{width:100%;font-weight:800}.hero{background:#173f44;color:white;border-radius:20px;padding:22px;margin-bottom:15px}.hero p{color:#dce8e5}.ok{background:#e8f4ef;border:1px solid #bcdccd;border-radius:14px;padding:14px}</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>الطالب الصامد</h1><p>أنشئ حساب الطالب أولًا، ثم حمّل التطبيق واربطه بالحساب مرة واحدة.</p></div>',unsafe_allow_html=True)

def download_box(email):
    url=str(st.secrets.get("app",{}).get("apk_download_url","")).strip()
    st.success(f"الحساب جاهز: {email}")
    st.info("بعد تثبيت التطبيق افتحه أثناء الاتصال، ثم أدخل البريد وكلمة المرور نفسيهما. بعد الربط تعمل الوحدات دون إنترنت وتُزامن النتائج تلقائيًا.")
    if url: st.link_button("تحميل تطبيق Android (APK)",url,type="primary")
    else: st.warning("لم يضبط مدير المنصة رابط APK بعد في Streamlit Secrets.")

tab_new,tab_existing=st.tabs(["تسجيل طالب جديد","لدي حساب"])
with tab_new:
    with st.form("register",clear_on_submit=False):
        name=st.text_input("اسم الطالب الكامل")
        email=st.text_input("البريد الإلكتروني").strip().lower()
        password=st.text_input("كلمة المرور (8 أحرف على الأقل)",type="password")
        grade=st.selectbox("الصف",list(range(6,13)),index=6)
        school=st.text_input("المدرسة (اختياري)")
        governorate=st.selectbox("المحافظة",["شمال غزة","غزة","الوسطى","خان يونس","رفح","أخرى"])
        phone=st.text_input("رقم الهاتف أو ولي الأمر (اختياري)")
        subjects=st.multiselect("المواد",["الفيزياء","الكيمياء"],default=["الفيزياء","الكيمياء"])
        accepted=st.checkbox("أوافق على حفظ بيانات الحساب والنتائج التعليمية لعرضها لإدارة المنصة.")
        submit=st.form_submit_button("إنشاء الحساب")
    if submit:
        if len(name.strip())<2 or "@" not in email or len(password)<8 or not accepted:
            st.error("أكمل الاسم والبريد وكلمة مرور من 8 أحرف، ثم وافق على حفظ النتائج.")
        else:
            ok,msg=register_student(email,password,{"full_name":name.strip(),"grade":int(grade),"school":school.strip() or None,"governorate":governorate,"phone":phone.strip() or None,"subjects":subjects})
            if ok: download_box(email)
            else: st.error("تعذر إنشاء الحساب: "+str(msg))
with tab_existing:
    with st.form("signin"):
        old_email=st.text_input("البريد الإلكتروني",key="old_email").strip().lower()
        old_password=st.text_input("كلمة المرور",type="password",key="old_password")
        enter=st.form_submit_button("متابعة إلى التحميل")
    if enter:
        ok,result=sign_in(old_email,old_password)
        if ok: download_box(old_email)
        else: st.error("بيانات الدخول غير صحيحة أو الحساب غير موجود.")
