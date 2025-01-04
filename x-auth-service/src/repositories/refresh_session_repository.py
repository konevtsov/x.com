import uuid
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Result, select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import connector
from schemas.auth import RefreshSessionSchema, JWTTokenUpdateSchema
from database.models import RefreshSession, User


class RefreshSessionRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_getter)):
        self._session = session

    async def add_refresh_session(self, refresh_session: RefreshSessionSchema):
        new_refresh_session = RefreshSession(**refresh_session.model_dump())
        self._session.add(new_refresh_session)
        await self._session.commit()

    async def get_all_sessions_by_user_id(self, user_id: int):
        stmt = select(RefreshSession).where(RefreshSession.user_id == user_id)
        result: Result = await self._session.execute(stmt)
        return result.scalars().all()

    async def drop_all_sessions(self, user_id: int):
        stmt = delete(RefreshSession).where(RefreshSession.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_token_by_uuid(self, uuid: str):
        stmt = select(RefreshSession.refresh_token).where(RefreshSession.refresh_token_uuid == uuid)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def get_all_refresh_tokens_by_email(self, email: str):
        stmt = select(RefreshSession.refresh_token).join(User).filter(User.email == email)
        result: Result = await self._session.execute(stmt)
        return result.scalars().all()

    async def delete_session_by_uuid(self, uuid: str):
        stmt = delete(RefreshSession).where(RefreshSession.refresh_token_uuid == uuid)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_refresh_token_by_uuid(self, jwt_update: JWTTokenUpdateSchema):
        stmt = (
            update(RefreshSession)
            .where(RefreshSession.refresh_token_uuid == jwt_update.uuid)
            .values(refresh_token=jwt_update.refresh_token)
        )
        await self._session.execute(stmt)
        await self._session.commit()
