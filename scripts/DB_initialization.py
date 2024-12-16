import os
import importlib
from dal.database import Base, engine

def import_models_from_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, directory))[0].replace(os.sep, '.')
                print(f"Trying to import: {module_name}")  # Debugging output
                try:
                    importlib.import_module(f'models.{module_name}')                
                except ImportError as e:
                    print(f"Error importing {module_name}: {e}")
def init_db():
    """
    Initialize the database by creating all tables.
    """
    import_models_from_directory('models')  # Adjust the path if necessary
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()