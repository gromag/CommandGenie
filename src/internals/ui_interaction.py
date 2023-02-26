from abstractions import UserInteractionBase


class UIInteraction(UserInteractionBase):
    def __init__(self) -> None:
        super().__init__()

    def ask(self, question) -> str:
        return input(question)

    def say(self, text: str):
        print(text)
