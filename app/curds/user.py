from database import db_dependency
from models.user import User

def getEmail(db:db_dependency,userId:int):
    return db.query(User).filter(User.id==userId).first().email