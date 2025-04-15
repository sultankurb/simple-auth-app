from beanie import Document


class BeanieRepository:
    model: Document = None

    async def get_all(
        self,
        filters: dict = None
    ):
        result = await self.model.find_all(filters).to_list()
        return result
    
    async def get_one(self, filters: dict):
        result = await self.model.find_one(filters)
        return result
    
    @classmethod
    async def add_one(cls, data: Document):
        result = await data.save()
        return result

    async def delete_one(self, filters: dict) -> bool:
        result = await self.model.find_one(filters)
        if result is not None:
            await result.delete()
            return True
        return False

    async def update_one(self, filters: dict, data: dict) -> bool:
        result = await self.model.find_one(filters)
        await result.update({"$set": data})
        if result is not None:
            return True
        return False
