import psutil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from loguru import logger

class HealthService:
    @staticmethod
    async def check_database(db: AsyncSession) -> bool:
        try:
            await db.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    @staticmethod
    def get_memory_usage():
        vm = psutil.virtual_memory()
        return {
            "total_gb": round(vm.total / (1024**3), 2),
            "used_gb": round(vm.used / (1024**3), 2),
            "free_gb": round(vm.available / (1024**3), 2),
            "percent": vm.percent
        }

    @staticmethod
    def get_disk_usage():
        disk = psutil.disk_usage('/')
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent
        }
