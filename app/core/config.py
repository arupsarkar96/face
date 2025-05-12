from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_MATCHING_QUEUE: str = "FACE_MATCH"
    DATABASE_URL: str = "mysql+pymysql://arup:Aspire_5742@192.168.0.100/lpis"

settings = Settings()
