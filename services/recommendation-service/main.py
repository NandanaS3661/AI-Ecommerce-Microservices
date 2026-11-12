import os, time, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pymysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="recommendation-service")
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
def health(): return {"status":"ok","service":"recommendation-service"}

class RecommendIn(BaseModel):
    product_id: int


@app.post("/recommend")
def recommend(p:RecommendIn):
    c=db()
    try:
        with c.cursor() as x:
            x.execute("SELECT id,name,category,description,price,stock FROM products")
            rows=x.fetchall()
    finally: c.close()
    ids=[r["id"] for r in rows]
    if p.product_id not in ids: raise HTTPException(404,"Product not found")
    if len(rows)<2: return {"method":"TF-IDF","recommendations":[]}
    corpus=[f'{r["name"]} {r["category"]} {r["description"]}' for r in rows]
    matrix=TfidfVectorizer(stop_words="english").fit_transform(corpus)
    i=ids.index(p.product_id); scores=cosine_similarity(matrix[i],matrix).flatten()
    ranked=sorted([(float(scores[j]),rows[j]) for j in range(len(rows)) if j!=i],key=lambda z:z[0],reverse=True)
    return {"method":"TF-IDF cosine similarity","recommendations":[{**r,"similarity":round(s,3)} for s,r in ranked[:5]]}

