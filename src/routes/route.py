from src.configs import app
import jwt 
from datetime import datetime, timedelta
from fastapi import Response, Header, status as status_code
from pydantic import BaseModel
from src.infra.entities import User
from src.infra.config import ConnectionHandler
from sqlmodel import select
from src.auth import token_creator, token_verify
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

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
        select(User.uuid, User.password)
        .where(
            User.active == True, 
            User.username == user.username
        )
    )
    row = [u._asdict() for u in result.all()]
    if len(row) != 1:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401, "message": "not authorized"}
    if not check_password_hash(row[0]['password'],user.password):
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401, "message": "not authorized"}
    token = token_creator.create(uuid = row[0]['uuid'])
    response.status_code = status_code.HTTP_200_OK
    return {"status_code": 200, 'token': token}

@app.get('/secret-information')
@token_verify
def secret_information(response: Response, Authorization: str = Header(None), uuid: str = Header(None)):
    response.status_code = status_code.HTTP_200_OK
    return {"status_code": 200, 'message': 'secret information'}