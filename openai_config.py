import os
from dotenv import load_dotenv
from openai import OpenAI  # Import the OpenAI class

load_dotenv()  # Load environment variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)