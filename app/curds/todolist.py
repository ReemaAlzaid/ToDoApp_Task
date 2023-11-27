from database import Base, engine, SessionLocal,db_dependency
from models.todolist import ToDoList

def getListId(db:db_dependency,userid:int):
    return db.query(ToDoList).filter(ToDoList.owner_id==userid).first().id

def getShareListId(db:db_dependency,listId:int):
    return db.query(ToDoList).filter(ToDoList.id==listId).first().sharewith_id

def getOwnerId(db:db_dependency,listId:int):
    return db.query(ToDoList).filter(ToDoList.id==listId).first().owner_id