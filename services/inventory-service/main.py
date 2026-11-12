import os, time, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pymysql


app = FastAPI(title="inventory-service")
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
def health(): return {"status":"ok","service":"inventory-service"}

class StockIn(BaseModel):
    stock: int = Field(ge=0)


@app.get("/inventory/{pid}")
def stock(pid:int):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("SELECT id,name,stock FROM products WHERE id=%s",(pid,)); r=x.fetchone()
        if not r: raise HTTPException(404,"Product not found")
        return r
    finally: c.close()

@app.patch("/inventory/{pid}")
def update_stock(pid:int,p:StockIn):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("UPDATE products SET stock=%s WHERE id=%s",(p.stock,pid))
            if not x.rowcount: raise HTTPException(404,"Product not found")
        return {"product_id":pid,"stock":p.stock}
    finally: c.close()

