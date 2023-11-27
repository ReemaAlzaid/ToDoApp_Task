from typing import Annotated
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.pdf import create_pdf
from curds.user import getEmail
from schemas.todolist import ShareId
from curds.todoitem import getOrder
from schemas.todoitem import ItemAdd,Status,Title,Order
from models.todoitem import ToDoItem
from models.todolist import ToDoList
from curds.todolist import getListId,getShareListId,getOwnerId
from services.auth import validateUser
from database import db_dependency
from fastapi import APIRouter, Depends, HTTPException, Request, Response,status
import pdfkit
user_dependency = Annotated[dict,Depends(validateUser)]

router = APIRouter(
    prefix='/list',
    tags=['list']
)

@router.get("/")
async def getList(db:db_dependency,user_token:user_dependency,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        todo_item=db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).order_by(ToDoItem.order.asc())
        if todo_item.first() is not None:
            response.status_code = status.HTTP_200_OK
            return todo_item.all()
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"You don't have any to do items yet"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return
    
@router.put("/share")
async def modifyShareList(db:db_dependency,sharewith_id:ShareId,user_token:user_dependency,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        print(List_id)
        todoList = db.query(ToDoList).filter(List_id == ToDoList.id)
        print(todoList.first().sharewith_id)
        if todoList.first() is not None:
            todoList.first().sharewith_id = sharewith_id.sharewith_id
            db.commit()
            response.status_code = status.HTTP_200_OK
            return todoList.all()
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"List not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return


@router.get("/doc")
async def getListPDF(db:db_dependency,user_token:user_dependency,response: Response):
    try:
        List_id= getListId(db,user_token.get("id"))
        print(List_id)
        todo_item=db.query(ToDoItem).where(List_id == ToDoItem.todolist_id).order_by(ToDoItem.order.asc())
        if todo_item.first() is not None:
            response.status_code = status.HTTP_200_OK
            owner_id = getOwnerId(db,List_id)
            owner_email = getEmail(db,owner_id)
            await create_pdf("ToDoList",todo_item.all(),owner_email)
            headers = {"Content-Disposition": "inline; filename=ToDoList.pdf"}  
            response = FileResponse(".\\static\\ToDoList.pdf", media_type="application/pdf", headers=headers)
            return response

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"You don't have any to do items yet"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return

@router.get("/{idList}")
async def getListbyID(db:db_dependency,idList:int,user_token:user_dependency,response: Response):
    try:
        sharewith_id = getShareListId(db,idList)
        if sharewith_id is not None:
            owner_id = getOwnerId(db,idList)
            owner_email = getEmail(db,owner_id)
            if sharewith_id == user_token.get("id"):
                todo_item=db.query(ToDoItem).where(idList == ToDoItem.todolist_id).order_by(ToDoItem.order.asc())
                if todo_item.first() is not None:
                    response.status_code = status.HTTP_200_OK
                    return {"Owner Email":owner_email,"ToDoItems":todo_item.all()}
                else:
                    response.status_code = status.HTTP_404_NOT_FOUND
                    return {"message":"This list doesn't have any todos yet"}
            else:
                response.status_code = status.HTTP_403_FORBIDDEN
                return {"message":"You don't have permission"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message":"No such list with this id"}
            
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print({"error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"})
        return