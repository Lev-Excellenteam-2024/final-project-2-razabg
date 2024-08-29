import os
import json
import pytest
from GPTPresentationSummarizer import GPTSummarizer


@pytest.mark.asyncio  # pytest for asyncio
async def test_the_project():
    """this test check that all the aspects of the project is working properly"""
    summarizer = GPTSummarizer()
    presentation_path = r".\AsyncIO Lecture.pptx"
    base_name = os.path.basename(presentation_path)
    json_file = os.path.splitext(base_name)[0] + ".json"

    summarized_slides = await summarizer.summarize_presentation(presentation_path)

    # Save the list to the JSON file
    with open(json_file, 'w') as file:
        json.dump(summarized_slides, file, indent=4)

    # Assert the JSON file was created
    assert os.path.exists(json_file), f"File {json_file} was not created"
