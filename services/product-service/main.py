import os, time, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pymysql


app = FastAPI(title="product-service")
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
def health(): return {"status":"ok","service":"product-service"}

class ProductIn(BaseModel):
    name: str
    category: str
    description: str = ""
    price: float = Field(gt=0)
    stock: int = Field(ge=0,default=0)


@app.post("/products")
def add_product(p:ProductIn):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("INSERT INTO products(name,category,description,price,stock) VALUES(%s,%s,%s,%s,%s)",
                      (p.name,p.category,p.description,p.price,p.stock))
            return {"id":x.lastrowid,**p.model_dump()}
    finally: c.close()

@app.get("/products")
def products(q:str|None=None):
    c=db()
    try:
        with c.cursor() as x:
            if q:
                x.execute("SELECT * FROM products WHERE name LIKE %s OR category LIKE %s OR description LIKE %s",
                          (f"%{q}%",f"%{q}%",f"%{q}%"))
            else: x.execute("SELECT * FROM products ORDER BY id")
            return x.fetchall()
    finally: c.close()

@app.get("/products/{pid}")
def product(pid:int):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("SELECT * FROM products WHERE id=%s",(pid,)); r=x.fetchone()
        if not r: raise HTTPException(404,"Product not found")
        return r
    finally: c.close()

