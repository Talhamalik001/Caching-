    # """
    # caching strategies:
    # 1. Cache Aside (Lazy Loading)
    # Simple
    # Flexible
    # Easy to control
    # Framework independent
    # Scalable
    # Redis ke saath perfect
    # widely used

    # flow : Check Cache → 
    # If Miss → 
    # Get from DB → 
    # Save in Cache
    # """

import redis
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, but you can restrict to specific domains if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis Connection (Define the Redis client `r` globally)
r = redis.Redis(host="localhost", port=6379, db=0)
print("Redis connected:", r.ping())

# Serve Static Files (JavaScript, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve index.html at the root URL
@app.get("/", response_class=HTMLResponse)
async def get_index():
    # Make sure index.html exists in your current directory
    with open(os.path.join(os.path.dirname(__file__), "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Fake Database Fetch Function
def fetch_user_from_db(user_id: int):
    print("DB fetch for user:", user_id)
    return {"id": user_id, "name": f"User{user_id}"}

# API Route to Get User from Redis Cache
@app.get("/user/redis/{user_id}")
def get_user(user_id: int):
    # Try to get cached user data from Redis
    cached = r.get(f"user:{user_id}")
    
    # If cached data exists, return it
    if cached:
        print("Cache HIT:", user_id)
        return {"data": json.loads(cached), "source": "cache"}

    # If no cached data, fetch from DB, set to cache and return
    print("Cache MISS:", user_id)
    user = fetch_user_from_db(user_id)
    r.set(f"user:{user_id}", json.dumps(user), ex=60)  # TTL = 60 sec for cache

    return {"data": user, "source": "db"}
