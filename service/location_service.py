from dal.database import get_session
from models.location import Location
from sqlalchemy.exc import SQLAlchemyError

def add_location(location_name, latitude, longitude, ecosystem_type):
    try:
        session = get_session()
        location = Location(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            ecosystem_type=ecosystem_type
        )
        session.add(location)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error adding location: {e}")
    finally:
        session.close()

def get_location_data():
    session = get_session()
    try:
        location_list = session.query(Location).all()
        return [location_to_dict(location) for location in location_list]
    except SQLAlchemyError as e:
        print(f"Error fetching location data: {e}")
        raise e
    finally:
        session.close()

def location_to_dict(location):
    return {
        'location_id': location.id,
        'location_name': location.location_name,
        'latitude': location.latitude,
        'longitude': location.longitude,
        'description': location.description,
        'ecosystem_type': location.ecosystem_type
    }
