from dal.database import get_session
from models.habitat import Habitat

def add_habitat(habitat_type, habitat_description, species_id):

    session = get_session()

    new_habitat = Habitat(
        type=habitat_type,
        description=habitat_description,
        species_id=species_id
    )
    
    session.add(new_habitat)
    session.commit()

    return new_habitat