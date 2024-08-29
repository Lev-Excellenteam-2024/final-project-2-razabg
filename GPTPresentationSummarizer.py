import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import presentaion_parse


class GPTSummarizer:
    """
    A class to summarize PowerPoint presentations using OpenAI's GPT model.

    Attributes:
        client (AsyncOpenAI): An instance of the AsyncOpenAI client to interact with the OpenAI API.
        prompt (str): The prompt used to instruct GPT on how to summarize the slide content.

    Methods:
        gpt_api(slide: str) -> str:
            Sends the slide text to the OpenAI API to get a summarized response.
            Args:
                slide (str): The text content of a slide to be summarized.
            Returns:
                str: The summarized content of the slide.

        summarize_presentation(presentation_path: str) -> list:
            Summarizes the entire presentation by extracting text from each slide and generating
            a summary using the OpenAI API.
            Args:
                presentation_path (str): The file path to the PowerPoint presentation.
            Returns:
                list: A list of strings where each string contains the slide number and its summary.
    """

    def __init__(self):
        """
        Initializes the GPTSummarizer, loads environment variables for API key, and sets up the OpenAI client.
        """
        load_dotenv()  # Load environment variables from a .env file
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.prompt = ("Explain the given text of the slide in a simple way so every student who missed the class will "
                       "understand the material as fast as he can.")

    async def gpt_api(self, slide: str) -> str:
        """
        Sends the slide text to the OpenAI API for summarization.

        Args:
            slide (str): The text content of a slide to be summarized.

        Returns:
            str: The summarized content of the slide.
        """
        response = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{self.prompt}: {slide}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content.strip()

    async def summarize_presentation(self, presentation_path: str) -> list:
        """
        Summarizes the entire presentation by extracting text from each slide and generating a summary
        using the OpenAI API.

        Args:
            presentation_path (str): The file path to the PowerPoint presentation.

        Returns:
            list: A list of strings where each string contains the slide number and its summary.
        """
        presentation_to_sum_up = presentaion_parse.PresentationReader(presentation_path).extract_text()

        # Create a list of tasks for asynchronous processing of slide summaries
        tasks = [self.gpt_api(slide) for key, slide in presentation_to_sum_up.items()]

        # Gather results from all tasks
        sum_up_of_slides = await asyncio.gather(*tasks)

        
        sum_up = [f"Slide number: {key} -- {summary}" for key, summary in
                  zip(presentation_to_sum_up.keys(), sum_up_of_slides)]

        return sum_up
