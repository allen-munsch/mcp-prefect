import os

PREFECT_API_URL = os.getenv("PREFECT_API_URL", "http://localhost:4200/api")
PREFECT_API_KEY = os.getenv("PREFECT_API_KEY")