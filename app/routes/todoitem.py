from typing import Annotated
from curds.todoitem import getOrder,countItems
from schemas.todoitem import ItemAdd,Status,Title,Order
from models.todoitem import ToDoItem
from models.todolist import ToDoList
from curds.todolist import getListId
from services.auth import validateUser
from database import Base, engine, SessionLocal,db_dependency
from fastapi import APIRouter, Depends, HTTPException, Request, Response,status

user_dependency = Annotated[dict,Depends(validateUser)]

router = APIRouter(
    prefix='/item',
    tags=['item']
)
@router.post("/")
async def create_todoItem(db:db_dependency,item:ItemAdd,user_token:user_dependency,response: Response):
    try:
        todolist_id = db.query(ToDoList).filter(ToDoList.owner_id == user_token.get("id")).first()
        orderNumber = getOrder(db,todolist_id.id)
        todoItem = ToDoItem(title=item.title,status="Not Done",order=orderNumber+1,todolist_id=todolist_id.id)
        db.add(todoItem)
        db.commit()
        db.refresh(todoItem)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return
    response.status_code = status.HTTP_201_CREATED
    return
    

@router.delete("/{todoitem_id}")
async def delete_todoItem(db:db_dependency,user_token:user_dependency,todoitem_id:int,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        todo_item=db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).filter(todoitem_id == ToDoItem.id).first()
        if todo_item is not None:
            db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).filter(todoitem_id == ToDoItem.id).delete()
            db.commit()
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"The entered to do id in not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return

@router.put("/{todoitem_id}/title")
async def modifyTitle(db:db_dependency,title:Title,todoitem_id:int,user_token:user_dependency,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        print(List_id)
        todoItem = db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).filter(todoitem_id == ToDoItem.id)
        print(todoItem.first().title)
        if todoItem.first() is not None:
            todoItem.first().title = title.title
            db.commit()
            response.status_code = status.HTTP_200_OK
            return todoItem.all()
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"The entered to do id in not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return
    
@router.put("/{todoitem_id}/status")
async def modifyStatus(db:db_dependency,statusReq:Status,todoitem_id:int,user_token:user_dependency,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        todoItem = db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).filter(todoitem_id == ToDoItem.id)
        print(todoItem.first().status)
        if todoItem.first() is not None:
            todoItem.first().status = statusReq.status
            db.commit()
            response.status_code = status.HTTP_200_OK
            return todoItem.all()
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"The entered to do id in not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return
    
@router.put("/{todoitem_id}/order")
async def modifyOrder(db:db_dependency,order:Order,todoitem_id:int,user_token:user_dependency,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        ItemCount= countItems(db,List_id)
        print(order)
        print(ItemCount)
        if ItemCount < order.order:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message":"The order exceeds the count of todos"}

        todoItemModify = db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).filter(todoitem_id == ToDoItem.id)
        todoItemReplace= db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).filter(order.order == ToDoItem.order)
        if todoItemModify.first() is not None:
            todoItemReplace.first().order=todoItemModify.first().order
            todoItemModify.first().order = order.order
            db.commit()
            response.status_code = status.HTTP_200_OK
            return todoItemModify.all()
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"The entered to do id in not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return