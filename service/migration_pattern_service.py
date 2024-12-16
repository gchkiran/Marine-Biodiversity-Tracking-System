# service/migration_pattern_service.py
from dal.database import get_session
from models.migration_pattern import MigrationPattern

def add_migration_pattern(description, species_id):
    session = get_session()

    new_migration_pattern = MigrationPattern(
        description=description,
        species_id=species_id
    )

    session.add(new_migration_pattern)
    session.commit()

    return new_migration_pattern