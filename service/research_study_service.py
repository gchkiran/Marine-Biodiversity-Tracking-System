from dal.database import get_session
from models.research_study import ResearchStudy
from sqlalchemy.exc import SQLAlchemyError

def add_research_study(study_title, lead_researcher, species_focus):
    try:
        session = get_session()
        study = ResearchStudy(
            study_title=study_title,
            lead_researcher=lead_researcher,
            species_focus="; ".join(species_focus)
        )
        session.add(study)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error adding research study: {e}")
    finally:
        session.close()

def get_research_studies():
    session = get_session()
    try:
        return session.query(ResearchStudy).all()
    except SQLAlchemyError as e:
        print(f"Error fetching research studies: {e}")
        raise e
    finally:
        session.close()
