from sqlalchemy import String, Integer, Column



from base import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column("user_id",Integer, primary_key =True, nullable = False)
    first_name = Column("first_name",String(255),nullable=False)
    last_name = Column("last_name",String(255),nullable=False)
    username = Column("username",String(255),nullable=False)
    password = Column("password",String(255),nullable=False)
    email = Column("email",String(255),nullable=False)
