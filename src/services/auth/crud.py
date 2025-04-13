from src.database.models.users import UsersODM
from src.database.reposiotries.beanie_repository import BeanieRepository


class UsersRepository(BeanieRepository):
    model = UsersODM
