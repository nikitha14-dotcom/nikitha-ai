# backend/app/api/tasks.py
"""Task CRUD endpoints.
All routes require authentication and operate on the Task model.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

from backend.app.core.security import get_current_user_optional
from backend.app.database import get_db
from backend.app.models.task import Task
from backend.app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = Field(default="pending")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: str
    updated_at: str

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(item: TaskCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    task = Task(title=item.title, description=item.description, status=item.status)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat(),
    )

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status,
            created_at=t.created_at.isoformat(),
            updated_at=t.updated_at.isoformat(),
        )
        for t in tasks
    ]

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, item: TaskUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat(),
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
    return None
