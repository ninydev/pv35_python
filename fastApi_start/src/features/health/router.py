from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from .service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_alive = await HealthService.check_database(db)
    memory = HealthService.get_memory_usage()
    disk = HealthService.get_disk_usage()
    
    status = "ok" if db_alive else "unhealthy"
    
    return {
        "status": status,
        "database": "online" if db_alive else "offline",
        "system": {
            "memory": memory,
            "disk": disk
        }
    }
