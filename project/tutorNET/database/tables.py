from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Text

from database.base_orm import Base


class Teacher(Base):
    __tablename__ = "teachers"

    # Basic user data
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(20), nullable=False)
    pwhash = Column(String(20), nullable=False)
    # Profile data
    name = Column(String(100), unique=True)
    phone = Column(String(20), unique=True)
    bio = Column(Text)
    photo = Column(String(50), unique=True)

    subjects = relationship(
        "Subject", back_populates="user", cascade="all, delete-orphan",
    )

    def __repr__(self):
        return "<Teacher(id='%s', name='%s')>" % (self.id, self.name)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("teachers.id"))
    subject = Column(String(20), nullable=False)

    user = relationship("Teacher", back_populates="subjects")
    schedules = relationship(
        "Schedule", back_populates="subject", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return "<Subject(subject='%s', user='%s')>" % (self.subject, self.user_id)


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    weekday = Column(String(10), nullable=False)
    time_from = Column(String(5), nullable=False)
    time_to = Column(String(5), nullable=False)

    subject = relationship("Subject", back_populates="schedules")

    def __repr__(self):
        return "<Schedule(subject='%s',weekday='%s', time_from=%s, time_to=%s)>" % (
            self.subject,
            self.weekday,
            self.time_from,
            self.time_to,
        )
