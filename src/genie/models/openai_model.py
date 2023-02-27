import re
from dotenv import load_dotenv
from langchain.llms import OpenAI
from abstractions import LanguageModelResponse, LanguageModelBase
from internals.logger import genie_logger

load_dotenv()


class OpenAILanguageModel(LanguageModelBase):
    def __init__(self, open_api_key: str) -> None:
        self.llm = OpenAI(temperature=0, openai_api_key=open_api_key)

    def execute(self, prompt: str) -> LanguageModelResponse:
        genie_logger.info(prompt)
        result = self.llm.generate([prompt])
        output = result.generations[0][0].text
        genie_logger.info(output)
        outputs = re.split("```bash", output)
        reasoning = outputs[0].strip()
        command = "\n".join(re.split("\n", outputs[1])[:-1]).strip()
        return LanguageModelResponse(command=command, reasoning=reasoning)
