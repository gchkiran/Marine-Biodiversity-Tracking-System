from dal.database import get_session
from models.conservation_project import ConservationProject
from sqlalchemy.exc import SQLAlchemyError

def add_conservation_project(project_name, description, start_date, end_date, organization_name):
    try:
        session = get_session()
        project = ConservationProject(
            project_name=project_name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            organization_name=organization_name
        )
        session.add(project)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error adding conservation project: {e}")
    finally:
        session.close()

def get_conservation_projects():
    session = get_session()
    try:
        return session.query(ConservationProject).all()
    except SQLAlchemyError as e:
        print(f"Error fetching conservation projects: {e}")
        raise e
    finally:
        session.close()
