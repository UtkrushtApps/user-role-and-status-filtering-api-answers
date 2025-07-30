import os
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import User
from app.schemas import UserRead
from app.database import get_async_session
from sqlalchemy.future import select

app = FastAPI()

@app.get("/users", response_model=List[UserRead])
async def get_users(
    role: Optional[str] = Query(None, description="Role to filter by"),
    status: Optional[str] = Query(None, description="Status to filter by"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(User)
        if role:
            query = query.where(User.role == role)
        if status:
            query = query.where(User.status == status)
        result = await session.execute(query)
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
