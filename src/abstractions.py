"""
The interfaces module provides a set of abstract classes that define interfaces for interacting
with some functionality.

Classes:
    GenieBase: Abstract base class for a Genie, a class that generates and executes commands.
    LanguageModelResponse: A data class for holding a response from a language model.
    LanguageModelBase: An abstract base class for a language model.

"""

from abc import ABC, abstractmethod
from pathlib import Path
from pydantic import BaseModel


class GenieBaseServer(ABC):
    """
    Abstract base class for a Genie, a class that generates commands.

    Attributes:
        None

    Methods:
        get_command(instruction): Abstract method that returns a command string based on the provided instruction.
    """

    @abstractmethod
    def get_command(self, instruction):
        """
        Returns a command string based on the provided instruction.

        Args:
            instruction: A string representing an instruction.

        Returns:
            A string representing a command.
        """
        pass


class GenieBaseClient(GenieBaseServer):
    """
    Abstract base class for a Genie, a class that generates and executes commands.

    Attributes:
        None

    Methods:
        execute_command(command): Abstract method that executes the given command.
        confirm_command(command, reasoning): Abstract method that confirms the given command based on some reasoning.
    """

    @abstractmethod
    def execute_command(self, command):
        """
        Executes the given command.

        Args:
            command: A string representing a command.

        Returns:
            None
        """
        pass

    @abstractmethod
    def confirm_command(self, command, reasoning):
        """
        Confirms the given command based on some reasoning.

        Args:
            command: A string representing a command.
            reasoning: A string representing the reasoning behind the command.

        Returns:
            A Boolean indicating whether the command was confirmed.
        """
        pass


class LanguageModelResponse(BaseModel):
    """
    A data class for holding a response from a language model.

    Attributes:
        command: A string representing a command generated by the language model.
        reasoning: A string representing the reasoning behind the generated command.
    """

    command: str
    reasoning: str


class LanguageModelBase(ABC):
    """
    An abstract base class for a language model.

    Attributes:
        None

    Methods:
        execute(prompt): Abstract method that generates a command based on the provided prompt.
    """

    @abstractmethod
    def execute(self, prompt: str) -> LanguageModelResponse:
        """
        Generates a command based on the provided prompt.

        Args:
            prompt: A string representing a prompt to generate a command from.

        Returns:
            A LanguageModelResponse object containing the generated command and reasoning.
        """
        pass


class UserInteractionBase(ABC):
    def ask(self, question) -> str:
        pass

    def say(self, text: str):
        pass


class LogPathProvider(ABC):
    def get_path(self) -> Path:
        pass
