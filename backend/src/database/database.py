from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import logging

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    with engine.connect() as connection:
        logger.info("Successfully connected to the database!")
        result = connection.execute(text("SELECT version();"))
        logger.info(f"PostgreSQL version: {result.scalar()}")
except Exception as e:
    logger.error(f"Error connecting to the database: {e}", exc_info=True)
    raise
