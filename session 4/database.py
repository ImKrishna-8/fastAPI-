from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///book.db',echo=True)

sessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
