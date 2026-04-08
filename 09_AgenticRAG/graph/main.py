from pathlib import Path
from dotenv import load_dotenv

CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")


if __name__ == "__main__":
    print("Hello Agentic RAG")