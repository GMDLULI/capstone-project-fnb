import hashlib
import hmac
import json
import os
from pathlib import Path
import threading
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Resource Finder API", 
    description="A Small JSON file serving local events communities",
    version="1.0.0")

DATA_FILE = Path(__file__).parent / "data" / "resource.json"
USERS_FILE = Path(__file__).parent / "data" / "users.json"
_users_lock = threading.Lock()


def load_users() -> dict:
    try:
        text = USERS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    if not text.strip():
        return {}
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("users.json must contain a JSON object")
    return data

def save_users() -> None:
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = USERS_FILE.with_suffix(".json.tmp")
    tmp_file.write_text(json.dumps(USERS, indent=2), encoding="utf-8")
    os.replace(tmp_file, USERS_FILE)

def load_resources() -> list[dict]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


RESOURCES = load_resources()


@app.get("/")
def root():
    return {
        "name": "Resource Finder API",
        "docs": "/docs",
        "message": "Resource Finder API is running. See /docs",
        'endpoints': {
            '/resources': 'List all resources, with optional query parameters for filtering',
            '/resources/{resource_id}': 'Get a specific resource by ID',
            '/auth/register': 'Register a new user with email and password',
            '/auth/login': 'Login with email and password'
        }
        }


@app.get("/resources")
def list_resources(q: str = "", category: str = ""):
    results = RESOURCES 

    if category:
        results = [r for r in results if r["category"] == category]

    if q:
        q = q.lower()
        results = [
            r for r in results
            if q in r["name"].lower()
            or q in r["description"].lower()
            or q in r["area"].lower()
        ]

    return results


@app.get("/resources/{resource_id}")
def get_resource(resource_id: int):
    for r in RESOURCES:
        if r["id"] == resource_id:
            return r
    raise HTTPException(status_code=404, detail="Resource not found")

class Resources(BaseModel):
    id: int
    name: str
    category: str
    area: str
    description: str
    phone: str | None = None
    website: str | None = None

class UserCredentials(BaseModel):
    email : str = Field(min_length=3)
    password : str = Field(min_length=6, description='Plain-text password')

    @field_validator('email')
    @classmethod
    def email_looks_valid(cls, value:str) -> str:
        candidate = value.strip().lower()
        if '@' not in candidate or "." not in candidate.split('@')[-1]:
            raise ValueError('Not a valid email address')
        return candidate


class UserPublic(BaseModel):
    email:str

_ITERATIONS = 200_000

def hash_password(password:str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, _ITERATIONS)
    return f'{salt.hex()}${digest.hex()}'

def verify_password(password:str, stored_hash:str) -> bool:
    try:
        salt_hex, digest_hex = stored_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)
    except(ValueError, AttributeError):
        return False
    actual_digest = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, _ITERATIONS)
    return hmac.compare_digest(actual_digest, expected_digest)

USERS = load_users()

@app.post('/auth/register', response_model=UserPublic, status_code=201)
def register(credentials:UserCredentials) -> UserPublic:    
    with _users_lock:
        if credentials.email in USERS:
                raise HTTPException(status_code=409, detail='This Account already exists')
        USERS[credentials.email] = hash_password(credentials.password)
        save_users()
        return UserPublic(email=credentials.email)

@app.post('/auth/login', response_model=UserPublic)
def login(credentials:UserCredentials) -> UserPublic:
    with _users_lock:
        stored_hash = USERS.get(credentials.email)
        if stored_hash is None or not verify_password(credentials.password, stored_hash):
            raise HTTPException(status_code=401, detail='invalid email or password')
        return UserPublic(email=credentials.email)

@app.post('/auth/reset-password')
def reset_password(credentials: UserCredentials) -> dict:
    with _users_lock:
        if credentials.email not in USERS:
            raise HTTPException(status_code=404, detail='No account found with that email')
        USERS[credentials.email] = hash_password(credentials.password)
        save_users()
    return {'message': 'Password updated'}


@app.exception_handler(Exception)
async def unhandled_expection_handler(request:Request, exec: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content= {'detail':'Something went wrong in the server'})


