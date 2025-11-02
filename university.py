from flask import Blueprint, render_template, request, redirect, url_for, Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from database import db
from models import *
import csv
import io
from datetime import datetime
import os

university_bp = Blueprint('university', __name__, template_folder='templates', static_folder='static')

# Forms
class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=100)])
    major = StringField('Major', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Submit')

class ProfessorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=100)])
    department = StringField('Department', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Submit')

class CourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    code = StringField('Code', validators=[DataRequired(), Length(min=1, max=20)])
    credits = IntegerField('Credits', validators=[DataRequired()], default=3)
    professor_id = SelectField('Professor', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Submit')

class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student', coerce=str, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    grade = StringField('Grade', validators=[Length(max=2)])
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    student_id = SelectField('Student', coerce=str, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    amount_paid = IntegerField('Amount Paid ($)', validators=[DataRequired()])
    status = SelectField('Status', choices=[('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Routes
@university_bp.route('/')
def index():
    return render_template('index.html')

@university_bp.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@university_bp.route('/students/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data, major=form.major.data)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('university.students'))
    return render_template('add_student.html', form=form)

@university_bp.route('/students/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.email = form.email.data
        student.major = form.major.data
        db.session.commit()
        return redirect(url_for('university.students'))
    return render_template('edit_student.html', form=form)

@university_bp.route('/students/delete/<id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('university.students'))

@university_bp.route('/professors')
def professors():
    professors = Professor.query.all()
    return render_template('professors.html', professors=professors)

@university_bp.route('/professors/add', methods=['GET', 'POST'])
def add_professor():
    form = ProfessorForm()
    if form.validate_on_submit():
        professor = Professor(name=form.name.data, email=form.email.data, department=form.department.data)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('university.professors'))
    return render_template('add_professor.html', form=form)

@university_bp.route('/professors/edit/<id>', methods=['GET', 'POST'])
def edit_professor(id):
    professor = Professor.query.get_or_404(id)
    form = ProfessorForm(obj=professor)
    if form.validate_on_submit():
        professor.name = form.name.data
        professor.email = form.email.data
        professor.department = form.department.data
        db.session.commit()
        return redirect(url_for('university.professors'))
    return render_template('edit_professor.html', form=form)

@university_bp.route('/professors/delete/<id>')
def delete_professor(id):
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    return redirect(url_for('university.professors'))

@university_bp.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@university_bp.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    form.professor_id.choices = [(p.id, p.name) for p in Professor.query.all()]
    if form.validate_on_submit():
        course = Course(name=form.name.data, code=form.code.data, credits=form.credits.data, professor_id=form.professor_id.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('university.courses'))
    return render_template('add_course.html', form=form)

@university_bp.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    form.professor_id.choices = [(p.id, p.name) for p in Professor.query.all()]
    if form.validate_on_submit():
        course.name = form.name.data
        course.code = form.code.data
        course.credits = form.credits.data
        course.professor_id = form.professor_id.data
        db.session.commit()
        return redirect(url_for('university.courses'))
    return render_template('edit_course.html', form=form)

@university_bp.route('/courses/delete/<int:id>')
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('university.courses'))

@university_bp.route('/enrollments')
def enrollments():
    enrollments = Enrollment.query.all()
    return render_template('enrollments.html', enrollments=enrollments)

@university_bp.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    form = EnrollmentForm()
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.all()]
    if form.validate_on_submit():
        enrollment = Enrollment(student_id=form.student_id.data, course_id=form.course_id.data, grade=form.grade.data)
        db.session.add(enrollment)
        db.session.commit()
        return redirect(url_for('university.enrollments'))
    return render_template('add_enrollment.html', form=form)

@university_bp.route('/enrollments/edit/<int:id>', methods=['GET', 'POST'])
def edit_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    form = EnrollmentForm(obj=enrollment)
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.all()]
    if form.validate_on_submit():
        enrollment.student_id = form.student_id.data
        enrollment.course_id = form.course_id.data
        enrollment.grade = form.grade.data
        db.session.commit()
        return redirect(url_for('university.enrollments'))
    return render_template('edit_enrollment.html', form=form)

@university_bp.route('/enrollments/delete/<int:id>')
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('university.enrollments'))

@university_bp.route('/payments')
def payments():
    payments = TuitionPayment.query.all()
    return render_template('payments.html', payments=payments)

@university_bp.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    form = PaymentForm()
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    form.course_id.choices = [(c.id, f"{c.name} ({c.code})") for c in Course.query.all()]
    if form.validate_on_submit():
        payment = TuitionPayment(
            student_id=form.student_id.data,
            course_id=form.course_id.data,
            amount_paid=form.amount_paid.data,
            status=form.status.data
        )
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('university.payments'))
    return render_template('add_payment.html', form=form)

@university_bp.route('/payments/edit/<int:id>', methods=['GET', 'POST'])
def edit_payment(id):
    payment = TuitionPayment.query.get_or_404(id)
    form = PaymentForm(obj=payment)
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    form.course_id.choices = [(c.id, f"{c.name} ({c.code})") for c in Course.query.all()]
    if form.validate_on_submit():
        payment.student_id = form.student_id.data
        payment.course_id = form.course_id.data
        payment.amount_paid = form.amount_paid.data
        payment.status = form.status.data
        db.session.commit()
        return redirect(url_for('university.payments'))
    return render_template('edit_payment.html', form=form)

@university_bp.route('/payments/delete/<int:id>')
def delete_payment(id):
    payment = TuitionPayment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    return redirect(url_for('university.payments'))

# Export routes
@university_bp.route('/students/export')
def export_students():
    students = Student.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Major'])
    for student in students:
        writer.writerow([student.id, student.name, student.email, student.major])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=students.csv'})

@university_bp.route('/professors/export')
def export_professors():
    professors = Professor.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Department'])
    for professor in professors:
        writer.writerow([professor.id, professor.name, professor.email, professor.department])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=professors.csv'})

@university_bp.route('/courses/export')
def export_courses():
    courses = Course.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Code', 'Credits', 'Professor ID'])
    for course in courses:
        writer.writerow([course.id, course.name, course.code, course.credits, course.professor_id])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=courses.csv'})

@university_bp.route('/enrollments/export')
def export_enrollments():
    enrollments = Enrollment.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Student ID', 'Course ID', 'Grade'])
    for enrollment in enrollments:
        writer.writerow([enrollment.id, enrollment.student_id, enrollment.course_id, enrollment.grade])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=enrollments.csv'})

@university_bp.route('/payments/export')
def export_payments():
    payments = TuitionPayment.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Student ID', 'Course ID', 'Amount Paid', 'Payment Date', 'Status'])
    for payment in payments:
        writer.writerow([payment.id, payment.student_id, payment.course_id, payment.amount_paid, payment.payment_date, payment.status])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=payments.csv'})

# Import forms
class ImportStudentForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import')

class ImportProfessorForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import')

class ImportCourseForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import')

class ImportEnrollmentForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import')

class ImportPaymentForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import')

# Import routes
@university_bp.route('/students/import', methods=['GET', 'POST'])
def import_students():
    form = ImportStudentForm()
    if form.validate_on_submit():
        file = form.file.data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                student = Student(id=row[0], name=row[1], email=row[2], major=row[3])
                db.session.add(student)
        db.session.commit()
        return redirect(url_for('university.students'))
    return render_template('import_students.html', form=form)

@university_bp.route('/professors/import', methods=['GET', 'POST'])
def import_professors():
    form = ImportProfessorForm()
    if form.validate_on_submit():
        file = form.file.data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                professor = Professor(id=row[0], name=row[1], email=row[2], department=row[3])
                db.session.add(professor)
        db.session.commit()
        return redirect(url_for('university.professors'))
    return render_template('import_professors.html', form=form)

@university_bp.route('/courses/import', methods=['GET', 'POST'])
def import_courses():
    form = ImportCourseForm()
    if form.validate_on_submit():
        file = form.file.data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 5:
                course = Course(id=int(row[0]), name=row[1], code=row[2], credits=int(row[3]), professor_id=row[4])
                db.session.add(course)
        db.session.commit()
        return redirect(url_for('university.courses'))
    return render_template('import_courses.html', form=form)

@university_bp.route('/enrollments/import', methods=['GET', 'POST'])
def import_enrollments():
    form = ImportEnrollmentForm()
    if form.validate_on_submit():
        file = form.file.data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                enrollment = Enrollment(id=int(row[0]), student_id=row[1], course_id=int(row[2]), grade=row[3] if row[3] else None)
                db.session.add(enrollment)
        db.session.commit()
        return redirect(url_for('university.enrollments'))
    return render_template('import_enrollments.html', form=form)

@university_bp.route('/payments/import', methods=['GET', 'POST'])
def import_payments():
    form = ImportPaymentForm()
    if form.validate_on_submit():
        file = form.file.data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 6:
                payment_date = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f') if row[4] else datetime.now()
                payment = TuitionPayment(id=int(row[0]), student_id=row[1], course_id=int(row[2]), amount_paid=float(row[3]), payment_date=payment_date, status=row[5])
                db.session.add(payment)
        db.session.commit()
        return redirect(url_for('university.payments'))
    return render_template('import_payments.html', form=form)

# Gallery routes
@university_bp.route('/gallery')
def gallery():
    campus_images = os.listdir('static/uploads/campus') if os.path.exists('static/uploads/campus') else []
    academic_images = os.listdir('static/uploads/academic') if os.path.exists('static/uploads/academic') else []
    student_images = os.listdir('static/uploads/student') if os.path.exists('static/uploads/student') else []
    return render_template('gallery.html', campus_images=campus_images, academic_images=academic_images, student_images=student_images)

@university_bp.route('/gallery/upload/<category>', methods=['POST'])
def upload_image(category):
    if 'file' not in request.files:
        return redirect(url_for('university.gallery'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('university.gallery'))
    if file:
        filename = file.filename
        file.save(os.path.join(f'static/uploads/{category}', filename))
    return redirect(url_for('university.gallery'))

@university_bp.route('/gallery/download/<category>/<filename>')
def download_image(category, filename):
    return send_from_directory(f'static/uploads/{category}', filename, as_attachment=True)