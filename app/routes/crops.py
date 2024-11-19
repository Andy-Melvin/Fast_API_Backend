from fastapi import APIRouter, Form
from sqlalchemy.sql import select
from app.database import database
from app.models import crop_records

crop_router = APIRouter()


@crop_router.get("/crops/")
async def list_crops():
    query = select(crop_records)
    return await database.fetch_all(query)


@crop_router.post("/crops/")
async def add_crop_record(
    gardener_id: int = Form(...),
    plot_id: int = Form(...),
    crop_type: str = Form(...),
    planting_date: str = Form(...),
    expected_harvest_date: str = Form(...),
    notes: str = Form(None),
):
    query = crop_records.insert().values(
        gardener_id=gardener_id,
        plot_id=plot_id,
        crop_type=crop_type,
        planting_date=planting_date,
        expected_harvest_date=expected_harvest_date,
        notes=notes,
    )
    await database.execute(query)
    return {"message": "Crop record added successfully"}