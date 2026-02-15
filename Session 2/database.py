from sqlmodel import create_engine

engine = create_engine('sqlite:///books.db',echo=True)



