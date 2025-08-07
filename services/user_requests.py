from services.models import async_session
from services.models import User
from sqlalchemy import select, func
import time
import asyncio

class UserRequests:
    async def add(self, user_dto):  # принимает DTO object
        async with async_session() as session:
            user = User(user_dto.name, user_dto.email, user_dto.username, user_dto.password)  # типа to_model
            session.add(user)
            await session.commit()

    async def check_username(self, username):  # чётко работает
        async with async_session() as session:
            result = await session.scalar(select(func.count()).where(
                User.username == username))  # scalar это как #execute, но возвращается сразу объектом
            # print(result)
            # print("Check сработал")
            return result

    async def check_email(self, email):  # чётко работает
        async with async_session() as session:
            result = await session.scalar(select(func.count()).where(
                User.email == email))  # scalar это как #execute, но возвращается сразу объектом
            print(result)
            print("Check сработал")
            return result

    async def get_password(self, username):
        async with async_session() as session:
            result = await session.scalar(
                select(User.password).where(User.username == username)
            )
            return result

    async def getUser(self, user_id):
        async with async_session() as session:
            result = await session.execute(
                select(User)
                .where(User.id == user_id)
                .limit(1)
            )
            return result.scalar_one_or_none()

    async def getUserByUsername(self, username):
        async with async_session() as session:
            result = await session.execute(
                select(User)
                .where(User.username == username)
                .limit(1)
            )
            return result.scalar_one_or_none()

    async def getAllUsers(self):
        async with async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()



class UserDto:
    def __init__(self, name, email, username, password, created_at = None, user_id = None):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        if created_at == None:
            created_at = round(time.time())
        self.created_at = created_at
        self.user_id = user_id

class UserLogin:
    @classmethod
    def fromDB(cls, user_id):
        self = cls()
        user_requests = UserRequests()
        self.__user = asyncio.run(user_requests.getUser(user_id))
        return self

    def create(self, user):
        self.__user = user
        return self
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.__user.id) #айди юзера из базы данных

    def get_user_id(self):
        return self.__user.id

    def get_name(self):
        return self.__user.name

    def get_email(self):
        return self.__user.email

    def get_username(self):
        return self.__user.username

    def get_created_at(self):
        return self.__user.created_at