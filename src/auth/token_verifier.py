import jwt
from fastapi import status as status_code
from .handlers import token_creator
from src.configs import environment_config
from functools import wraps

def token_verify(function: callable)->callable:

    @wraps(function)
    def decorated(*agr, **kwargs):
        bearer_token = kwargs['Authorization']
        if not bearer_token or not kwargs['uuid']:
            kwargs['response'].status_code = status_code.HTTP_401_UNAUTHORIZED
            return {"status_code": 401, "message": "not authorized"}
        try:
            token = bearer_token.split()[1]
            token_information = jwt.decode(token, key = environment_config['key'], algorithms = "HS256")
            token_uuid = token_information['uuid']
        except jwt.InvalidSignatureError:
            kwargs['response'].status_code = status_code.HTTP_401_UNAUTHORIZED
            return {"status_code": 401,"error":"token invalido"}
        except jwt.ExpiredSignatureError:
            kwargs['response'].status_code = status_code.HTTP_401_UNAUTHORIZED
            return {"status_code": 401,"error":"token expirado"}
        except KeyError:
            kwargs['response'].status_code = status_code.HTTP_401_UNAUTHORIZED
            return {"status_code": 401,"error":"not authorized"}
        
        if token_uuid != kwargs['uuid']:
            kwargs['response'].status_code = status_code.HTTP_401_UNAUTHORIZED
            return {"status_code": 401,"error":"not authorized"}
        return function(*agr, **kwargs) 

    return decorated