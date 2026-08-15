import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


APP_NAME = "Enterprise AI Support Agent"


MAX_RETRIES = 2