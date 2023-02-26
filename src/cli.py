import os
import sys
from dotenv import load_dotenv
from internals import shell_args
from genie.genie import Genie
from genie.models.openai_model import OpenAILanguageModel
load_dotenv()

model = OpenAILanguageModel(os.getenv("OPENAI_API_KEY"))
genie = Genie(model)


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
