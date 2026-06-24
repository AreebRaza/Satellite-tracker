from skyfield.api import load, EarthSatellite, wgs84
import requests
import logging

logger = logging.getLogger(__name__)

def fetch_tle(norad_id: int) -> str:
    
    # check if norad id is valid
    if norad_id<=0:
        logger.warning(f"Invalid NORAD code {norad_id}. The value must be a positive integer")
        raise ValueError(f"Invalid NORAD code {norad_id}. The value must be a positive integer")


    logger.info(f"NORAD id {norad_id} is valid")

    # fetch the tle from Celestrak
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
    response=requests.get(url)


    # check status
    response.raise_for_status()
    logger.info(f"NORAD id {norad_id} TLE fetched from Celestrak")

    #if we get a positive response (i.e: code 200) return the TLE
    if response.text.strip():
        return response.text
    else:        
        logger.warning(f"TLE fetched is empty or contains invalid data")
        raise ValueError(f"TLE fetched is empty or contains invalid data")
        raise HTTPErrror

def compute_position(tle_text: str) -> dict:

    #parse the TLE text, splitting into 3 distinct lines
    lines =tle_text.strip().splitlines()
    if len(lines) !=3:
        logger.warning(f"Possible TLE corruption or invalid format")
        logger.debug(f"TLE = {tle_text}")
        raise ValueError(f"Error: TLE is corrupted or contains invalid data.")
    name, line1, line2 = lines[0].strip(), lines[1], lines[2]
    # Initialization Skyfield object

    ts = load.timescale()
    satellite= EarthSatellite(line1,line2, name, ts)

    logger.info(f" Satellite object {name} successfully created")
    # propagate to current time and determine position
    t_current= ts.now()
    geocentric_pos=satellite.at(t_current)

    lat, lon = wgs84.latlon_of(geocentric_pos)
    height = wgs84.height_of(geocentric_pos)

    # Log the geographic position
    logger.info(f"Satellite: {name}")
    logger.info(f"Latitude:  {lat}")
    logger.info(f"Longitude: {lon}")
    logger.info(f"Altitude:  {height.km}")


    satellite_pos={"name": name, "Latitude":lat.degrees,"Longitude":lon.degrees,"Altitude":height.km}
    return satellite_pos