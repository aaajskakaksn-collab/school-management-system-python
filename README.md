# -*- coding: utf-8 -*-
"""
قالب مشروع مبسّط لنظام إدارة مدارس بسيط باللغة العربية (RTL)
حافظت هنا على الوظائف الأساسية فقط: تسجيل الدخول (مدير/معلم)،
إدارة الطلاب والمعلمين والصفوف والمواد، تسجيل الدرجات والحضور.

تشغيل سريع:
1) python -m venv venv
2) source venv/bin/activate  (أو venv\Scripts\activate على ويندوز)
3) pip install -r requirements.txt
4) ضع متغيرات البيئة في .env (SECRET_KEY و DATABASE_URL) أو انسخ example/.env.example
5) python seed_db.py
6) python run.py

تأكد من تشغيل التطبيق ثم افتح: http://127.0.0.1:5000/login
"""
