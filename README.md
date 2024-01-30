# ToDoApp Backend

ToDo Application with user authentication.

## Backend
- Framework - FastAPI
- DB - PostgreSQL, SQLAlchemy
- Security - Oauth2
- Create PDF - fpdf2

## Start
- pip install -r requirements.txt
- uvicorn main:app
- test the APIs in Postman with the available collection 'ToDoApp.postman_collection.json'

## Functional requirements 
- Register: - The user can register by email and create a username and 
password to use the app, the email, user name, and password 
will be marked as required in the user registration form.
- Login: - The user can log in to his To-Do app using the username and 
password he created.
- Add: - The user can add new tasks, and they will appear in a numbered list
as per the addition time oldest will be first.
- Modify: - The user can edit any of his existing tasks, tasks shall stay in 
the same order after modification.
- Delete: - The user can delete any of his tasks.
- Reorder (prioritize): The user can change the order of his tasks.
- Task Status: - the user shall be allowed to change the status of the 
task and mark it as done.
- Share: - The user can share his updated tasks list with any app user by 
using his email, the shared task list will appear on the other user 
app page with the name of the owner on the top of the list.
- Stop sharing: - The user can cancel sharing his task list.

## Non-functional requirements: -
- Performance: app processes do not take a long time to execute, especially registration and user login. 
- Security: The app is secured and no one can use the app without logging in.
- The user can export their tasks list as a PDF.


Project structure
-----------------
Files related to the application are in the ``app`` directory.
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
