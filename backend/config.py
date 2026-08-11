import os

from dotenv import load_dotenv

load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

if not all([COGNODB_URI, COGNODB_USERNAME, COGNODB_PASSWORD]):
    raise RuntimeError(
        "Missing COGNODB_URI, COGNODB_USERNAME, or COGNODB_PASSWORD"
    )
