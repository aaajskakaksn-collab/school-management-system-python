# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Student, Teacher, SchoolClass, Subject, Grade, Attendance

admin_bp = Blueprint('admin', __name__)


def admin_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or (not getattr(current_user, 'is_admin', False)):
            flash('غير مصرح بالدخول', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapper


def teacher_or_admin(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('الرجاء تسجيل الدخول', 'danger')
            return redirect(url_for('auth.login'))
        # teacher role may have limited permissions in المستقبل، الآن نفس الصلاحيات الأساسية
        return func(*args, **kwargs)

    return wrapper


@admin_bp.route('/')
@login_required
@teacher_or_admin
def dashboard():
    students_count = Student.query.count()
    teachers_count = Teacher.query.count()
    classes_count = SchoolClass.query.count()
    return render_template('dashboard.html', students_count=students_count, teachers_count=teachers_count, classes_count=classes_count)


# Students
@admin_bp.route('/students', methods=['GET', 'POST'])
@login_required
@teacher_or_admin
def students():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        class_id = request.form.get('class_id') or None
        s = Student(name=name, email=email, class_id=class_id)
        db.session.add(s)
        db.session.commit()
        flash('تم إضافة الطالب', 'success')
        return redirect(url_for('admin.students'))

    students = Student.query.order_by(Student.name).all()
    classes = SchoolClass.query.order_by(SchoolClass.name).all()
    return render_template('students.html', students=students, classes=classes)


@admin_bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_or_admin
def edit_student(id):
    s = Student.query.get_or_404(id)
    if request.method == 'POST':
        s.name = request.form.get('name')
        s.email = request.form.get('email')
        s.class_id = request.form.get('class_id') or None
        db.session.commit()
        flash('تم حفظ التغييرات', 'success')
        return redirect(url_for('admin.students'))
    classes = SchoolClass.query.order_by(SchoolClass.name).all()
    return render_template('students_edit.html', student=s, classes=classes)


@admin_bp.route('/students/delete/<int:id>', methods=['POST'])
@login_required
@teacher_or_admin
def delete_student(id):
    s = Student.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('تم حذف الطالب', 'success')
    return redirect(url_for('admin.students'))


# Teachers
@admin_bp.route('/teachers', methods=['GET', 'POST'])
@login_required
@admin_required
def teachers():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        t = Teacher(name=name, email=email)
        db.session.add(t)
        db.session.commit()
        flash('تم إضافة المعلم', 'success')
        return redirect(url_for('admin.teachers'))

    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template('teachers.html', teachers=teachers)


@admin_bp.route('/teachers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_teacher(id):
    t = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        t.name = request.form.get('name')
        t.email = request.form.get('email')
        db.session.commit()
        flash('تم حفظ التغييرات', 'success')
        return redirect(url_for('admin.teachers'))
    return render_template('teachers_edit.html', teacher=t)


@admin_bp.route('/teachers/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_teacher(id):
    t = Teacher.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash('تم حذف المعلم', 'success')
    return redirect(url_for('admin.teachers'))


# Classes
@admin_bp.route('/classes', methods=['GET', 'POST'])
@login_required
@admin_required
def classes():
    if request.method == 'POST':
        name = request.form.get('name')
        c = SchoolClass(name=name)
        db.session.add(c)
        db.session.commit()
        flash('تم إضافة الصف', 'success')
        return redirect(url_for('admin.classes'))

    classes = SchoolClass.query.order_by(SchoolClass.name).all()
    return render_template('classes.html', classes=classes)


@admin_bp.route('/classes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_class(id):
    c = SchoolClass.query.get_or_404(id)
    if request.method == 'POST':
        c.name = request.form.get('name')
        db.session.commit()
        flash('تم حفظ التغييرات', 'success')
        return redirect(url_for('admin.classes'))
    return render_template('classes_edit.html', class_item=c)


# Subjects
@admin_bp.route('/subjects', methods=['GET', 'POST'])
@login_required
@admin_required
def subjects():
    if request.method == 'POST':
        name = request.form.get('name')
        teacher_id = request.form.get('teacher_id') or None
        subj = Subject(name=name, teacher_id=teacher_id)
        db.session.add(subj)
        db.session.commit()
        flash('تم إضافة المادة', 'success')
        return redirect(url_for('admin.subjects'))

    subjects = Subject.query.order_by(Subject.name).all()
    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template('subjects.html', subjects=subjects, teachers=teachers)


@admin_bp.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subject(id):
    s = Subject.query.get_or_404(id)
    if request.method == 'POST':
        s.name = request.form.get('name')
        s.teacher_id = request.form.get('teacher_id') or None
        db.session.commit()
        flash('تم حفظ التغييرات', 'success')
        return redirect(url_for('admin.subjects'))
    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template('subjects_edit.html', subject=s, teachers=teachers)


# Grades
@admin_bp.route('/grades', methods=['GET', 'POST'])
@login_required
@teacher_or_admin
def grades():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        value = request.form.get('value')
        g = Grade(student_id=student_id, subject_id=subject_id, value=float(value))
        db.session.add(g)
        db.session.commit()
        flash('تم إضافة الدرجة', 'success')
        return redirect(url_for('admin.grades'))

    grades = Grade.query.order_by(Grade.date.desc()).all()
    students = Student.query.order_by(Student.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('grades.html', grades=grades, students=students, subjects=subjects)


@admin_bp.route('/grades/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_or_admin
def edit_grade(id):
    g = Grade.query.get_or_404(id)
    if request.method == 'POST':
        g.student_id = request.form.get('student_id')
        g.subject_id = request.form.get('subject_id')
        g.value = float(request.form.get('value'))
        db.session.commit()
        flash('تم حفظ التغييرات', 'success')
        return redirect(url_for('admin.grades'))
    students = Student.query.order_by(Student.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('grades_edit.html', grade=g, students=students, subjects=subjects)


# Attendance
@admin_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
@teacher_or_admin
def attendance():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        status = request.form.get('status')
        a = Attendance(student_id=student_id, status=status)
        db.session.add(a)
        db.session.commit()
        flash('تم تسجيل الحضور', 'success')
        return redirect(url_for('admin.attendance'))

    attendance = Attendance.query.order_by(Attendance.date.desc()).all()
    students = Student.query.order_by(Student.name).all()
    return render_template('attendance.html', attendance=attendance, students=students)


@admin_bp.route('/attendance/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_or_admin
def edit_attendance(id):
    a = Attendance.query.get_or_404(id)
    if request.method == 'POST':
        a.student_id = request.form.get('student_id')
        a.status = request.form.get('status')
        db.session.commit()
        flash('تم حفظ التغييرات', 'success')
        return redirect(url_for('admin.attendance'))
    students = Student.query.order_by(Student.name).all()
    return render_template('attendance_edit.html', attendance_record=a, students=students)


# Search route
@admin_bp.route('/search')
@login_required
@teacher_or_admin
def search():
    q = request.args.get('q', '')
    students = Student.query.filter(Student.name.contains(q)).all() if q else []
    teachers = Teacher.query.filter(Teacher.name.contains(q)).all() if q else []
    classes = SchoolClass.query.filter(SchoolClass.name.contains(q)).all() if q else []
    return render_template('search.html', q=q, students=students, teachers=teachers, classes=classes)
