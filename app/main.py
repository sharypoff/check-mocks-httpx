import httpx
from fastapi import FastAPI

app = FastAPI()
client = httpx.AsyncClient()


@app.post("/")
async def root():
    result1 = await client.request(
        "POST",
        "http://example.com/user",
        json={"name": "John", "age": 21},
    )
    user_json = result1.json()
    result2 = await client.request(
        "POST",
        "http://example1.com/group/23",
        json={"user_id": user_json["id"]},
    )
    group_json = result2.json()
    return {"user": user_json, "group": group_json}
