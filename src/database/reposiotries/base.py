from typing import Protocol


class BaseReposiotry(Protocol):

    async def get_all(
        self,
        filters: dict = None
    ):
        pass

    async def get_one(self, filters: dict):
        pass

    async def add_one(self, data):
        pass
    
    async def update_one(
        self, 
        filters: dict, 
        data: dict
    ) -> bool:
        pass

    async def delete_one(slef, filters: dict) -> bool:
        pass

