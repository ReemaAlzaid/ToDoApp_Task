# ToDoApp Backend

ToDo Application with user authentication.

## Backend
- Framework - FastAPI
- DB - PostgreSQL, SQLAlchemy
- Secruity - Oauth2
- Create PDF - fpdf2

## Start
- pip install -r requirements.txt
- uvicorn main:app
- test the apis in postman with the avaliable collection 'ToDoApp.postman_collection.json'

Project structure
-----------------
Files related to application are in the ``app`` directory.
Application parts are:
```text
app
├── curds
│   ├── todoitem.py
│   ├── todolist.py
│   └── user.py
├── models
│   ├── todoitem.py
│   ├── todolist.py
│   └── user.py
├── routes
│   ├── todoitem.py
│   ├── todolist.py
│   └── user.py
├── schemas
│   ├── todoitem.py
│   ├── todolist.py
│   └── user.py
├── services
│   ├── auth.py
│   └── pdf.py
├── static
│   └── ToDoList.pdf
├── .env
├── database.py
├── main.py
└── router.py
