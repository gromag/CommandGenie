import os
import sys
from dotenv import load_dotenv
from internals import shell_args
from genie.genie import Genie
from genie.models.openai_model import OpenAILanguageModel
from internals.ui_interaction import UIInteraction
load_dotenv()

model = OpenAILanguageModel(os.getenv("OPENAI_API_KEY"))
ui_interaction = UIInteraction()
genie = Genie(model, ui_interaction)


def start():
    # Get the command-line arguments
    args = sys.argv[1:]
    # Join the arguments into a single string
    instruction = " ".join(args).strip()

    if not len(instruction):
        shell_args.get_shell_args(["--help"])
    elif instruction[0] == "-":
        shell_args.get_shell_args()
    else:
        genie.run(instruction)


if __name__ == "__main__":
    start()
