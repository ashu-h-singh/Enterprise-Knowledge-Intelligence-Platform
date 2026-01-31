from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "EKIP")

settings = Settings()
