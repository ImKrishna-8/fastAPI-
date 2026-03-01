from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base 
engine = create_async_engine("sqlite+aiosqlite:///test.db",echo=True,pool_size=2)


async_session = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)


