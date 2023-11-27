from sqlalchemy import  Column, Integer, String, ForeignKey 
from database import Base

class ToDoItem(Base):
    __tablename__ ="todo_item" 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status= Column(String)
    order= Column(Integer)
    todolist_id=Column(Integer, ForeignKey("todo_list.id"))