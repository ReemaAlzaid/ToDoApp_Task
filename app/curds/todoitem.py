from models.todoitem import ToDoItem
from database import Base, engine, SessionLocal,db_dependency
from models.todolist import ToDoList
from fastapi import APIRouter, Depends, HTTPException, Request, Response,status

def getOrder(db:db_dependency,id:int):
    checkCount = db.query(ToDoItem).filter(id == ToDoItem.todolist_id).count()
    if checkCount is not 0:
        return db.query(ToDoItem).filter(id == ToDoItem.todolist_id).order_by(ToDoItem.order.desc()).first().order
    else:
        return 0

def countItems(db:db_dependency,idList:int):
    return db.query(ToDoItem).filter(idList == ToDoItem.todolist_id).count()