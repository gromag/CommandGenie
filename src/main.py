import subprocess
import pydantic
from abc import ABC, abstractmethod
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMBashChain
from langchain.utilities import BashProcess
import sys
import re
import os
from dotenv import load_dotenv
load_dotenv()

_PROMPT_TEMPLATE = """If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:
Question: "copy the files in the directory named 'target' into a new directory at the same level as target called 'myNewDirectory'"
I need to take the following actions:
- List all files in the directory
- Create a new directory
- Copy the files from the first directory into the second directory
Explanation:
`ls` lists all files in current directory 
`mkdir` creates a new directory
`cp -r` copies files recursively into the new directory
```bash
ls
mkdir myNewDirectory
cp -r target/* myNewDirectory
```

Do not use 'echo' when writing the script.

That is the format. Begin!
Question: {question}"""

PROMPT = PromptTemplate(input_variables=["question"], template=_PROMPT_TEMPLATE)

llm = OpenAI(temperature=0, openai_api_key= os.getenv("OPENAI_API_KEY"))
bash_chain = LLMBashChain(llm=llm, prompt=PROMPT, verbose=True)



class GenieBase(ABC):
    
    @abstractmethod
    def get_command(self, instruction):
        pass
    @abstractmethod
    def execute_command(self):
        pass
    @abstractmethod
    def confirm_command(self):
        pass

class Genie(GenieBase):

    def __init__(self) -> None:
        super().__init__()
        self.commands_history = []
        self.bash = BashProcess()

    def get_command(self, instruction):

        prompt = PROMPT.format(question=instruction)
        # print(prompt)

        result = llm.generate([prompt])
        output = result.generations[0][0].text
        outputs = re.split("```bash", output)
        reasoning = outputs[0].strip()
        command = "\n".join(re.split("\n", outputs[1])[:-1]).strip()
        self.commands_history.append((command, reasoning))
        return command, reasoning
    
    def execute_command(self, command):
        output = self.bash.run(command)
        print(output)
        
    
    def confirm_command(self, command, reasoning):
        answer = input("\n\n{command}\n\nWould you like to execute? [Y/n/(e)xplain] ".format(command=command))
        if answer in ["Y", "y"]:
            print("\n")
            return True
        if answer in ["e", "explain"]:
            self.confirm_command(reasoning, reasoning)
            

    @classmethod
    def activate(cls, instruction):
        g = Genie()
        # try:
        command, reasoning = g.get_command(instruction)
        execute = g.confirm_command(command, reasoning)
        if execute:
            g.execute_command(command)



if __name__ == "__main__":
    # Get the command-line arguments
    args = sys.argv[1:]
    # Join the arguments into a single string
    instruction = ' '.join(args)
    Genie.activate(instruction)
    
