from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship


from base import Base


class Students(Base):
    __tablename__ = "students"
    student_id = Column("student_id",Integer,primary_key = True,nullable= False)
    first_name = Column("first_name",String(255),nullable=False)
    last_name = Column("last_name",String(255),nullable=False)
    username = Column("username",String(255),nullable=False)
    ref_number = Column("ref_number",String(255),nullable=False)
    password = Column("password",String(255), nullable = False)

#relationships
transactions = relationship("transactions",uselist = False,back_populates="transactions")
ratings = relationship("ratings", uselist=False,back_populates = "ratings")
provider = relationship("providers",uselist=False,back_populates="providers")
provider_categories = relationship("provider_categories", back_populates = "provider_categories")