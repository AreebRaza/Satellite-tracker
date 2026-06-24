from app.services.satellite_service import fetch_tle, compute_position
from fastapi import APIRouter, HTTPException
from requests.exceptions import HTTPError
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/satellite/{norad_id}/position")
def get_satellite_position(norad_id: int):
    try:
        tle_text=fetch_tle(norad_id)
        pos=compute_position(tle_text)
        return pos

    except ValueError as e:
        logger.warning(f"Incorrect value error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


    except HTTPError as e:
        logger.error(f"Connection error: {e}")
        raise HTTPException(status_code=503, detail="Tracking data stream is currently unreachable.")

    except Exception as e:
        logger.error(f"Unhandled system exception: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")        
  