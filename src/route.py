from src.configs import app
import jwt 
from datetime import datetime, timedelta
from fastapi import Response, Header, status as status_code
from pydantic import BaseModel
from src.infra.entities import User
from src.infra.config import ConnectionHandler
from sqlmodel import select

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
    token = jwt.encode(
        {
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'uuid': uuid[0]
        }, 
        key = '12345', 
        algorithm = 'HS256'
    )
    response.status_code = status_code.HTTP_200_OK
    return {"status_code": 200, 'token': token}

@app.get('/secret-information')
def secret_information(response: Response, Authorization: str = Header(None), uuid: str = Header(None)):
    bearer_token = Authorization
    if not bearer_token or not uuid:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401, "message": "not authorized"}
    try:
        token = bearer_token.split()[1]
        token_information = jwt.decode(token, key = "12345", algorithms = "HS256")
        token_uuid = token_information['uuid']
    except jwt.InvalidSignatureError:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401,"error":"token invalido"}
    except jwt.ExpiredSignatureError:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401,"error":"token expirado"}
    except KeyError:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401,"error":"not authorized"}
    
    if token_uuid != uuid:
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"status_code": 401,"error":"not authorized"}

    response.status_code = status_code.HTTP_200_OK
    return {"status_code": 200, 'message': 'secret information'}