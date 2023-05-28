from sqlalchemy import String, Integer, Date, ForeignKey, Column
from sqlalchemy.orm import relationship


from base import Base


class Transactions(Base):
    __tablename__ ="transactions"
    transaction_id = Column("transaction_id",Integer, primarykey=True,nullable=False)
    student_id = Column("student_id",Integer,ForeignKey=True,nullable=False)
    description = Column("description",String(255),nullable=False)
    amount = Column("amount",Integer,nullable = False)
    date_completed = Column("date_completed",Date)