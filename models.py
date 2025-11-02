from database import db
from sqlalchemy import event

def generate_student_id(mapper, connection, target):
    if not target.id:
        last_student = connection.execute(
            db.select(Student.id).order_by(Student.id.desc()).limit(1)
        ).scalar()
        if last_student:
            num = int(last_student[1:]) + 1
        else:
            num = 1
        target.id = f"s{num:04d}"

def generate_professor_id(mapper, connection, target):
    if not target.id:
        last_professor = connection.execute(
            db.select(Professor.id).order_by(Professor.id.desc()).limit(1)
        ).scalar()
        if last_professor:
            num = int(last_professor[1:]) + 1
        else:
            num = 1
        target.id = f"i{num:04d}"

class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Professor(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', backref='professor', lazy=True)

# Register event listeners
event.listen(Student, 'before_insert', generate_student_id)
event.listen(Professor, 'before_insert', generate_professor_id)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=3)
    professor_id = db.Column(db.String(10), db.ForeignKey('professor.id'), nullable=False)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.String(2), nullable=True)

class TuitionPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(20), nullable=False, default='paid')  # paid, pending, overdue

    student = db.relationship('Student', backref='payments')
    course = db.relationship('Course', backref='payments')