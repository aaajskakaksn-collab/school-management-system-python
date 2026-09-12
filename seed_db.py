# -*- coding: utf-8 -*-
import os
from app import create_app, db
from app.models import User, Student, Teacher, SchoolClass, Subject
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    os.makedirs('instance', exist_ok=True)
    db.drop_all()
    db.create_all()

    # Add default admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.set_password('Admin123!')
        db.session.add(admin)

    # Add sample teachers
    t1 = Teacher(name='أحمد علي', email='ahmed@example.com')
    t2 = Teacher(name='سارة محمد', email='sara@example.com')
    db.session.add_all([t1, t2])

    # Add sample subjects
    s1 = Subject(name='الرياضيات')
    s2 = Subject(name='اللغة العربية')
    db.session.add_all([s1, s2])

    # Add sample classes
    c1 = SchoolClass(name='الصف الأول')
    c2 = SchoolClass(name='الصف الثاني')
    db.session.add_all([c1, c2])

    # Add sample students
    st1 = Student(name='محمد حسن', email='m.hassan@example.com', school_class=c1)
    st2 = Student(name='ليلى كريم', email='l.karim@example.com', school_class=c2)
    db.session.add_all([st1, st2])

    db.session.commit()

    print('قاعدة البيانات تم إنشاؤها ومليئة ببيانات تجريبية. بيانات الدخول: admin / Admin123!')
