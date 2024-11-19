import csv
from fastapi import APIRouter, Response
from io import StringIO
from sqlalchemy.sql import select
from app.database import database
from app.models import garden_plots, events, crop_records

analytics_router = APIRouter()


@analytics_router.get("/analytics/export/")
async def export_analytics():
    output = StringIO()
    writer = csv.writer(output)

    # Export Garden Plots
    writer.writerow(["Garden Plots"])
    writer.writerow(["ID", "Plot Number", "Size", "Location", "Status"])
    query = select(garden_plots)
    plots = await database.fetch_all(query)
    for plot in plots:
        writer.writerow([plot["id"], plot["plot_number"], plot["size"], plot["location"], plot["status"]])

    # Export Events
    writer.writerow([])
    writer.writerow(["Events"])
    writer.writerow(["ID", "Title", "Description", "Date", "Volunteers Needed"])
    query = select(events)
    events_data = await database.fetch_all(query)
    for event in events_data:
        writer.writerow([event["id"], event["title"], event["description"], event["date"], event["volunteers_needed"]])

    # Export Crop Records
    writer.writerow([])
    writer.writerow(["Crop Records"])
    writer.writerow(["ID", "Gardener ID", "Plot ID", "Crop Type", "Planting Date", "Expected Harvest Date"])
    query = select(crop_records)
    crops = await database.fetch_all(query)
    for crop in crops:
        writer.writerow([crop["id"], crop["gardener_id"], crop["plot_id"], crop["crop_type"], crop["planting_date"], crop["expected_harvest_date"]])

    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=analytics.csv"
    return response