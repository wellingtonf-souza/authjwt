from src.configs import app
import jwt 
from datetime import datetime, timedelta
from fastapi import Response, Header, status as status_code
from pydantic import BaseModel
from src.infra.entities import User
from src.infra.config import ConnectionHandler
from sqlmodel import select
from .auth import token_creator, token_verify

@app.get("/")
def status():
    return {"status":200, "message": "server running"}

class UserAuth(BaseModel):
    username: str
    password: str

@app.post('/auth')
async def authorization(response: Response, user: UserAuth):
    conn = ConnectionHandler()
    result = conn.session.exec(
        select(User.uuid).where(User.active == True, User.username == user.username, User.password == user.password)
    )
    uuid = result.fetchall()
    if len(uuid) == 0:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401, "message": "not authorized"}
    token = token_creator.create(uuid = uuid[0])
    response.status_code = status_code.HTTP_200_OK
    return {"status_code": 200, 'token': token}

@app.get('/secret-information')
@token_verify
def secret_information(response: Response, Authorization: str = Header(None), uuid: str = Header(None)):
    response.status_code = status_code.HTTP_200_OK
    return {"status_code": 200, 'message': 'secret information'}