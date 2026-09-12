# -*- coding: utf-8 -*-
import os
from app import create_app, db
from app.models import User, Student, Teacher, SchoolClass, Subject, Grade, Attendance

# Read admin password from environment if provided. Do NOT store secrets in the repo.
SECURE_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'A!9kX2#b7LqP')

app = create_app()

with app.app_context():
    os.makedirs('example', exist_ok=True)
    # حذف الجداول القديمة وإنشاء جديدة لضمان القيم التجريبية النقية
    db.drop_all()
    db.create_all()

    # Add default admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True, role='admin')
        admin.set_password(SECURE_ADMIN_PASSWORD)
        db.session.add(admin)

    # إضافة معلمين تجريبيين
    t1 = Teacher(name='أحمد علي', email='ahmed@example.com')
    t2 = Teacher(name='سارة محمد', email='sara@example.com')
    db.session.add_all([t1, t2])

    # إضافة مواد مرتبطة بالمعلمين
    s1 = Subject(name='الرياضيات', teacher=t1)
    s2 = Subject(name='اللغة العربية', teacher=t2)
    db.session.add_all([s1, s2])

    # إضافة صفوف
    c1 = SchoolClass(name='الصف الأول')
    c2 = SchoolClass(name='الصف الثاني')
    db.session.add_all([c1, c2])

    # إضافة طلاب مرتبطة بالصفوف
    st1 = Student(name='محمد حسن', email='m.hassan@example.com', school_class=c1)
    st2 = Student(name='ليلى كريم', email='l.karim@example.com', school_class=c2)
    db.session.add_all([st1, st2])

    db.session.commit()

    # إضافة درجات بعد معرفة ids
    g1 = Grade(student_id=st1.id, subject_id=s1.id, value=85.0)
    g2 = Grade(student_id=st2.id, subject_id=s2.id, value=92.5)
    db.session.add_all([g1, g2])

    a1 = Attendance(student_id=st1.id, status='حاضر')
    a2 = Attendance(student_id=st2.id, status='غائب')
    db.session.add_all([a1, a2])

    db.session.commit()

    print('قاعدة البيانات تم إنشاؤها ومليئة ببيانات تجريبية.')
    print('ملاحظة: إذا لم تكن قد عيّنت متغير البيئة ADMIN_PASSWORD فُيستخدم قيمة افتراضية لأغراض الاختبار.')
    print('بيانات الدخول التجريبية:')
    print('  اسم المستخدم: admin')
    print(f'  كلمة المرور: {SECURE_ADMIN_PASSWORD}')
