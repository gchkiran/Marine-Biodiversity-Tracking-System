from dal.database import get_session
from models.species import Species
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def add_species(species_name, scientific_name, conservation_status, category='Fauna', image_url=None):
    try:
        session = get_session()
        
        new_species = Species(
            common_name=species_name,
            scientific_name=scientific_name,
            conservation_status=conservation_status,
            category=category,
            image_url=image_url
        )
        
        session.add(new_species)
        session.commit()
        return new_species.id
    except IntegrityError:
        session.rollback()
        return "A species with this scientific name and conservation status already exists. Please check your data."
    except SQLAlchemyError as e:
        session.rollback()
        return f"An unexpected error occurred: {e}"

def get_species_data(query=None):
    session = get_session()
    if query:
        # Filter species by query
        species_list = session.query(Species).filter(
            (Species.common_name.ilike(f"%{query}%")) | 
            (Species.scientific_name.ilike(f"%{query}%"))
        ).all()
    else:
        species_list = session.query(Species).all()
    
    return [species_to_dict(species) for species in species_list]


def species_to_dict(species):
    return {
        'species_id': species.id,
        'species_name': species.common_name,
        'scientific_name': species.scientific_name,
        'category': species.category,
        'image_url': species.image_url,
        'conservation_status': species.conservation_status
    }


def get_species_habitat_and_threat(species_id):
    session = get_session()
    try:
        # Correctly format the SQL execution
        result = session.execute(
            text("SELECT habitat_type, habitat_description, threat_description, threat_severity, migration_pattern_description "
                 "FROM species_habitat_threat_migration_view WHERE species_id = :species_id"),
            {'species_id': species_id}
        ).fetchone()

        if result:
            return {
                'habitat_type': result.habitat_type,
                'habitat_description': result.habitat_description,
                'threat_description': result.threat_description,
                'threat_severity': result.threat_severity,
                'migration_pattern_description': result.migration_pattern_description
            }
        else:
            return {
                'habitat_type': None,
                'habitat_description': None,
                'threat_description': None,
                'threat_severity': None,
                'migration_pattern_description': None
            }
    except SQLAlchemyError as e:
        print(f"Error fetching habitat and threat information for species ID {species_id}: {e}")
        return {
            'habitat_type': None,
            'habitat_description': None,
            'threat_description': None,
            'threat_severity': None,
            'migration_pattern_description': None
        }
    finally:
        session.close()