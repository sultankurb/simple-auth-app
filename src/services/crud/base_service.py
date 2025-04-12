from beanie import Document

from src.database.reposiotries.base import BaseReposiotry


class BaseService:
    def __init__(self, repository: BaseReposiotry):
        self.repository: BaseReposiotry = repository
    
    async def get_all(
        self,
        filters: dict | None = None,
        limit: int | None = None,
        offset: int | None = None

    ):
        filters.update(
            limit=limit,
            offset=offset
        )
        result = await self.repository.get_all(
            filters=filters
        )
        return result
    
    async def get_one(self, filters: dict):
        result = await self.repository.get_one(filters=filters)
        return result
    
    async def add_new_one(self, data: Document):
        pass

