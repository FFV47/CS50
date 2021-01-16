from database.base_orm import db_session, init_db
from database.tables import Teacher, Subject, Schedule

# teacher = Teacher.query.filter(Teacher.id == 1).first()
# subjects = teacher.subjects

# print(teacher)
# print("")
# print(teacher.user)
# print("")
# print(subjects)
# print("")

# for subject in subjects:
#     print(subject)
#     for schedule in subject.schedules:
#         print(schedule)
#     print("")

print("")

teachers = Teacher.query.join(Subject).filter(Subject.subject == "Earth Sciences").all()
print(teachers)
print("")

teachers = (
    Teacher.query.join(Subject)
    .join(Schedule)
    .filter(Schedule.weekday == "Monday", Subject.subject == "Biology")
    .all()
)
print(teachers)
