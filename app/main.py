import services.auth
from fastapi import FastAPI
from router import router as api_router
import models.todoitem as todoitem
import models.user as User
import models.todolist as ToDoList
from database import Base, engine, SessionLocal

todoitem.Base.metadata.create_all(engine)
User.Base.metadata.create_all(engine)
ToDoList.Base.metadata.create_all(engine)


def create_app() -> FastAPI:

    application = FastAPI()

    application.include_router(api_router, prefix="/api/v1")
    
    return application


app = create_app()