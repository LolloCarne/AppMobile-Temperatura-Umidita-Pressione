from fastapi import FastAPI, HTTPException, status
from fastapi.param_functions import Path
from pydantic import BaseModel
from typing import Optional
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Session


SQLALCHEMY_DATABASE_URL = "sqlite:///root:banana.33@localhost:3306/iot"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Dato(Base):
    __tablename__ = "dati"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    temperatura = Column(String(10))
    umidità = Column(String(20))
    pressione = Column(String(10))
    tempo=Column(DateTime)

app= FastAPI()
inventory= {}

class Item(BaseModel):
    temp: str
    press: str
    hum: str
#endpoit, root "/hello"


@app.get("/",response_model=Item)
def home(*,name:Optional[str]=None,test:int):
    return {"Data":"Testing"}

@app.get("/about")
def about():
    return {"data":"About"}

@app.post("/")
def create_item(db:Session, item_id:int, item:Item):
    if item_id in inventory:
        raise HTTPException(status_code=404, detail="item id already exist")
    #inventory[item_id]={"name":item.name,"brand":item.brand,"price":item.price}  
    inventory[item_id]=item
    now=datetime.datetime.now()
    db_dato=Dato(id=item_id,temperatura=item.temp,umiditià=item.hum,pressione=item.press,tempo=now)
    db.add(db_dato)
    db.commit()
    db.refresh(db_dato)
    return db_dato


    return item.press