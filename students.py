"""Simple database test by gabr0."""
from peewee import *


db = SqliteDatabase('students.db')


class Student(Model):
    """Student model."""

    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)

    class Meta:
        """Meta class."""

        database = db


students = [{
    'username': 'Gabriel',
    'points': 4888
}, {
    "username": 'oshetuto',
    'points': 14000
}, {
    "username": 'Dr.Rabo',
    "points": 4
}, {
    "username": 'Dabladex',
    'points': 1
}
]


def add_students():
    """Add the students to the db."""
    for student in students:
        try:
            Student.create(username=student['username'],
                           points=student['points'])
        except IntegrityError:
            student_record = Student.get(username=student['username'])
            student_record.points = student['points']
            student_record.save()


def get_master():
    student = Student.select().order_by(Student.points.desc()).get()
    return student


if __name__ == '__main__':
    db.connect()
    db.create_tables([Student], safe=True)
    add_students()
    print("El master del universe es: {0.username}".format(get_master()))
