import jwt
from datetime import datetime, timedelta

class TokenCreator:
    def __init__(self, key, exp_time) -> None:
        self.__TOKEN_KEY = key
        self.__EXP_TIME = exp_time

    def create(self, uuid: int):
        return self.__encode_token(uuid = uuid)

    def __encode_token(self, uuid: str):
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(minutes=self.__EXP_TIME),
                'uuid': uuid
            }, 
            key = self.__TOKEN_KEY, 
            algorithm = 'HS256'
        )
        return token