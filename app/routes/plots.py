from fastapi import APIRouter, HTTPException, Form
from sqlalchemy.sql import select, update
from app.database import database
from app.models import garden_plots

plot_router = APIRouter()


@plot_router.get("/plots/")
async def list_plots():
    query = select(garden_plots)
    return await database.fetch_all(query)


@plot_router.post("/plots/")
async def create_plot(plot_number: str = Form(...), size: str = Form(...), location: str = Form(...)):
    query = garden_plots.insert().values(plot_number=plot_number, size=size, location=location)
    await database.execute(query)
    return {"message": "Plot created successfully"}


@plot_router.put("/plots/{plot_id}/apply/")
async def apply_for_plot(plot_id: int, gardener_id: int = Form(...)):
    query = select(garden_plots).where(garden_plots.c.id == plot_id)
    plot = await database.fetch_one(query)

    if not plot or plot["status"] != "available":
        raise HTTPException(status_code=400, detail="Plot is not available")

    update_query = (
        update(garden_plots)
        .where(garden_plots.c.id == plot_id)
        .values(status="pending", gardener_id=gardener_id)
    )
    await database.execute(update_query)
    return {"message": "Applied for plot successfully"}