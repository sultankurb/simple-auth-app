from src.routers.main_router import api_routers
from src.services.create_app import create_app

app = create_app()
app.include_router(router=api_routers)
