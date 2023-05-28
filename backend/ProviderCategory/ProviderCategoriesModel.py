from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from Providers.ProviderModel import Providers
from Students.StudentModel import Students

from base import Base

class ProviderCategories(Base):
    __tablename__ = "provider_categories"
    category_id = Column("category_id",Integer,primary_key =True,autoincrement=True)
    student_id = Column("student_id",Integer,ForeignKey(Students.student_id),nullable=False)
    main_categories = Column("main_categories",String(255),nullable=False)
    sub_categories = Column("sub_categories",String(255),nullable=False)