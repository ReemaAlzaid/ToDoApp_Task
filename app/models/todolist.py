from sqlalchemy import  Column, Integer, String, ForeignKey 
from database import Base

class ToDoList(Base):
    __tablename__ ="todo_list"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    sharewith_id = Column(Integer)