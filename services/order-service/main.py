import os, time, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pymysql


app = FastAPI(title="order-service")
def db():
    last = None
    for _ in range(30):
        try:
            return pymysql.connect(host=os.getenv("MYSQL_HOST","mysql"), user=os.getenv("MYSQL_USER","appuser"),
                password=os.getenv("MYSQL_PASSWORD","apppass"), database=os.getenv("MYSQL_DATABASE","ecommerce"),
                cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        except Exception as e:
            last=e
            time.sleep(2)
    raise HTTPException(503, f"MySQL unavailable: {last}")

@app.get("/health")
def health(): return {"status":"ok","service":"order-service"}

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0)


@app.post("/orders")
def add_order(p:OrderIn):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("INSERT INTO orders(user_id,product_id,quantity,status) VALUES(%s,%s,%s,'PLACED')",
                      (p.user_id,p.product_id,p.quantity))
            return {"id":x.lastrowid,**p.model_dump(),"status":"PLACED"}
    finally: c.close()

@app.get("/orders")
def orders(user_id:int|None=None):
    c=db()
    try:
        with c.cursor() as x:
            if user_id: x.execute("SELECT * FROM orders WHERE user_id=%s",(user_id,))
            else: x.execute("SELECT * FROM orders")
            return x.fetchall()
    finally: c.close()

