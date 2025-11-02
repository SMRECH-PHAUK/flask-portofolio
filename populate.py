from app import app, db
from models import Student, Professor, Course, Enrollment, TuitionPayment
from datetime import datetime

def populate_database():
    with app.app_context():
        # Create sample professors
        prof1 = Professor(id="i0001", name="Dr. John Smith", email="john.smith@university.edu", department="Computer Science")
        prof2 = Professor(id="i0002", name="Dr. Jane Doe", email="jane.doe@university.edu", department="Mathematics")
        prof3 = Professor(id="i0003", name="Dr. Bob Johnson", email="bob.johnson@university.edu", department="Physics")

        db.session.add_all([prof1, prof2, prof3])
        db.session.commit()

        # Create sample students
        student1 = Student(id="s0001", name="Alice Wilson", email="alice.wilson@student.edu", major="Computer Science")
        student2 = Student(id="s0002", name="Charlie Brown", email="charlie.brown@student.edu", major="Mathematics")
        student3 = Student(id="s0003", name="Diana Prince", email="diana.prince@student.edu", major="Physics")
        student4 = Student(id="s0004", name="Eve Adams", email="eve.adams@student.edu", major="Computer Science")

        db.session.add_all([student1, student2, student3, student4])
        db.session.commit()

        # Create sample courses
        course1 = Course(name="Introduction to Programming", code="CS101", credits=3, professor_id=prof1.id)
        course2 = Course(name="Calculus I", code="MATH101", credits=4, professor_id=prof2.id)
        course3 = Course(name="Physics Fundamentals", code="PHYS101", credits=3, professor_id=prof3.id)
        course4 = Course(name="Data Structures", code="CS201", credits=3, professor_id=prof1.id)
        course5 = Course(name="Linear Algebra", code="MATH201", credits=3, professor_id=prof2.id)

        db.session.add_all([course1, course2, course3, course4, course5])
        db.session.commit()

        # Create sample enrollments
        enrollment1 = Enrollment(student_id=student1.id, course_id=course1.id, grade="A")
        enrollment2 = Enrollment(student_id=student1.id, course_id=course4.id, grade="B+")
        enrollment3 = Enrollment(student_id=student2.id, course_id=course2.id, grade="A-")
        enrollment4 = Enrollment(student_id=student2.id, course_id=course5.id, grade="B")
        enrollment5 = Enrollment(student_id=student3.id, course_id=course3.id, grade="A")
        enrollment6 = Enrollment(student_id=student4.id, course_id=course1.id, grade="B")
        enrollment7 = Enrollment(student_id=student4.id, course_id=course4.id, grade="A-")

        db.session.add_all([enrollment1, enrollment2, enrollment3, enrollment4, enrollment5, enrollment6, enrollment7])
        db.session.commit()

        # Create sample tuition payments ($20 per credit)
        payment1 = TuitionPayment(student_id=student1.id, course_id=course1.id, amount_paid=60.0, status='paid')  # 3 credits * $20
        payment2 = TuitionPayment(student_id=student1.id, course_id=course4.id, amount_paid=60.0, status='paid')  # 3 credits * $20
        payment3 = TuitionPayment(student_id=student2.id, course_id=course2.id, amount_paid=80.0, status='paid')  # 4 credits * $20
        payment4 = TuitionPayment(student_id=student2.id, course_id=course5.id, amount_paid=60.0, status='pending')  # 3 credits * $20
        payment5 = TuitionPayment(student_id=student3.id, course_id=course3.id, amount_paid=60.0, status='paid')  # 3 credits * $20
        payment6 = TuitionPayment(student_id=student4.id, course_id=course1.id, amount_paid=60.0, status='overdue')  # 3 credits * $20
        payment7 = TuitionPayment(student_id=student4.id, course_id=course4.id, amount_paid=60.0, status='paid')  # 3 credits * $20

        db.session.add_all([payment1, payment2, payment3, payment4, payment5, payment6, payment7])
        db.session.commit()

        print("Database populated with sample data!")

if __name__ == "__main__":
    populate_database()