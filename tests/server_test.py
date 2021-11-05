from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from fast_auth import authenticate, create_token_jwt, require_auth, connect_database, get_db

connect_database()

app = FastAPI()


class SchemaLogin(BaseModel):
    username: str
    password: str


@app.get('/')
def home():
    return 'home'


@app.post('/login')
async def login(credentials: SchemaLogin):
    user = await authenticate(credentials.username, credentials.password)
    token = create_token_jwt(user)
    return {'access': token}


@app.get('/test_session_db')
async def session_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute('select username, password from auth_users')
    return [dict(r) for r in result]


@app.get('/authenticated')
def authenticated(payload: dict = Depends(require_auth)):
    return payload
