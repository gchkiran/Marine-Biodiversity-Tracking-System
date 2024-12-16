from dal.database import get_session
from models.threat import Threat

def add_threat(description, severity, species_id):
    session = get_session()

    new_threat = Threat(
        description=description,
        severity=severity,
        species_id=species_id
    )

    session.add(new_threat)
    session.commit()

    return new_threat