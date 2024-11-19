from fastapi import APIRouter, HTTPException, Form
from sqlalchemy.sql import select, update
from app.database import database
from app.models import events

event_router = APIRouter()


@event_router.get("/events/")
async def list_events():
    query = select(events)
    return await database.fetch_all(query)


@event_router.post("/events/")
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    volunteers_needed: int = Form(...),
):
    query = events.insert().values(title=title, description=description, date=date, volunteers_needed=volunteers_needed)
    await database.execute(query)
    return {"message": "Event created successfully"}


@event_router.put("/events/{event_id}/signup/")
async def sign_up_for_event(event_id: int, user_id: int = Form(...)):
    query = select(events).where(events.c.id == event_id)
    event = await database.fetch_one(query)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    assigned_volunteers = set(event["assigned_volunteers"].split(",") if event["assigned_volunteers"] else [])
    if str(user_id) in assigned_volunteers:
        raise HTTPException(status_code=400, detail="Already signed up for this event")

    if len(assigned_volunteers) >= event["volunteers_needed"]:
        raise HTTPException(status_code=400, detail="Event is full")

    assigned_volunteers.add(str(user_id))
    updated_volunteers = ",".join(assigned_volunteers)

    update_query = update(events).where(events.c.id == event_id).values(assigned_volunteers=updated_volunteers)
    await database.execute(update_query)
    return {"message": "Signed up for event successfully"}