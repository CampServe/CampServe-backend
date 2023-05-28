from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from Students.StudentModel import Students

from base import Base

class Providers(Base):
    __tablename__ = "providers"
    provider_id = Column("provider_id",Integer, primary_key=True, autoincrement=True)
    student_id = Column("student_id",Integer, ForeignKey(Students.student_id), nullable=False)
    profile_pic = Column("profile_pic",String(255), nullable=True, default=None)
    banner_image = Column("banner_image",String(255), nullable=True, default=None)
    provider_contact = Column("provider_contact",String(255), nullable=True, default=None)
    business_name = Column("business_name",String(255), nullable=True, default=None)
    bio = Column("bio",String(255), nullable=True, default=None)


# Relationships
ratings = relationship("Ratings", uselist=False, back_populates="provider")
product = relationship("Product", uselist=False, back_populates="provider")
