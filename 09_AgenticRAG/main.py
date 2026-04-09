from graph.graph import app
from dotenv import load_dotenv
from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")


if __name__ == "__main__":
    print("Hello Advanced RAG")
    print(app.invoke(input={"question": "what is agent memory?"}))
