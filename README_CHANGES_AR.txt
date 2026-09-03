تحديث v23 — ملفات التغيير فقط (ارفعها إلى GitHub مع الحفاظ على المسارات)
=========================================================================

1) تمارين «علّل»: حذف خطوات الحل تمامًا (لا الشريط البرتقالي ولا الفراغات)
   ويبقى فقط صندوق الخيارات الثلاثة ثم زر «تحقق».
   (في Streamlit وفي نسخة الأوفلاين/PWA معًا)

2) قبول ترتيب الرموز (الضرب تبديلي):
   - I = F × Δt  ≡  I = Δt × F
   - P = m v      ≡  P = v m
   - m × v = P    ≡  P = v × m   (طرفا المساواة قابلان للتبادل)
   - تجاهل الفراغات والأقواس وأشكال × · * وـ ÷ /
   - ما لم يُقبل (عن قصد): تبديل طرفي القسمة (ΔP ÷ Δt ≠ Δt ÷ ΔP)
     وتبديل أرقام (12 ≠ 21).

3) رفع ذاكرة التخزين المؤقت: service-worker ← samed-core-v23 (يفرض تحديث الأوفلاين)
   وإعادة بناء حزم الأوفلاين مع تحديث بصمات SHA256.

الملفات (9):
  pages/physics_textbook_exercises.py
  app.py
  static/pwa/unit.js
  static/pwa/styles.css
  static/pwa/service-worker.js
  static/pwa/unit-physics-textbook-data.js
  unit_packs/physics12_unit1_complete_offline.zip
  unit_packs/student_samed_pwa_offline.zip
  unit_packs/OFFLINE_PACKS_V18_SHA256.txt

بعد الرفع: Commit changes ← ثم في Streamlit: Manage app → Reboot app ← ثم Ctrl+Shift+R.
