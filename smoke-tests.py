# -*- coding: utf-8 -*-
# Smoke tests for the School Management System
# Usage: Ensure the app is running (python run.py) then run this script in a separate terminal:
#    python smoke-tests.py

import requests
from bs4 import BeautifulSoup
import os
import sys

BASE = os.environ.get('SMOKE_BASE', 'http://127.0.0.1:5000')
ADMIN_USER = os.environ.get('SMOKE_ADMIN', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASSWORD', 'A!9kX2#b7LqP')

s = requests.Session()

results = []

def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('input', {'name': 'csrf_token'})
    return t['value'] if t else None

try:
    # 1) GET /login
    r = s.get(BASE + '/login')
    results.append(('/login GET', r.status_code == 200))
    csrf = get_csrf_token(r.text)

    # 2) POST /login with CSRF
    payload = {'username': ADMIN_USER, 'password': ADMIN_PASS}
    if csrf:
        payload['csrf_token'] = csrf
    r = s.post(BASE + '/login', data=payload, allow_redirects=True)
    results.append(('/login POST', r.status_code in (200, 302)))

    # 3) Access dashboard
    r = s.get(BASE + '/')
    results.append(('/ (dashboard)', r.status_code == 200))

    # 4) Add a student
    r = s.get(BASE + '/students')
    csrf = get_csrf_token(r.text)
    data = {'name': 'اختبار طالب', 'email': 'test@example.com', 'class_id': ''}
    if csrf: data['csrf_token'] = csrf
    r = s.post(BASE + '/students', data=data, allow_redirects=True)
    results.append(('/students ADD', r.status_code in (200,302)))

    # 5) Find the student in list
    r = s.get(BASE + '/students')
    found = 'اختبار طالب' in r.text
    results.append(('/students FIND', found))

    # 6) Add a grade
    r = s.get(BASE + '/grades')
    csrf = get_csrf_token(r.text)
    # choose existing student and subject ids from the page if possible
    # fallback: pick first options by parsing
    soup = BeautifulSoup(r.text, 'html.parser')
    s_opt = soup.find('select', {'name': 'student_id'})
    sub_opt = soup.find('select', {'name': 'subject_id'})
    student_id = s_opt.find('option')['value'] if s_opt and s_opt.find('option') else ''
    subject_id = sub_opt.find('option')['value'] if sub_opt and sub_opt.find('option') else ''
    data = {'student_id': student_id, 'subject_id': subject_id, 'value': '75'}
    if csrf: data['csrf_token'] = csrf
    r = s.post(BASE + '/grades', data=data, allow_redirects=True)
    results.append(('/grades ADD', r.status_code in (200,302)))

    # 7) Add attendance
    r = s.get(BASE + '/attendance')
    csrf = get_csrf_token(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    s_opt = soup.find('select', {'name': 'student_id'})
    student_id = s_opt.find('option')['value'] if s_opt and s_opt.find('option') else ''
    data = {'student_id': student_id, 'status': 'حاضر'}
    if csrf: data['csrf_token'] = csrf
    r = s.post(BASE + '/attendance', data=data, allow_redirects=True)
    results.append(('/attendance ADD', r.status_code in (200,302)))

    # 8) Logout and check protected page
    r = s.get(BASE + '/logout', allow_redirects=True)
    r = s.get(BASE + '/students', allow_redirects=False)
    # should redirect to login (302)
    results.append(('/students after logout should be redirect', r.status_code in (302, 401)))

except Exception as e:
    print('Exception during smoke tests:', e)
    sys.exit(2)

# Print results
ok = True
print('Smoke test results:')
for name, passed in results:
    print(f' - {name}:', 'OK' if passed else 'FAIL')
    if not passed:
        ok = False

if not ok:
    sys.exit(1)
else:
    sys.exit(0)
