import os

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings


class OpenAIUtils:

    def __init__(self, LLM_TO_USE="gpt4o", EMBED_TO_USE="midasembed"):
        self.llm_to_use = LLM_TO_USE
        self.embed_to_use = EMBED_TO_USE
        load_dotenv()
        self.__llm = self.__load_llm()
        self.__embeddings = self.__load_embed()

    def __load_llm(self):
        llm_api_key = os.environ.get(f"{self.llm_to_use}_api_key")
        llm_api_version = os.environ.get(f"{self.llm_to_use}_api_version")
        llm_azure_endpoint = os.environ.get(f"{self.llm_to_use}_api_endpoint")
        llm_deployment_name = os.environ.get(f"{self.llm_to_use}_dep_name")
        llm = AzureChatOpenAI(
            api_key=llm_api_key,
            openai_api_version=llm_api_version,
            azure_endpoint=llm_azure_endpoint,
            azure_deployment=llm_deployment_name,
        )
        return llm

    def __load_embed(self):
        embed_api_key = os.environ.get(f"{self.embed_to_use}_api_key")
        embed_api_version = os.environ.get(f"{self.embed_to_use}_api_version")
        embed_azure_endpoint = os.environ.get(f"{self.embed_to_use}_api_endpoint")
        embed_deployment_name = os.environ.get(f"{self.embed_to_use}_dep_name")
        embed_model = os.environ.get(f"{self.embed_to_use}_model")
        embeddings = AzureOpenAIEmbeddings(
            model=embed_model,
            api_key=embed_api_key,
            openai_api_version=embed_api_version,
            azure_endpoint=embed_azure_endpoint,
            deployment=embed_deployment_name,
            disallowed_special=(),
        )
        return embeddings

    def call_llm(self, prompt: str, max_tokens: int = 100):
        SYSTEM_MESSAGE = """You are a helpful assistant that tells the meaning of a text given in chat language.
        The text is in telugu written in English alphabets to English. Translate the text. 
        Do not translate if the text is already in English. In this case return the original text.
        Else, Give me only the translated text, nothing additional"""
        messages = [
            (
                "system",
                SYSTEM_MESSAGE,
            ),
            ("human", prompt),
        ]
        try:
            response = self.__llm.invoke(messages)
            return response.content
        except Exception as e:
            response = (
                f"Unable to translate. Reason: {e}, while translating message: {prompt}"
            )
            return response


if __name__ == "__main__":
    openai_utils = OpenAIUtils()
    text = """Em chestunnav?"""
    response = openai_utils.call_llm(text)
    print(response)
