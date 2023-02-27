"""
The genie module provides the Genie class, a class that generates
 and executes commands based on natural language instructions.

Classes:
    Genie: A class that generates and executes commands based on natural language instructions.

"""

from typing import Dict
from langchain.utilities import BashProcess
from genie.consts import PROMPT_TEMPLATE, COMMAND_ASK_EXECUTE_TEMPLATE
from abstractions import GenieBaseClient, GenieBaseServer, LanguageModelBase, LanguageModelResponse
from internals.ui_interaction import UIInteraction
from internals.logger import genie_logger
from daemon.client import call_daemon


class GenieServer(GenieBaseServer):
    """
    The Genie class generates commands based on natural language instructions.
    Run as a daemon.

    Attributes:
        commands_history: A list of tuples containing the command and reasoning for each generated command.
        bash: A BashProcess object for executing commands.

    Methods:
        get_command(instruction): Generates a command string based on the provided natural language instruction.
        execute_command(command): Executes the given command.
        confirm_command(command, reasoning): Asks the user to confirm the given command based on some reasoning.
        run(instruction): Creates a Genie instance and generates, executes and confirms a command based on
         the provided instruction.
    """

    def __init__(self, llm: LanguageModelBase) -> None:
        super().__init__()
        self.llm = llm
        self.commands_history: Dict[str, LanguageModelResponse] = {}

    def get_command(self, instruction):
        """
        Generates a command string based on the provided natural language instruction.

        Args:
            instruction: A string representing a natural language instruction.

        Returns:
            A tuple containing a string representing a command and a string representing the
             reasoning behind the command.
        """
        if instruction not in self.commands_history.keys():
            genie_logger.info("Command not found in history")
            prompt = PROMPT_TEMPLATE.format(question=instruction)
            command = self.llm.execute(prompt=prompt)
            self.commands_history[instruction] = command

        output = self.commands_history[instruction]
        return output.command, output.reasoning


class GenieClient(GenieBaseClient):
    """
    The Genie class generates and executes commands based on natural language instructions.

    Attributes:
        commands_history: A list of tuples containing the command and reasoning for each generated command.
        bash: A BashProcess object for executing commands.

    Methods:
        get_command(instruction): Generates a command string based on the provided natural language instruction.
        execute_command(command): Executes the given command.
        confirm_command(command, reasoning): Asks the user to confirm the given command based on some reasoning.
        run(instruction): Creates a Genie instance and generates, executes and confirms a command based on
         the provided instruction.
    """

    def __init__(self, ui_interaction: UIInteraction) -> None:
        super().__init__()
        self.ui = ui_interaction
        self.bash = BashProcess()

    def get_command(self, instruction):
        """
        Generates a command string based on the provided natural language instruction.

        Args:
            instruction: A string representing a natural language instruction.

        Returns:
            A tuple containing a string representing a command and a string representing the
             reasoning behind the command.
        """
        return call_daemon(instruction)

    def execute_command(self, command):
        """
        Executes the given command.

        Args:
            command: A string representing a command.

        Returns:
            None
        """
        output = self.bash.run(command)
        self.ui.say(output)

    def confirm_command(self, command, reasoning):
        """
        Asks the user to confirm the given command based on some reasoning.

        Args:
            command: A string representing a command.
            reasoning: A string representing the reasoning behind the command.

        Returns:
            A Boolean indicating whether the command should be executed.
        """
        answer = self.ui.ask(COMMAND_ASK_EXECUTE_TEMPLATE.format(command=command)).lower()
        if answer in ["yes", "y"]:
            self.ui.say("\n")
            return True
        elif answer in ["e", "explain"]:
            return self.confirm_command(reasoning, reasoning)
        else:
            return False

    def run(self, instruction):
        """
        Given some instructions generates, executes, and confirms a command based on the provided instruction.

        Args:
            instruction: A string representing a natural language instruction.

        Returns:
            None
        """

        command, reasoning = self.get_command(instruction)
        execute = self.confirm_command(command, reasoning)
        if execute:
            self.execute_command(command)
