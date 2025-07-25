import os

from dotenv import load_dotenv


load_dotenv()

DEBUG = os.getenv("DEBUG", "true").lower() == "true"

APP_ID=os.getenv('APP_ID')
APP_HASH=os.getenv('APP_HASH')

DB_HOST = os.getenv("CHAT_ACC_MNGR_DB_HOST")
DB_PORT = os.getenv("CHAT_ACC_MNGR_PORT")
DB_USER = os.getenv("CHAT_ACC_MNGR_DB")
DB_PASSWORD = os.getenv("CHAT_ACC_MNGR_USER")
DB_NAME = os.getenv("CHAT_ACC_MNGR_PASSWORD")

REDIS_URL=os.getenv("REDIS_URL")

CHAT_PROCESS_SERVICE_URL=os.getenv("CHAT_PROCESS_SERVICE_URL")