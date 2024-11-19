from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.auth import auth_router
from app.routes.plots import plot_router
from app.routes.events import event_router
from app.routes.crops import crop_router
from app.routes.analytics import analytics_router
from app.database import database


app = FastAPI()

# Connect to the database on startup and disconnect on shutdown
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Include the routers for each feature
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(plot_router, prefix="/plots", tags=["Garden Plots"])
app.include_router(event_router, prefix="/events", tags=["Volunteer Events"])
app.include_router(crop_router, prefix="/crops", tags=["Crop Records"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

# Root route for home
