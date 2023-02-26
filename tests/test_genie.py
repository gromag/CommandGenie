import pytest
from genie.genie import Genie
from internals.ui_interaction import UIInteraction


class MockLanguageModel:
    pass


class MockUIInteraction(UIInteraction):
    """
    A mock implementation of the UIInteraction class that overrides the ask() method.
    """

    def ask(self, prompt):
        return "Y"


class TestGenie:
    @pytest.mark.parametrize(
        "answer, expected",
        [
            ("Yes", True),
            ("yes", True),
            ("Y", True),
            ("y", True),
            ("N", False),
        ],
    )
    def test_confirm_command(self, monkeypatch, answer, expected):
        # Arrange
        genie = Genie(MockLanguageModel(), MockUIInteraction())
        monkeypatch.setattr(MockUIInteraction, "ask", lambda s, _: answer)

        # Act
        output = genie.confirm_command("ls", "list files")
        
        # Assert
        assert output == expected, f"answer was {answer} and output expected was {expected}"

