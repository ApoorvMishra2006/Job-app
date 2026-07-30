import os
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = r"C:\Users\Apoorv Mishra\Desktop\Apoorv_Py\JobApp\data\applied.json"

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

RESULTS_PER_PAGE = 50