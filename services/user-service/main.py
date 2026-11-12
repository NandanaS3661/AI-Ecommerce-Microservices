import os, time, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pymysql


app = FastAPI(title="user-service")
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
def health(): return {"status":"ok","service":"user-service"}

class UserIn(BaseModel):
    name: str
    email: str


@app.post("/users")
def create_user(p: UserIn):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("INSERT INTO users(name,email) VALUES(%s,%s)",(p.name,p.email))
            return {"id":x.lastrowid,"name":p.name,"email":p.email}
    except pymysql.err.IntegrityError: raise HTTPException(409,"Email already exists")
    finally: c.close()

@app.get("/users/{uid}")
def get_user(uid:int):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("SELECT id,name,email FROM users WHERE id=%s",(uid,)); r=x.fetchone()
        if not r: raise HTTPException(404,"User not found")
        return r
    finally: c.close()

