import databases
import sqlalchemy as sa

from dio_blog.config import settings

metadata = sa.MetaData()
database = databases.Database(settings.DATABASE_URL)
engine = sa.create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)
