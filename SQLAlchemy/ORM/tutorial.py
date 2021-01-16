from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

# engine = create_engine("sqlite:///database.sqlite", echo=True)
engine = create_engine("sqlite:///database.sqlite")
Session = sessionmaker(bind=engine)
commit = 0

# Base catalogs all tables (object factory for new tables)
Base = declarative_base()


class User(Base):
    """
    Set up table
    """

    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=False)

    def __repr__(self) -> tuple:
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.fullname,
            self.nickname,
        )


# Create all tables and generate database if not yet exist
Base.metadata.create_all(engine)


ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")

print(ed_user.name)
print(ed_user.fullname)
print(ed_user.nickname)
print(ed_user.uid)  # Primary Key increment doesn't work without INSERT

# SESSION (responsible for communicating with the database)

session = Session()
session.add(ed_user)

# Querying the database flushes new objects first before the query
our_user = session.query(User).filter_by(name="ed").first()
print(our_user.fullname)
print("")
# The object queried is the same that was added into the session
print(ed_user is our_user)

session.add_all(
    [
        User(name="wendy", fullname="Wendy Williams", nickname="windy"),
        User(name="mary", fullname="Mary Contrary", nickname="mary"),
        User(name="fred", fullname="Fred Flintstone", nickname="freddy"),
    ]
)

# Session is paying attention. It detects modifications made to the object that was flushed. Changes are tracked in the dirty property.
ed_user.nickname = "eddie"
print("")
print(session.dirty)
print("")
# Pending objects are the ones added but not flushed.
print(session.new)
print("")
# The flush method writes out SQL statements for the objects added in the session and modifications made to them.
# session.flush()
# Commit the changes from the transaction
# session.commit()

query = session.query(User).filter_by(uid=3).first()
print(query.name)
print("")
# After flushing, ed_user is not the sames object
print(ed_user is our_user)
print("")
# ed_user has a primary_key now
print(ed_user.uid)

session.add_all(
    [
        User(name="joelma", fullname="Joelma Calipso", nickname="jojo"),
        User(name="lucas", fullname="Lucas Oliveira", nickname="lucao"),
        User(name="pedro", fullname="Pedro Brito", nickname="pedrinho"),
        User(name="megumi", fullname="Fushigoro Megumi", nickname="mimi"),
    ]
)
if commit == 1:
    session.commit()

ed_user.name = "Edwardo"

fake_user = User(name="fakeuser", fullname="Invalid", nickname="12345")
session.add(fake_user)

print("")
query = session.query(User).filter(User.name.in_(["Edwardo", "fakeuser"]))
print(query.all())
print("")
for instance in query:
    print(instance)

# Rollback all flushed changes
session.rollback()
query = session.query(User).filter(User.name.in_(["ed", "fakeuser"]))
print("")
print(query.count())
print(query[0])

# Querying from database
print("")
query = session.query(User.name, User.fullname, User.uid)
print(query.all())

print("")
for instance in session.query(User):
    print(instance.uid, instance.name, instance.fullname, instance.nickname)


# Basic operations with Query include issuing LIMIT and OFFSET, most conveniently using Python array slices and typically in conjunction with ORDER BY:
print("")
for name, fullname in session.query(User.name, User.fullname)[::2]:
    print(name, fullname)


# filtering results, which is accomplished either with filter_by(), which uses keyword arguments
print("")
for (name,) in session.query(User.name).filter_by(fullname="Fushigoro Megumi"):
    print(name)

# or filter(), which uses more flexible SQL expression language constructs. These allow you to use regular Python operators with the class-level attributes on your mapped class:
print("")
for user in session.query(User).filter(User.fullname == "Fushigoro Megumi"):
    print(user.nickname)


# The Query object is fully generative, meaning that most method calls return a new Query object upon which further criteria may be added.
# For example, to query for users named “ed” with a full name of “Ed Jones”, you can call filter() twice, which joins criteria using AND:
print("")
for user in (
    session.query(User)
    .filter(User.name == "mary")
    .filter(User.fullname == "Mary Contrary")
):
    print(user.nickname)

# REGEX
print("")
query = session.query(User.fullname).filter(User.name.like("%ed")).order_by(User.uid)
for (instance,) in query:
    print(instance)

print("")
query = session.query(User).filter(User.name.like("ed")).one()
print(query.fullname)

# RELATIONSHIPS


class Address(Base):
    __tablename__ = "addresses"

    uid = Column(Integer, primary_key=True)
    email_address = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.uid"))

    # Address.user.relationship() uses the foreign key relationships between the two tables to determine the nature of this linkage, determining that Address.user will be many to one.
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship("Address", order_by=Address.uid, back_populates="user")
Base.metadata.create_all(engine)

# Adding new user with email addresses
jack = User(name="jack", fullname="Jack Bean", nickname="gjffdd")
jack.addresses = [
    Address(email_address="jack@google.com"),
    Address(email_address="j25@yahoo.com"),
]
session.add(jack)
print("")

# Addind email addresses to existing user
print("")
user = session.query(User).filter(User.name == "ed").one()
print(user)
user.addresses.extend(
    [
        Address(email_address="eddie@google.com"),
        Address(email_address="edward@yahoo.com"),
    ]
)

print(user.addresses)
print("")
print(user.fullname)
print("")

addresses = session.query(Address)
print(addresses[0].user)

if commit == 1:
    session.commit()

print("")
for u, a in (
    session.query(User, Address)
    .filter(User.uid == Address.user_id)
    .filter(Address.email_address == "jack@google.com")
    .all()
):
    print(u)
    print(a)
