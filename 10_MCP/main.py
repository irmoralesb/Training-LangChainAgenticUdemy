import asyncio
from dotenv import load_dotenv
from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")


async def main():
    print("Hello from MCP!")


if __name__ == "__main__":
    asyncio.run(main())
