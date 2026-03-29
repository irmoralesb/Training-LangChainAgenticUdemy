import os
from pathlib import Path
from dotenv import load_dotenv
#from langchain_core.messages import InputTokenDetails
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def get_chat_llm(provider_name: str, **kwargs) -> BaseChatModel:

    factories = {
        "openai": lambda : ChatOpenAI (model="gpt-4o-mini", **kwargs),
        "anthropic": lambda : ChatAnthropic(model="claude-haiku-4-5", **kwargs),
        #"ollama": lambda : ChatOllama (model="gemma3:270m", **kwargs),
        "ollama": lambda : ChatOllama (model="gpt-oss:20b", **kwargs),
        #"ollama": lambda : ChatOllama (model="qwen3:1.7b", **kwargs),
    }


    if provider_name not in factories:
        raise ValueError(f"Unknown provider: {provider_name}")

    return factories[provider_name]()



def main(provider_name:str):
    print("Hello LangChain")
    info_path = Path(__file__).resolve().parent / "information.txt"
    information = info_path.read_text(encoding='utf-8')
    person = "Elon Musk"

    summary_template = f"""
    Given the information {information} about {person} I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    #llm = ChatOpenAI(temperature=0, model="gpt-5")
    llm = get_chat_llm(provider_name=provider_name, temperature = 0)

    # LangChain Expression Syntax!!!
    chain = summary_prompt_template | llm
    response = chain.invoke(input={"information": information, "person":person})
    print(response.content)

if __name__ == "__main__":
    main("ollama")
    #print(os.environ.get("OPENAI_API_KEY"))
