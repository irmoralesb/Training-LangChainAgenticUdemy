from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def main():
    pass


if __name__ == "__main__":
    main()
