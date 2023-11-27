from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Status(str,Enum):
    Done = 'Done'
    NotDone = 'Not Done'

class ItemAdd(BaseModel):
    title: str

class Status(BaseModel):
    status: Status

class Title(BaseModel):
    title: str

class Order(BaseModel):
    order: int

class Item(BaseModel):
    title: str
    status: Status
    order : int