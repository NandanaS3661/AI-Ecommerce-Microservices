import os, re
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
app=FastAPI(title="AI Assistant Service")
mongo=MongoClient(os.getenv("MONGO_URL","mongodb://mongodb:27017"))
collection=mongo[os.getenv("MONGO_DATABASE","ecommerce_ai")]["knowledge"]
class DocumentIn(BaseModel):
    title:str
    content:str
class ChatIn(BaseModel):
    user_id:str="guest"
    message:str
@app.get("/health")
def health(): return {"status":"ok","service":"ai-service"}
@app.post("/documents")
def add_document(p:DocumentIn):
    r=collection.insert_one({"kind":"document","title":p.title,"content":p.content})
    return {"id":str(r.inserted_id),"title":p.title}
@app.get("/documents")
def documents():
    return [{"id":str(d["_id"]),"title":d["title"]} for d in collection.find({"kind":"document"})]
@app.post("/chat")
def chat(p:ChatIn):
    terms=set(re.findall(r"[a-z0-9]+",p.message.lower()))
    matches=[]
    for d in collection.find({"kind":"document"}):
        words=set(re.findall(r"[a-z0-9]+",(d.get("content","")+" "+d.get("title","")).lower()))
        score=len(terms & words)
        if score: matches.append((score,d))
    matches.sort(key=lambda a:a[0],reverse=True)
    if matches:
        answer=f'From "{matches[0][1]["title"]}": {matches[0][1]["content"][:700]}'
        source=matches[0][1]["title"]
    else:
        answer="I am the store assistant. Ask about products or upload store/product documents so I can retrieve relevant information."
        source=None
    collection.insert_one({"kind":"chat","user_id":p.user_id,"message":p.message,"answer":answer})
    return {"answer":answer,"source":source,"mode":"document retrieval baseline"}
@app.get("/chat/history/{user_id}")
def history(user_id:str):
    return [{"message":d["message"],"answer":d["answer"]} for d in collection.find({"kind":"chat","user_id":user_id}).sort("_id",-1).limit(20)]
