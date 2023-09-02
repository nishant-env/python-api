from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote_plus
engine1 = create_engine('postgresql+psycopg2://postgres:%s@localhost:9876/fastapi' % quote_plus('Root@123'), echo=True)

class SessionContextManger:
    def __init__(self):
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
        self.session = None

    def __enter__(self):
        self.session = self.Session()
        return self.session
    
    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.session.close()