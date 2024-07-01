from helpers.web_scraping import get_listed_gb_details
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def gb_details():
    return "Landing Page"

@app.get("/gb_details")
def gb_details():
    """
    Scrapes first 5 pages of GB forum listings
    """
    return get_listed_gb_details()