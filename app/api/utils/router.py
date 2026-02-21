

from fastapi import APIRouter, Depends
from app.core.error.error_types import ErrorType
from app.core.error.message_codes import MessageCode
from app.core.response.response_builder import ResponseBuilder
from app.database.mysql.base import MysqlBase
from app.database.mysql.session import _engine
from app.database.postgresql.session import create_tables, init_engine
from app.depends.language_depends import get_language

router = APIRouter(prefix="/utils", tags=["Utils"])

@router.get("/create-tables")
async def start(lang: str = Depends(get_language),):

    # PostgreSQL Tables
    init_engine(echo=True)
    await create_tables()

    # MySQL Tables
    MysqlBase.metadata.create_all(bind=_engine)
    return ResponseBuilder.build(
        ErrorType.SUC_200_SUCCESS,
        MessageCode.RESOURCE_CREATED,
        lang
    )