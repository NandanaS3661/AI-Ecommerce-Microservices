import os
import httpx
from fastapi import FastAPI, Request, HTTPException
app=FastAPI(title="E-Commerce API Gateway")
targets={"users":os.getenv("USER_URL","http://user-service:8001"),
"products":os.getenv("PRODUCT_URL","http://product-service:8002"),
"orders":os.getenv("ORDER_URL","http://order-service:8003"),
"inventory":os.getenv("INVENTORY_URL","http://inventory-service:8004"),
"recommendations":os.getenv("RECOMMEND_URL","http://recommendation-service:8005"),
"ai":os.getenv("AI_URL","http://ai-service:8006")}
@app.get("/health")
def health(): return {"status":"ok"}
@app.api_route("/{service}/{path:path}",methods=["GET","POST","PATCH","PUT","DELETE"])
@app.api_route("/{service}",methods=["GET","POST","PATCH","PUT","DELETE"])
async def proxy(service:str,request:Request,path:str=""):
    if service not in targets: raise HTTPException(404,"Unknown service")
    url=targets[service]+("/"+path if path else "")
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.request(request.method,url,params=request.query_params,content=await request.body(),
            headers={"content-type":request.headers.get("content-type","application/json")})
    try: data=r.json()
    except Exception: data={"detail":r.text}
    if r.status_code>=400: raise HTTPException(r.status_code,data)
    return data
