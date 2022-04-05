from sqlmodel import Field, SQLModel, create_engine, Session, select
from src.infra.entities import *
from uuid import uuid4
from src.configs import environment_config
from werkzeug.security import generate_password_hash

class ConnectionHandler:

    def __init__(self, path: str = 'src/data/access.db') -> None:
        self.__engine = create_engine(f'sqlite:///{path}')
        SQLModel.metadata.create_all(self.__engine)
        self.session = Session(self.__engine)
        self.__create_admin()

    def __create_admin(self)->None:
        users_active = (
            self.session.exec(select(User.active).where(User.username == User.username, User.active == True))
        )
        if len(users_active.fetchall()) < 1:
            user = User(
                username = environment_config['username_admin'],
                password = generate_password_hash(environment_config['password_admin'], method='sha256'),
                uuid = uuid4().hex
            )
            self.session.add(user)
            self.session.commit()

    def close(self):
        self.session.close()