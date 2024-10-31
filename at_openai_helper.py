import logging
import pandas as pd
from openai import OpenAI
from openai import AzureOpenAI
from openai import AsyncAzureOpenAI
import asyncio
import nest_asyncio

# Configure logging to include date and time
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

class ATOpenAIException(Exception):
    """
    Custom Exception used to handle exceptions in this module.

    :Author: Alonso Castañeda
    :Date: 2024-08-06

    """
    pass

class ATOpenAIIHelper:

    """

    Class to abstract the calls to Open AI API.

    Attributes
    ----------
    openai_api_key: str
        OpenAI API Key

    Methods
    -------
    def get_paylocity_token(url: str, clientid: str, clientsecret: str, data: dict)
        Generates access token to execute all subsequent API requests.
    
    """
    def __init__(self,openai_api_key: str, azure_ai_endpoint:str = None, async_limit:int = 25) -> None:
        """
        Constructs all necessary attributes for the OpenAIIHelper object.

        Parameters
        ----------
            openai_api_key : str
                API key that is used to call the api.
        """
        self.openai_api_key = openai_api_key
        self.azure_ai_endpoint = azure_ai_endpoint
        self.limit = asyncio.Semaphore(async_limit)

    def test_method(self):
         return "This works!!!"
    
    def completions(self, system_content: str, user_content: str, messages: list[dict] = [], temperature: float = 0.7, model: str="gpt-4o-mini") -> str:
        """
        Chat Completion API from Open AI.

        Parameters
        ----------
            system_content : str
                Prompt for how the model should interact with the user.
            user_content : str
                Prompt for how the model should interact with the user.
            messages : list[dict]
                Messages to instruct the model with system, user and assistant roles.
            temperature : float = 0.7
                Prompt for how the model should interact with the user.
            model : str = "gpt-4o-mini"
                Prompt for how the model should interact with the user.
        """

        if self.azure_ai_endpoint is not None:
            client = AzureOpenAI(
                azure_endpoint=self.azure_ai_endpoint,
                api_version="2024-02-15-preview",
                api_key=self.openai_api_key
            )
        else:
            client = OpenAI(
                # This is the default and can be omitted
                api_key=self.openai_api_key,
            )

        if(len(messages) == 0):
            messages = [
                {
                "role": "system",
                "content": system_content
                },
                {
                "role": "user",
                "content": user_content
                }
            ]
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model= model,
                temperature= temperature,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            logging.log(logging.ERROR,f"Error calling the Open AI API.",e)
            raise OpenAIException(f"Error calling the Open AI API.",e)
        
    async def async_completions(self, system_content: str, user_content: str, messages: list[dict] = [], temperature: float = 0.7, model: str="gpt-4o-mini") -> str:
        """
        Chat Completion API from Open AI in Async Mode.

        Parameters
        ----------
            system_content : str
                Prompt for how the model should interact with the user.
            user_content : str
                Prompt for how the model should interact with the user.
            messages : list[dict]
                Messages to instruct the model with system, user and assistant roles.
            temperature : float = 0.7
                Prompt for how the model should interact with the user.
            model : str = "gpt-4o-mini"
                Prompt for how the model should interact with the user.
        """

        if self.azure_ai_endpoint is not None:
            client = AsyncAzureOpenAI(
                azure_endpoint=self.azure_ai_endpoint,
                api_version="2024-02-15-preview",
                api_key=self.openai_api_key
            )
        else:
            client = AsyncOpenAI(
                # This is the default and can be omitted
                api_key=self.openai_api_key,
            )

        if(len(messages) == 0):
            messages = [
                {
                "role": "system",
                "content": system_content
                },
                {
                "role": "user",
                "content": user_content
                }
            ]
        try:
            async with self.limit:
                chat_completion = await client.chat.completions.create(
                    messages=messages,
                    model= model,
                    temperature= temperature,
                )
                # When workers hit the limit, they'll wait for a second
                # before making more requests.
                if self.limit.locked():
                    logging.info(f"Concurrency limit reached, waiting ...")
                    await asyncio.sleep(1)

                return chat_completion.choices[0].message.content

        except Exception as e:
            logging.error(f"Error calling the Open AI API.",e)
            raise OpenAIException(f"Error calling the Open AI API.",e)
        
    nest_asyncio.apply()

    def async_pandas_apply_for_func_result(self,dfi,prompt,func, *args, **kwargs):
        """
        Applies an asynchronous OpenAI async_completions function call for the given prompt and Dataframe dfi.

        Parameters:
        dfi (pandas.DataFrame): The DataFrame to which the function will be applied.
        func (callable): The function to extract the data to be apply to each row of the DataFrame.
        *args: Additional positional arguments to pass to the function.
        **kwargs: Additional keyword arguments to pass to the function.

        Returns:
        pandas.DataFrame: A DataFrame with the results of the function applied to each row.
        """
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.async_completions(prompt,func(row,*args, **kwargs),temperature=0)) for _, row in dfi.iterrows()]
        return loop.run_until_complete(asyncio.gather(*tasks))


