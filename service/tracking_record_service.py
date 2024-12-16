from dal.database import get_session
from models.tracking_record import TrackingRecord
from models.species import Species
from models.location import Location
from sqlalchemy import text

def add_tracking_record(species_id, location_id, timestamp, count):
    try:
        session = get_session()
        record = TrackingRecord(
            species_id=species_id,
            location_id=location_id,
            timestamp=timestamp,
            count=count
        )
        session.add(record)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        print(f"Error adding tracking record: {e}")

def get_tracking_data():
    session = get_session()
    try:
        # Join TrackingRecord with Species and Location (via relationships)
        # tracking_records = session.query(TrackingRecord, Species, Location).join(Species).join(Location).all()

        tracking_records = session.execute(text("SELECT * FROM tracking_data_view")).fetchall()


        # Convert the result to a list of dictionaries including species and location data
        return [tracking_record_to_dict(record) for record in tracking_records]
        
    except Exception as e:
        print(f"Error fetching tracking data: {e}")
        raise e
    finally:
        session.close()


def tracking_record_to_dict(record):
    # Convert the TrackingRecord, Species, and Location to a dictionary
    return {
        'tracking_id': record.tracking_id,
        'timestamp': record.timestamp,
        'count': record.species_count,
        'species_id': record.species_id,
        'species_name': record.species_name,
        'scientific_name': record.scientific_name,
        'category': record.category,
        'image_url': record.image_url,
        'conservation_status': record.conservation_status,
        'location_id': record.location_id,
        'latitude': record.latitude,
        'longitude': record.longitude,
        'location_name': record.location_name
    }
