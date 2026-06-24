from fastapi import FastAPI 
from app.routers.satellites import router
import logging
from datetime import datetime


log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),              # console output
        logging.FileHandler(log_filename)   # file output
    ]
)
app=FastAPI()

app.include_router(router)
@app.get("/")
def home():
    return {"message": "Main system online"}  