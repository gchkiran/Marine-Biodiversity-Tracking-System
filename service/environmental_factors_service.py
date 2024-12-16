from dal.database import get_session
from models.environmental_factors import EnvironmentalFactors
from sqlalchemy import text

def get_environmental_factors(tracking_record_id):
    session = get_session()
    try:
        # Fetch environmental factors from the Environmental Factors table
        result = session.execute(
            text("SELECT * FROM environmental_factors WHERE tracking_record_id = :tracking_record_id"),
            {'tracking_record_id': tracking_record_id}
        ).fetchall()

        # Convert the result to a list of dictionaries
        environmental_factors = [environmental_factors_to_dict(row) for row in result]
        
        return environmental_factors
        
    except Exception as e:
        print(f"Error fetching environmental factors for tracking ID {tracking_record_id}: {e}")
        raise e
    finally:
        session.close()

def environmental_factors_to_dict(factor):
    return {
        'factor_id': factor.id,
        'tracking_record_id': factor.tracking_record_id,
        'factor_name': factor.factor_name,
        'factor_value': factor.factor_value,
    }