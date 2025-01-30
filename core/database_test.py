from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False # only for sqlite
}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30),nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean,default=True)
    is_verified = Column(Boolean,default=False)
    
    
    def __repr__(self):
        return f"User(id={self.id},first_name={self.first_name},last_name={self.last_name})"


# to create tables and database
Base.metadata.create_all(engine)


session = SessionLocal()


# inserting data
# ali = User(first_name="ali",age=31)
# session.add(ali)
# session.commit()

# bulk insert
# maryam = User(first_name="maryam",age=27)
# arousha = User(first_name="arousha",age=6)
# users = [maryam,arousha]
# session.add_all(users)
# session.commit()

# retrieve all data
# users = session.query(User).all()
# print(users)

# retrieve data with filter
user = session.query(User).filter_by(first_name="ali",age=31).first()


# updating a record of data
# user.last_name = "bigdeli"
# session.commit()

if user:
    session.delete(user)
    session.commit()







