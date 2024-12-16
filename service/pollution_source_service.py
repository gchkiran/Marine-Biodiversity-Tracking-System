from dal.database import get_session
from models.pollution_source import PollutionSource
from sqlalchemy.exc import SQLAlchemyError
from models.location import Location

def add_pollution_source(pollution_source_name, source_type, location_id, pollutant_level=None):
    try:
        session = get_session()
        pollution_source = PollutionSource(
            pollution_source_name=pollution_source_name,
            source_type=source_type,
            location_id=location_id,
            pollutant_level=pollutant_level
        )
        session.add(pollution_source)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error adding pollution source: {e}")
    finally:
        session.close()

def get_pollution_sources():
    session = get_session()
    try:
        results = session.query(PollutionSource, Location) \
            .join(Location, PollutionSource.location_id == Location.id) \
            .all()

        # Transform the results into a list of dictionaries
        pollution_sources = [{
            "pollution_source_name": ps.pollution_source_name,
            "pollution_type": ps.source_type,
            "pollutant_level": ps.pollutant_level,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "location_name": loc.location_name,
            "location_id": loc.id,
        } for ps, loc in results]

        return pollution_sources

    except SQLAlchemyError as e:
        print(f"Error fetching pollution sources: {e}")
        raise e
    finally:
        session.close()