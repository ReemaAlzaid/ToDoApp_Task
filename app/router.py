from fastapi import APIRouter
from routes import todoitem
from routes import todolist
from routes import user

router = APIRouter()

router.include_router(todoitem.router)
router.include_router(todolist.router)
router.include_router(user.router)