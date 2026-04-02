import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INDEX_NAME = os.environ.get("INDEX_NAME")


def main():
    print("Ingesting...")
    loader = TextLoader(Path.joinpath(CURRENT_DIRECTORY,
                        "mediumblog1.txt"), encoding="UTF-8")
    document = loader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks.")

    embeddings = OpenAIEmbeddings(openai_api_type=OPENAI_API_KEY)

    print("Ingesting...")

    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=INDEX_NAME)

    print("Finish!")


if __name__ == "__main__":
    main()
