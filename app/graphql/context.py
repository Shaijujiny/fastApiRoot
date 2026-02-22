from strawberry.fastapi import BaseContext

from app.database.postgresql.session import get_session_maker
from app.depends.jwt_depends import jwt_service
from app.models.postgresql.users import TblUser


class GraphQLContext(BaseContext):
    def __init__(self):
        super().__init__()
        self.user = None

    async def get_user(self):
        if self.user:
            return self.user

        # request is available on self.request in Strawberry FastAPI BaseContext
        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = await jwt_service.verify_token(token, "access")
            user_id = int(payload["sub"])

            session_maker = get_session_maker()
            async with session_maker() as db:
                user = await TblUser.get_by_id(db, user_id)
                self.user = user
                return user
        except Exception:
            return None


async def get_graphql_context():
    return GraphQLContext()
