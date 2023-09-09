from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import settings

engine1 = create_engine(f'postgresql+psycopg2://{settings.database_user}:%s@{settings.database_host}:{settings.database_port}/{settings.database_name}' % quote_plus(settings.database_password), echo=True)

class SessionContextManger:
    def __init__(self):
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
        self.session = None

    def __enter__(self):
        self.session = self.Session()
        return self.session
    
    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.session.close()