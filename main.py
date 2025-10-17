#Python 3.9 version
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional  # 用於可為 None 的欄位

app = FastAPI()

# -----------------------
# Pydantic 模型
# -----------------------
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# -----------------------
# 假資料庫
# -----------------------
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# -----------------------
# API 路由
# -----------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/item/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict  

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    # 先把 item 轉成字典
    result = {"item_id": item_id, **item.dict()}
    
    # 計算 price_with_tax，如果有 tax
    if item.tax is not None:
        result["price_with_tax"] = item.price + item.tax
    
    # 如果有 q 參數，也加入結果
    if q:
        result.update({"q": q})
    
    return result



